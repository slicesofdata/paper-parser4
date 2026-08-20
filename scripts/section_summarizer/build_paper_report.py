"""
Build a full-detail paper report by assembling all rendered .md files,
plus a PDF version and duplicate copies in processed/ at project root.

No LLM calls. Just file assembly + PDF rendering.

Reading order:
  1. Paper synthesis (executive brief)
  2. Abstract
  3. Paper-level introduction
  4. For each experiment: introduction, methods, results and discussion
  5. General discussion
  6. Critique (optional; excluded with --no-critique)

Usage:
  # Single paper
  uv run python -m scripts.section_summarizer.build_paper_report "<paper>"

  # All papers
  uv run python -m scripts.section_summarizer.build_paper_report --all

  # Skip critique in output
  uv run python -m scripts.section_summarizer.build_paper_report "<paper>" --no-critique

  # Force overwrite
  uv run python -m scripts.section_summarizer.build_paper_report "<paper>" --force

  # Skip PDF (markdown only)
  uv run python -m scripts.section_summarizer.build_paper_report "<paper>" --no-pdf
"""

from __future__ import annotations

import logging
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .config_loader import AppConfig, load_config
from .io_utils import list_papers, paper_output_dir


logger = logging.getLogger(__name__)


PROCESSED_DIR_NAME = "processed"
PDF_CONFIG_FILENAME = "pdf.yaml"


# ---------------------------------------------------------------------------
# Slug utilities
# ---------------------------------------------------------------------------

def _slugify_filename(text: str) -> str:
    """
    Full slug: lowercase, non-alphanumeric to underscores, collapse runs.

    Example:
      "Meeks, Knight, Brewer, Cook 2014 - Marsh Investigating..."
      -> "meeks_knight_brewer_cook_2014_marsh_investigating..."
    """
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    return s


def _slugify_anchor(text: str) -> str:
    """Slug for markdown anchor links (github-style)."""
    s = text.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    return s.strip("-")


# ---------------------------------------------------------------------------
# Section discovery and assembly (same as before, minor tweaks)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ReportSection:
    title: str
    anchor: str
    source_path: Path
    exists: bool


def _list_experiments(paper_dir: Path) -> list[str]:
    if not paper_dir.exists():
        return []
    return sorted(
        p.name for p in paper_dir.iterdir()
        if p.is_dir() and p.name.startswith("exp_")
    )


def _collect_sections(paper_dir: Path, include_critique: bool) -> list[ReportSection]:
    sections: list[ReportSection] = []

    def add(title: str, source: Path) -> None:
        sections.append(
            ReportSection(
                title=title,
                anchor=_slugify_anchor(title),
                source_path=source,
                exists=source.exists(),
            )
        )

    add("Paper Synthesis", paper_dir / "paper_overview.md")
    add("Abstract", paper_dir / "abstract.md")
    add("Introduction (Paper-Level)", paper_dir / "introduction.md")

    for exp in _list_experiments(paper_dir):
        pretty = exp.replace("exp_", "Experiment ").replace("_", " ")
        exp_dir = paper_dir / exp
        add(f"{pretty} — Introduction", exp_dir / "introduction.md")
        add(f"{pretty} — Methods", exp_dir / "methods.md")
        add(f"{pretty} — Results and Discussion", exp_dir / "results_and_discussion.md")

    add("General Discussion", paper_dir / "general_discussion.md")

    if include_critique:
        add("Critique", paper_dir / "critique.md")

    return sections


def _render_toc(sections: list[ReportSection]) -> str:
    lines = ["## Table of Contents", ""]
    for sec in sections:
        marker = "" if sec.exists else " *(not available)*"
        lines.append(f"- [{sec.title}](#{sec.anchor}){marker}")
    lines.append("")
    return "\n".join(lines)


def _demote_headings(content: str) -> str:
    def replace(match: re.Match) -> str:
        hashes = match.group(1)
        new_hashes = hashes + "#"
        if len(new_hashes) > 6:
            new_hashes = "######"
        return new_hashes + match.group(2)

    return re.sub(r"(?m)^(#{1,6})(\s)", replace, content)


def _strip_first_heading(content: str) -> str:
    """Remove the first markdown heading (source files start with # <title>)."""
    return re.sub(r"^\s*#+\s+[^\n]*\n+", "", content, count=1)


def _render_section(sec: ReportSection) -> str:
    """Render one report section: anchor + header + content (or missing note)."""
    # xhtml2pdf uses the older <a name="..."> anchor syntax for internal links,
    # not id="..." on headings.
    lines = [f'<a name="{sec.anchor}"></a>', f"## {sec.title}", ""]
    if not sec.exists:
        lines.append("*Not available for this paper.*")
        lines.append("")
        return "\n".join(lines)

    content = sec.source_path.read_text(encoding="utf-8").strip()
    content = _strip_first_heading(content)
    demoted = _demote_headings(content)
    lines.append(demoted)
    lines.append("")
    return "\n".join(lines)


def _assemble_markdown(paper_name: str, sections: list[ReportSection]) -> str:
    parts: list[str] = []
    parts.append(f"# {paper_name}")
    parts.append("")
    parts.append("*Auto-assembled report. Section content is drawn from the summarization pipeline outputs.*")
    parts.append("")
    parts.append(_render_toc(sections))
    for sec in sections:
        parts.append(_render_section(sec))
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# PDF rendering
# ---------------------------------------------------------------------------

def _load_pdf_config(cfg: AppConfig) -> dict[str, Any]:
    """Load PDF settings from config/pdf.yaml."""
    path = cfg.project_root / "config" / PDF_CONFIG_FILENAME
    if not path.exists():
        logger.warning(f"PDF config not found at {path}; using defaults.")
        return _default_pdf_config()
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    defaults = _default_pdf_config()
    defaults.update(data)
    if "heading_scale" in data and isinstance(data["heading_scale"], dict):
        defaults["heading_scale"] = {
            **defaults["heading_scale"],
            **data["heading_scale"],
        }
    return defaults


def _default_pdf_config() -> dict[str, Any]:
    return {
        "font_family": "Helvetica, Arial, sans-serif",
        "font_size_pt": 12,
        "line_height": 1.5,
        "heading_font_family": "Helvetica, Arial, sans-serif",
        "heading_scale": {"h1": 1.8, "h2": 1.4, "h3": 1.2, "h4": 1.1},
        "code_font_family": "Courier, monospace",
        "code_font_size_pt": 10,
        "margin_inches": 1.0,
        "paper_size": "letter",
        "show_page_numbers": True,
        "toc_link_color": "#0066cc",
        "blockquote_color": "#555555",
        "blockquote_border_color": "#dddddd",
        "output_prefix": "",
        "output_suffix": "_report",
    }


def _build_css(pdf_config: dict[str, Any], fonts_dir: Path) -> str:
    """
    Build CSS with @font-face declarations for Unicode support.

    Uses Bitstream Vera fonts bundled with reportlab. Covers em-dashes,
    en-dashes, curly quotes, and standard Latin Extended characters.
    """
    base_pt = pdf_config["font_size_pt"]
    scales = pdf_config["heading_scale"]
    h1_pt = round(base_pt * scales.get("h1", 1.8), 1)
    h2_pt = round(base_pt * scales.get("h2", 1.4), 1)
    h3_pt = round(base_pt * scales.get("h3", 1.2), 1)
    h4_pt = round(base_pt * scales.get("h4", 1.1), 1)

    vera_regular = fonts_dir.joinpath("Vera.ttf").as_uri()
    vera_bold = fonts_dir.joinpath("VeraBd.ttf").as_uri()
    vera_italic = fonts_dir.joinpath("VeraIt.ttf").as_uri()
    vera_bolditalic = fonts_dir.joinpath("VeraBI.ttf").as_uri()

    return f"""
@font-face {{
    font-family: "Vera";
    src: url("{vera_regular}");
}}

@font-face {{
    font-family: "Vera";
    src: url("{vera_bold}");
    font-weight: bold;
}}

@font-face {{
    font-family: "Vera";
    src: url("{vera_italic}");
    font-style: italic;
}}

@font-face {{
    font-family: "Vera";
    src: url("{vera_bolditalic}");
    font-weight: bold;
    font-style: italic;
}}

@page {{
    size: {pdf_config['paper_size']};
    margin: {pdf_config['margin_inches']}in;
    background-color: #ffffff;
}}

body {{
    font-family: "Vera";
    font-size: {base_pt}pt;
    line-height: {pdf_config['line_height']};
    color: #000000;
    background-color: #ffffff;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: "Vera";
    font-weight: bold;
    color: #000000;
}}

h1 {{ font-size: {h1_pt}pt; margin-top: 18pt; margin-bottom: 8pt; }}
h2 {{ font-size: {h2_pt}pt; margin-top: 14pt; margin-bottom: 6pt; border-bottom: 1pt solid #000000; padding-bottom: 3pt; }}
h3 {{ font-size: {h3_pt}pt; margin-top: 12pt; margin-bottom: 4pt; }}
h4 {{ font-size: {h4_pt}pt; margin-top: 10pt; margin-bottom: 4pt; }}

p {{ color: #000000; margin: 5pt 0; }}
ul, ol {{ color: #000000; margin: 5pt 0; padding-left: 20pt; }}
li {{ color: #000000; margin: 2pt 0; }}

code {{ font-family: "Courier"; font-size: {pdf_config['code_font_size_pt']}pt; color: #000000; }}
pre {{ font-family: "Courier"; font-size: {pdf_config['code_font_size_pt']}pt; color: #000000; border: 1pt solid #000000; padding: 5pt; }}

blockquote {{
    color: #000000;
    border-left: 3pt solid #000000;
    padding-left: 10pt;
    margin-left: 5pt;
    margin-top: 5pt;
    margin-bottom: 5pt;
}}

a {{ color: #000000; text-decoration: underline; }}

table {{ margin: 5pt 0; width: 100%; }}
th, td {{ color: #000000; border: 1pt solid #000000; padding: 3pt 6pt; vertical-align: top; }}
th {{ font-weight: bold; }}

hr {{ border-top: 1pt solid #000000; margin: 10pt 0; }}
em {{ color: #000000; font-style: italic; }}
strong {{ color: #000000; font-weight: bold; }}
"""

def _markdown_to_pdf(md_content: str, pdf_path: Path, pdf_config: dict[str, Any]) -> None:
    """Convert markdown to PDF via HTML + xhtml2pdf. Cross-platform, no system deps."""
    import markdown
    from xhtml2pdf import pisa
    import reportlab

    # Locate the Vera fonts bundled with reportlab.
    rl_dir = Path(reportlab.__file__).parent
    fonts_dir = rl_dir / "fonts"

    vera_regular = fonts_dir / "Vera.ttf"
    vera_bold = fonts_dir / "VeraBd.ttf"
    vera_italic = fonts_dir / "VeraIt.ttf"
    vera_bolditalic = fonts_dir / "VeraBI.ttf"

    # Register the fonts with reportlab (only once per process).
    _register_font_once("Vera", str(vera_regular))
    _register_font_once("Vera-Bold", str(vera_bold))
    _register_font_once("Vera-Italic", str(vera_italic))
    _register_font_once("Vera-BoldItalic", str(vera_bolditalic))

    normalized_md = _normalize_for_pdf(md_content)
    html_body = markdown.markdown(
        normalized_md,
        extensions=["extra", "toc", "sane_lists", "tables"],
    )
    
    css_text = _build_css(pdf_config, fonts_dir)

    html_full = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Report</title>
<style>
{css_text}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

    with open(pdf_path, "wb") as out_file:
        result = pisa.CreatePDF(html_full, dest=out_file, encoding="utf-8")

    if result.err:
        raise RuntimeError(f"xhtml2pdf reported {result.err} errors during PDF generation")


def _register_font_once(name: str, path: str) -> None:
    """Register a font with reportlab if not already registered."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    try:
        pdfmetrics.getFont(name)
    except KeyError:
        pdfmetrics.registerFont(TTFont(name, path))

# ---------------------------------------------------------------------------
# Main build function
# ---------------------------------------------------------------------------

def build_report(
    cfg: AppConfig,
    paper_name: str,
    *,
    include_critique: bool = True,
    write_pdf: bool = True,
    force: bool = False,
) -> bool:
    """
    Build a report for one paper.

    Writes:
      - summaries_output/<paper>/<prefix><slug><suffix>.md
      - summaries_output/<paper>/<prefix><slug><suffix>.pdf (unless --no-pdf)
      - processed/<prefix><slug><suffix>.md
      - processed/<prefix><slug><suffix>.pdf (unless --no-pdf)

    Prefix and suffix come from config/pdf.yaml.

    Returns True if any output was written.
    """
    paper_dir = paper_output_dir(cfg, paper_name)
    if not paper_dir.exists():
        logger.warning(f"[skip missing dir] {paper_name}")
        return False

    # Load PDF config once — used for filename prefix/suffix AND (later) PDF style.
    pdf_config = _load_pdf_config(cfg)
    prefix = pdf_config.get("output_prefix", "")
    suffix = pdf_config.get("output_suffix", "_report")

    slug = _slugify_filename(paper_name)
    filename_stem = f"{prefix}{slug}{suffix}"

    md_path = paper_dir / f"{filename_stem}.md"
    pdf_path = paper_dir / f"{filename_stem}.pdf"

    processed_dir = cfg.project_root / PROCESSED_DIR_NAME
    processed_dir.mkdir(exist_ok=True)
    processed_md = processed_dir / f"{filename_stem}.md"
    processed_pdf = processed_dir / f"{filename_stem}.pdf"

    if md_path.exists() and not force:
        logger.info(f"[skip cached]     {paper_name} (stem: {filename_stem})")
        return False

    sections = _collect_sections(paper_dir, include_critique=include_critique)
    if not any(sec.exists for sec in sections):
        logger.warning(f"[no content]      {paper_name}")
        return False

    # Assemble markdown.
    markdown_content = _assemble_markdown(paper_name, sections)
    md_path.write_text(markdown_content, encoding="utf-8")
    shutil.copy2(md_path, processed_md)
    missing = [sec.title for sec in sections if not sec.exists]
    missing_note = f"  (missing: {', '.join(missing)})" if missing else ""
    logger.info(f"[built .md]       {filename_stem}{missing_note}")

    # Render PDF using the already-loaded pdf_config.
    if write_pdf:
        try:
            _markdown_to_pdf(markdown_content, pdf_path, pdf_config)
            shutil.copy2(pdf_path, processed_pdf)
            logger.info(f"[built .pdf]      {filename_stem}")
        except ImportError as e:
            logger.warning(
                f"PDF rendering skipped -- dependency missing: {e}. "
                f"Run: uv add markdown xhtml2pdf"
            )
        except Exception as e:
            logger.error(f"PDF rendering failed for {filename_stem}: {e}")

    return True

# Character normalization map: Unicode punctuation that Vera doesn't render
# reliably, mapped to ASCII equivalents. Applied ONLY to the PDF pipeline;
# the source .md keeps the original Unicode.
_PDF_CHAR_MAP = {
    "\u2010": "-",   # hyphen
    "\u2011": "-",   # non-breaking hyphen (this is the "wordnfrequency" culprit)
    "\u2012": "-",   # figure dash
    "\u2013": "-",   # en-dash
    "\u2014": "--",  # em-dash
    "\u2015": "--",  # horizontal bar
    "\u2018": "'",   # left single quote
    "\u2019": "'",   # right single quote / apostrophe
    "\u201c": '"',   # left double quote
    "\u201d": '"',   # right double quote
    "\u2026": "...", # ellipsis
    "\u00a0": " ",   # non-breaking space
    "\u2032": "'",   # prime
    "\u2033": '"',   # double prime
}


def _normalize_for_pdf(text: str) -> str:
    """
    Replace Unicode punctuation the Vera font can't render with ASCII equivalents.

    Applied only when generating PDFs. The source markdown file is left with
    the original Unicode intact.
    """
    for src, dst in _PDF_CHAR_MAP.items():
        text = text.replace(src, dst)
    return text
    
# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    cfg = load_config()

    args = sys.argv[1:]
    include_critique = "--no-critique" not in args
    write_pdf = "--no-pdf" not in args
    force = "--force" in args
    all_mode = "--all" in args
    paper_args = [
        a for a in args
        if a not in ("--no-critique", "--no-pdf", "--force", "--all")
    ]

    if all_mode:
        papers = list_papers(cfg)
    elif paper_args:
        papers = paper_args
    else:
        print(
            "Usage:\n"
            "  uv run python -m scripts.section_summarizer.build_paper_report <paper> [options]\n"
            "  uv run python -m scripts.section_summarizer.build_paper_report --all [options]\n"
            "\n"
            "Options:\n"
            "  --no-critique   Exclude the critique section from the report\n"
            "  --no-pdf        Skip PDF generation (markdown only)\n"
            "  --force         Overwrite existing outputs\n"
            "  --all           Process every paper in sections_output/"
        )
        sys.exit(1)

    if not papers:
        print("No papers found.")
        sys.exit(0)

    built = 0
    for p in papers:
        if build_report(
            cfg, p,
            include_critique=include_critique,
            write_pdf=write_pdf,
            force=force,
        ):
            built += 1

    print(f"\nDone. Built: {built} / {len(papers)}")