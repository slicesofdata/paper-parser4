"""
Split MinerU markdown files into per-experiment section files.

Reads:  markdown_output/<paper>/auto/<paper>.md
Writes: sections_output/<paper>/
          title.md, authors.md, abstract.md, keywords.md,
          article_info.md, introduction.md,
          general_discussion.md, references.md, appendix.md, footnotes.md,
          exp_1/{introduction.md, methods.md, results_and_discussion.md}
          exp_2/...
          _debug.txt
"""
import logging
import re
import sys
from pathlib import Path

# ---- Paths ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "markdown_output"
OUTPUT_DIR = PROJECT_ROOT / "sections_output"
LOG_DIR = PROJECT_ROOT / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "split_sections.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


# ---- Section classification ----
METHODS_ALIASES = {"methods", "method", "materials and methods", "experimental",
                   "methodology", "materials & methods", "study design",
                   "materials and procedure", "participants", "procedure"}
RESULTS_ALIASES = {"results", "findings", "results and analysis"}
DISCUSSION_ALIASES = {"discussion"}
RD_COMBINED_ALIASES = {"results and discussion"}
INTRODUCTION_ALIASES = {"introduction", "background"}
GENERAL_DISCUSSION_ALIASES = {"general discussion"}
CONCLUSION_ALIASES = {"conclusion", "conclusions", "concluding remarks"}
REFERENCES_ALIASES = {"references", "bibliography", "works cited"}
ACKNOWLEDGMENTS_ALIASES = {"acknowledgments", "acknowledgements"}

INSTITUTION_KEYWORDS = [
    "university", "college", "institute", "department",
    "school", "laboratory", "hospital", "center", "centre",
]


def normalize_heading(text: str) -> str:
    """Lowercase, strip leading numbering like '5.1.', strip trailing punct."""
    text = text.strip().lower()
    text = re.sub(r"^\d+(\.\d+)*\.?\s*", "", text)
    text = re.sub(r"[:\.\-–—]+$", "", text)
    return text.strip()


def is_experiment_heading(text: str) -> tuple[bool, str]:
    """
    Match 'Experiment N', 'Study N', '5. Experiment 1', 'Experiments 3a and 3b'.
    Returns (True, 'exp_N') on match, else (False, '').
    """
    t = text.strip()
    t = re.sub(r"^\d+(\.\d+)*\.?\s+", "", t)  # strip leading "5. " or "5.1. "

    m = re.match(r"^experiment[s]?\s+(\d+[a-z]?(?:\s+and\s+\d+[a-z]?)*)",
                 t, re.IGNORECASE)
    if m:
        label = re.sub(r"\s+and\s+", "_and_", m.group(1).lower())
        return True, f"exp_{label}"

    m = re.match(r"^stud(?:y|ies)\s+(\d+[a-z]?(?:\s+and\s+\d+[a-z]?)*)",
                 t, re.IGNORECASE)
    if m:
        label = re.sub(r"\s+and\s+", "_and_", m.group(1).lower())
        return True, f"exp_{label}"

    return False, ""


def classify_section(text: str) -> str | None:
    """Classify a heading into a canonical section name."""
    normalized = normalize_heading(text)
    despaced = re.sub(r"\s+", "", normalized)  # for Elsevier "a b s t r a c t"

    if despaced == "abstract":
        return "abstract"
    if despaced in ("articleinfo", "articleinformation"):
        return "article_info"
    if normalized in INTRODUCTION_ALIASES:
        return "introduction"
    if normalized.startswith("appendix"):
        return "appendix"
    if normalized in METHODS_ALIASES:
        return "methods"
    if normalized in RESULTS_ALIASES:
        return "results"
    if normalized in DISCUSSION_ALIASES:
        return "discussion"
    if normalized in RD_COMBINED_ALIASES:
        return "results_and_discussion"
    if normalized in GENERAL_DISCUSSION_ALIASES:
        return "general_discussion"
    if normalized in CONCLUSION_ALIASES:
        return "conclusion"
    if normalized in REFERENCES_ALIASES:
        return "references"
    if normalized in ACKNOWLEDGMENTS_ALIASES:
        return "acknowledgments"
    return None


def looks_like_author_block(text: str) -> bool:
    lower = text.lower()
    if any(kw in lower for kw in INSTITUTION_KEYWORDS):
        return True
    return len(text) < 100


# ---- Markdown parsing ----

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def split_into_sections(md_text: str) -> list[tuple[int, str, str]]:
    """
    Split markdown into a list of (heading_level, heading_text, body).
    The first entry has level=0, heading_text='' if the file starts with content
    before any heading.
    """
    sections: list[tuple[int, str, str]] = []
    current_level = 0
    current_heading = ""
    current_body: list[str] = []

    for line in md_text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            # Flush previous section
            body = "\n".join(current_body).strip()
            if current_heading or body:
                sections.append((current_level, current_heading, body))
            current_level = len(m.group(1))
            current_heading = m.group(2).strip()
            current_body = []
        else:
            current_body.append(line)

    # Flush final section
    body = "\n".join(current_body).strip()
    if current_heading or body:
        sections.append((current_level, current_heading, body))

    return sections


def split_one_paper(paper_dir: Path, output_dir: Path = None) -> bool:
    """
    Split one paper's MinerU markdown into sections.

    Args:
        paper_dir: markdown_output/<paper>/ directory
        output_dir: sections_output/ root (defaults to global OUTPUT_DIR)

    Returns True on success.
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR

    paper_name = paper_dir.name
    paper_out = output_dir / paper_name

    md_file = find_markdown(paper_dir)
    if not md_file:
        log.warning(f"NO markdown found for: {paper_name}")
        return False

    log.info(f"SPLITTING: {paper_name} <- {md_file.name}")
    md_text = md_file.read_text(encoding="utf-8")
    raw_sections = split_into_sections(md_text)
    parsed = parse_paper(raw_sections)
    write_paper(paper_out, parsed)
    write_debug(paper_out, parsed, raw_sections)
    n_exp = len(parsed["experiments"])
    log.info(f"  DONE: {n_exp} experiment(s) -> {list(parsed['experiments'].keys())}")
    return True
    
# ---- Paper parsing ----

def parse_paper(sections: list[tuple[int, str, str]]) -> dict:
    """
    Route each (level, heading, body) tuple into the paper structure.
    """
    from collections import OrderedDict

    result = {
        "frontmatter": {
            "title": "", "authors": "", "abstract": "",
            "keywords": "", "article_info": "", "introduction": "",
        },
        "experiments": OrderedDict(),
        "backmatter": {
            "general_discussion": "", "conclusion": "",
            "references": "", "acknowledgments": "",
            "appendix": "", "footnotes": "", "unmatched": "",
        },
    }

    stage = "prelude"       # prelude → authors → abstract → intro → in_experiment → in_backmatter
    current_experiment = None
    current_section = None
    in_backmatter = False

    def append(bucket_dict: dict, key: str, heading: str, body: str, level: int = 2):
        """Append heading + body to a bucket, preserving heading as markdown."""
        chunk = ""
        if heading:
            chunk = f"{'#' * level} {heading}\n\n"
        if body:
            chunk += body
        if not chunk.strip():
            return
        existing = bucket_dict.get(key, "")
        bucket_dict[key] = (existing + "\n\n" + chunk).strip() if existing else chunk

    def ensure_exp(label: str):
        if label not in result["experiments"]:
            result["experiments"][label] = {
                "introduction": "", "methods": "",
                "results": "", "discussion": "",
                "results_and_discussion": "",
            }

    for level, heading, body in sections:

        # ---- Level 0 (content before any heading) ----
        if level == 0:
            # Rare: content before the paper title. Treat as unmatched.
            if body:
                result["backmatter"]["unmatched"] += body + "\n\n"
            continue

        # ---- Level 1 = paper title ----
        if level == 1:
            result["frontmatter"]["title"] = heading
            # Any body immediately under the title is authors (unless it looks like abstract)
            if body:
                # Split by blank lines; short lines with institutions are authors
                paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
                author_paras = []
                other_paras = []
                seen_long = False
                for p in paragraphs:
                    if not seen_long and looks_like_author_block(p):
                        author_paras.append(p)
                    else:
                        seen_long = True
                        other_paras.append(p)
                if author_paras:
                    result["frontmatter"]["authors"] = "\n\n".join(author_paras)
                if other_paras:
                    # Assume first long block after authors is abstract
                    if not result["frontmatter"]["abstract"]:
                        result["frontmatter"]["abstract"] = other_paras[0]
                        remaining = other_paras[1:]
                    else:
                        remaining = other_paras
                    if remaining:
                        result["frontmatter"]["introduction"] += "\n\n".join(remaining)
            stage = "post_title"
            continue

        # ---- Level 2+ headings ----
        heading_text = heading

        # Experiment heading?
        is_exp, exp_label = is_experiment_heading(heading_text)
        if is_exp:
            current_experiment = exp_label
            current_section = "introduction"
            ensure_exp(exp_label)
            append(result["experiments"][exp_label], "introduction",
                   heading_text, body, level)
            in_backmatter = False
            stage = "in_experiment"
            continue

        section_type = classify_section(heading_text)

        # Elsevier front-matter markers
        if section_type == "article_info":
            append(result["frontmatter"], "article_info", heading_text, body, level)
            stage = "article_info"
            # Also try to extract keywords from body
            if body:
                for line in body.splitlines():
                    if re.match(r"^\s*key\s*words?\s*[:\-]", line, re.IGNORECASE):
                        existing = result["frontmatter"]["keywords"]
                        result["frontmatter"]["keywords"] = (
                            existing + "\n" + line if existing else line
                        )
            continue

        if section_type == "abstract":
            append(result["frontmatter"], "abstract", heading_text, body, level)
            stage = "post_abstract"
            continue

        if section_type == "introduction":
            append(result["frontmatter"], "introduction", heading_text, body, level)
            stage = "extended_intro"
            current_experiment = None
            current_section = None
            in_backmatter = False
            continue

        # Paper-level backmatter
        if section_type in ("general_discussion", "references",
                            "acknowledgments", "conclusion", "appendix"):
            append(result["backmatter"], section_type, heading_text, body, level)
            in_backmatter = True
            current_experiment = None
            current_section = section_type
            stage = "in_backmatter"
            continue

        # Within-experiment section headings
        if section_type in ("methods", "results", "discussion", "results_and_discussion"):
            if current_experiment is None:
                # Single-experiment paper without explicit "Experiment 1" label
                current_experiment = "exp_1"
                ensure_exp(current_experiment)
            current_section = section_type
            append(result["experiments"][current_experiment], section_type,
                   heading_text, body, level)
            stage = "in_experiment"
            continue

        # ---- Unmatched heading ----
        # Route by current stage
        if stage == "in_experiment" and current_experiment and current_section:
            append(result["experiments"][current_experiment], current_section,
                   heading_text, body, level)
        elif stage == "extended_intro":
            append(result["frontmatter"], "introduction", heading_text, body, level)
        elif stage == "in_backmatter" and current_section:
            append(result["backmatter"], current_section, heading_text, body, level)
        elif stage == "post_abstract":
            # After abstract but before any recognized section — treat as intro
            append(result["frontmatter"], "introduction", heading_text, body, level)
            stage = "extended_intro"
        else:
            append(result["backmatter"], "unmatched", heading_text, body, level)

    return result


# ---- File writing ----

def write_paper(paper_out: Path, parsed: dict):
    paper_out.mkdir(parents=True, exist_ok=True)

    # Frontmatter
    for name, text in parsed["frontmatter"].items():
        if text.strip():
            (paper_out / f"{name}.md").write_text(text, encoding="utf-8")

    # Backmatter
    for name, text in parsed["backmatter"].items():
        if text.strip():
            (paper_out / f"{name}.md").write_text(text, encoding="utf-8")

    # Experiments
    for exp_label, sections in parsed["experiments"].items():
        exp_dir = paper_out / exp_label
        exp_dir.mkdir(exist_ok=True)

        if sections["introduction"].strip():
            (exp_dir / "introduction.md").write_text(sections["introduction"], encoding="utf-8")
        if sections["methods"].strip():
            (exp_dir / "methods.md").write_text(sections["methods"], encoding="utf-8")

        # Combine results + discussion + results_and_discussion in order
        rd_parts = []
        if sections["results"].strip():
            rd_parts.append(sections["results"])
        if sections["discussion"].strip():
            rd_parts.append(sections["discussion"])
        if sections["results_and_discussion"].strip():
            rd_parts.append(sections["results_and_discussion"])
        if rd_parts:
            (exp_dir / "results_and_discussion.md").write_text(
                "\n\n".join(rd_parts), encoding="utf-8"
            )


def write_debug(paper_out: Path, parsed: dict, raw_sections: list):
    lines = []

    lines.append("=== HEADING SCAN (raw) ===")
    for level, heading, body in raw_sections:
        if heading:
            preview = body[:80].replace("\n", " ") if body else ""
            lines.append(f"  H{level}: {heading!r}  body:{preview!r}")
        else:
            preview = body[:80].replace("\n", " ") if body else ""
            lines.append(f"  L{level} (no heading)  body:{preview!r}")

    lines.append("\n=== FRONTMATTER ===")
    for name, text in parsed["frontmatter"].items():
        if text.strip():
            preview = text[:150].replace("\n", " ")
            lines.append(f"  [{name}] {preview}")

    for exp_label, sections in parsed["experiments"].items():
        lines.append(f"\n=== {exp_label.upper()} ===")
        for name, text in sections.items():
            if text.strip():
                preview = text[:150].replace("\n", " ")
                lines.append(f"  [{name}] {preview}")

    lines.append("\n=== BACKMATTER ===")
    for name, text in parsed["backmatter"].items():
        if text.strip():
            preview = text[:150].replace("\n", " ")
            lines.append(f"  [{name}] {preview}")

    (paper_out / "_debug.txt").write_text("\n".join(lines), encoding="utf-8")


def find_markdown(paper_dir: Path) -> Path | None:
    auto_dir = paper_dir / "auto"
    if not auto_dir.exists():
        return None
    md_files = list(auto_dir.glob("*.md"))
    # Prefer the one that matches the paper name; fallback to any
    for md in md_files:
        if md.stem == paper_dir.name:
            return md
    return md_files[0] if md_files else None


def main():
    if not INPUT_DIR.exists():
        log.error(f"Input directory missing: {INPUT_DIR}")
        sys.exit(1)

    paper_dirs = [p for p in INPUT_DIR.iterdir() if p.is_dir()]
    log.info(f"Found {len(paper_dirs)} paper directories")

    done = skipped = failed = 0

    for paper_dir in sorted(paper_dirs):
        paper_name = paper_dir.name
        paper_out = OUTPUT_DIR / paper_name

        if paper_out.exists() and (paper_out / "_debug.txt").exists():
            log.info(f"SKIP (already done): {paper_name}")
            skipped += 1
            continue

        md_file = find_markdown(paper_dir)
        if not md_file:
            log.warning(f"NO markdown found for: {paper_name}")
            failed += 1
            continue

        log.info(f"SPLITTING: {paper_name} ← {md_file.name}")
        try:
            md_text = md_file.read_text(encoding="utf-8")
            raw_sections = split_into_sections(md_text)
            parsed = parse_paper(raw_sections)
            write_paper(paper_out, parsed)
            write_debug(paper_out, parsed, raw_sections)
            n_exp = len(parsed["experiments"])
            log.info(f"  DONE: {n_exp} experiment(s) → {list(parsed['experiments'].keys())}")
            done += 1
        except Exception as e:
            log.exception(f"  FAILED: {paper_name} — {e}")
            failed += 1

    log.info(f"Summary: done={done} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()