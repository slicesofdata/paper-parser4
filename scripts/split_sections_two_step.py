"""
Split MinerU content_list_v2.json into per-experiment section markdown files.

Directory structure:
  sections_output/<paper>/
    title.md, authors.md, abstract.md, keywords.md,
    introduction.md, general_discussion.md, references.md, footnotes.md,
    exp_1/{introduction.md, methods.md, results_and_discussion.md}
    exp_2/...
    _debug.txt
"""
import json
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


# ---- Section alias table (used within experiments) ----
METHODS_ALIASES = {"methods", "method", "materials and methods", "experimental",
                   "methodology", "materials & methods", "study design",
                   "materials and procedure", "participants", "procedure"}
RESULTS_ALIASES = {"results", "findings", "results and analysis"}
DISCUSSION_ALIASES = {"discussion"}
RD_COMBINED_ALIASES = {"results and discussion"}

# Paper-level sections
GENERAL_DISCUSSION_ALIASES = {"general discussion"}
CONCLUSION_ALIASES = {"conclusion", "conclusions", "concluding remarks"}
REFERENCES_ALIASES = {"references", "bibliography", "works cited"}
ACKNOWLEDGMENTS_ALIASES = {"acknowledgments", "acknowledgements"}

INSTITUTION_KEYWORDS = [
    "university", "college", "institute", "department",
    "school", "laboratory", "hospital", "center", "centre",
]

SKIP_BLOCK_TYPES = {"page_header", "page_footer", "page_number", "page_aside_text"}


def normalize_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"^\d+(\.\d+)*\.?\s*", "", text)
    text = re.sub(r"[:\.\-–—]+$", "", text)
    return text.strip()


def is_experiment_heading(text: str) -> tuple[bool, str]:
    """
    Returns (is_experiment, normalized_label).
    Matches: 'Experiment 1', 'Experiment 3a', 'Experiments 3a and 3b',
             'Study 1', 'Study 2', etc.
    """
    t = text.strip()
    # "Experiments 3a and 3b" style
    m = re.match(r"^\s*experiment[s]?\s+(\d+[a-z]?(?:\s+and\s+\d+[a-z]?)*)",
                 t, re.IGNORECASE)
    if m:
        label = re.sub(r"\s+and\s+", "_and_", m.group(1).lower())
        return True, f"exp_{label}"
    # "Study 1", "Studies 1 and 2"
    m = re.match(r"^\s*stud(?:y|ies)\s+(\d+[a-z]?(?:\s+and\s+\d+[a-z]?)*)",
                 t, re.IGNORECASE)
    if m:
        label = re.sub(r"\s+and\s+", "_and_", m.group(1).lower())
        return True, f"exp_{label}"
    return False, ""


def classify_section(text: str) -> str | None:
    """Classify a heading into: methods, results, discussion, results_and_discussion,
    general_discussion, references, acknowledgments, conclusion, or None."""
    normalized = normalize_heading(text)
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


def render_inline_content(items: list) -> str:
    parts = []
    for item in items:
        itype = item.get("type", "")
        content = item.get("content", "")
        if itype == "text":
            parts.append(content)
        elif itype == "equation_inline":
            parts.append(f"${content}$")
        else:
            parts.append(content)
    return "".join(parts).strip()


def block_to_markdown(block: dict) -> str:
    btype = block.get("type", "")
    content = block.get("content", {})

    if btype == "title":
        text = render_inline_content(content.get("title_content", []))
        level = content.get("level", 2)
        return "#" * level + " " + text

    if btype == "paragraph":
        return render_inline_content(content.get("paragraph_content", []))

    if btype == "table":
        html = content.get("html", "")
        cap_items = content.get("table_caption", [])
        cap = render_inline_content(cap_items) if cap_items else ""
        return (f"**{cap}**\n\n" if cap else "") + html

    if btype == "list":
        items = content.get("list_items", [])
        lines = []
        for it in items:
            item_content = it.get("item_content", [])
            lines.append("- " + render_inline_content(item_content))
        return "\n".join(lines)

    if btype == "page_footnote":
        return render_inline_content(content.get("page_footnote_content", []))

    if btype == "equation":
        text = content.get("text", "").strip()
        return f"$$\n{text}\n$$"

    return ""


def get_paragraph_text(block: dict) -> str:
    if block.get("type") != "paragraph":
        return ""
    return render_inline_content(block.get("content", {}).get("paragraph_content", []))


def get_title_info(block: dict) -> tuple[str, int] | None:
    if block.get("type") != "title":
        return None
    content = block.get("content", {})
    text = render_inline_content(content.get("title_content", []))
    level = content.get("level", 2)
    return text, level


def flatten_pages(pages: list) -> list[dict]:
    flat = []
    for page in pages:
        for block in page:
            btype = block.get("type", "")
            if btype in SKIP_BLOCK_TYPES:
                continue
            if btype == "paragraph":
                if not block.get("content", {}).get("paragraph_content"):
                    continue
            flat.append(block)
    return flat


def parse_paper(blocks: list[dict]) -> dict:
    """
    Parse blocks into a structured representation:
    {
      "frontmatter": {
        "title": [blocks], "authors": [blocks], "abstract": [blocks],
        "keywords": [blocks], "introduction": [blocks],
      },
      "experiments": OrderedDict[exp_label -> {
        "introduction": [blocks], "methods": [blocks],
        "results": [blocks], "discussion": [blocks],
        "results_and_discussion": [blocks],
      }],
      "backmatter": {
        "general_discussion": [blocks], "conclusion": [blocks],
        "references": [blocks], "acknowledgments": [blocks],
        "footnotes": [blocks], "unmatched": [blocks],
      }
    }
    """
    from collections import OrderedDict

    result = {
        "frontmatter": {"title": [], "authors": [], "abstract": [],
                        "keywords": [], "introduction": []},
        "experiments": OrderedDict(),
        "backmatter": {"general_discussion": [], "conclusion": [],
                       "references": [], "acknowledgments": [],
                       "footnotes": [], "unmatched": []},
    }

    stage = "title"
    current_experiment = None      # None = paper-level; str = "exp_1", etc.
    current_section = None         # within an experiment: "methods"/"results"/etc.
    in_backmatter = False

    def ensure_exp(label: str):
        if label not in result["experiments"]:
            result["experiments"][label] = {
                "introduction": [], "methods": [],
                "results": [], "discussion": [],
                "results_and_discussion": [],
            }

    for block in blocks:
        btype = block.get("type", "")

        if btype == "page_footnote":
            result["backmatter"]["footnotes"].append(block)
            continue

        title_info = get_title_info(block)
        if title_info:
            text, level = title_info

            # Paper title
            if level == 1:
                result["frontmatter"]["title"].append(block)
                stage = "authors"
                continue

            # Experiment / Study heading
            is_exp, exp_label = is_experiment_heading(text)
            if is_exp:
                current_experiment = exp_label
                current_section = "introduction"  # paragraphs after exp heading are exp intro
                ensure_exp(exp_label)
                # Store the heading itself in the experiment's introduction
                result["experiments"][exp_label]["introduction"].append(block)
                in_backmatter = False
                stage = "in_experiment"
                continue

            # Classify the heading
            section_type = classify_section(text)

            # Paper-level backmatter sections
            if section_type in ("general_discussion", "references",
                                "acknowledgments", "conclusion"):
                in_backmatter = True
                current_experiment = None
                current_section = section_type
                result["backmatter"][section_type].append(block)
                stage = "in_backmatter"
                continue

            # Within-experiment section headings (methods/results/discussion/R&D)
            if section_type in ("methods", "results", "discussion",
                                "results_and_discussion"):
                if current_experiment is None:
                    # Single-experiment paper without explicit "Experiment 1" label.
                    # Create implicit exp_1.
                    current_experiment = "exp_1"
                    ensure_exp(current_experiment)
                current_section = section_type
                result["experiments"][current_experiment][section_type].append(block)
                stage = "in_experiment"
                continue

            # Unmatched heading
            if in_backmatter:
                result["backmatter"]["unmatched"].append(block)
            elif current_experiment:
                # Store in current section as an inline sub-heading
                result["experiments"][current_experiment][current_section or "introduction"].append(block)
            else:
                result["backmatter"]["unmatched"].append(block)
            continue

        # Non-heading block routing
        if stage == "in_backmatter" and current_section:
            result["backmatter"][current_section].append(block)
            continue

        if stage == "in_experiment" and current_experiment and current_section:
            result["experiments"][current_experiment][current_section].append(block)
            continue

        # Frontmatter routing (before first experiment or backmatter section)
        if btype == "paragraph":
            text = get_paragraph_text(block)

            if re.match(r"^\s*key\s*words?\s*[:\-]", text, re.IGNORECASE):
                result["frontmatter"]["keywords"].append(block)
                stage = "introduction"
                continue

            if stage == "authors":
                if looks_like_author_block(text):
                    result["frontmatter"]["authors"].append(block)
                    continue
                stage = "abstract"

            if stage == "abstract":
                result["frontmatter"]["abstract"].append(block)
                stage = "post_abstract"
                continue

            if stage == "post_abstract":
                stage = "introduction"

            result["frontmatter"]["introduction"].append(block)
            continue

        # Non-paragraph, non-title in frontmatter → introduction
        result["frontmatter"]["introduction"].append(block)

    return result


def write_blocks_to_file(path: Path, blocks: list[dict]):
    if not blocks:
        return
    md_parts = [block_to_markdown(b) for b in blocks]
    md_text = "\n\n".join(p for p in md_parts if p)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md_text, encoding="utf-8")


def write_paper(paper_out: Path, parsed: dict):
    paper_out.mkdir(parents=True, exist_ok=True)

    # Frontmatter files
    for name, blocks in parsed["frontmatter"].items():
        write_blocks_to_file(paper_out / f"{name}.md", blocks)

    # Backmatter files
    for name, blocks in parsed["backmatter"].items():
        write_blocks_to_file(paper_out / f"{name}.md", blocks)

    # If no experiments detected but paper has methods/results content
    # captured somewhere, treat as single-experiment
    if not parsed["experiments"]:
        # No sections were found matching methods/results/discussion at all;
        # nothing to write for experiments
        pass

    # Experiment folders
    for exp_label, sections in parsed["experiments"].items():
        exp_dir = paper_out / exp_label
        exp_dir.mkdir(exist_ok=True)

        # Introduction (per-experiment intro paragraphs)
        write_blocks_to_file(exp_dir / "introduction.md", sections["introduction"])

        # Methods
        write_blocks_to_file(exp_dir / "methods.md", sections["methods"])

        # Results and Discussion: merge in order
        rd_blocks = (sections["results"]
                     + sections["discussion"]
                     + sections["results_and_discussion"])
        write_blocks_to_file(exp_dir / "results_and_discussion.md", rd_blocks)


def write_debug(paper_out: Path, parsed: dict):
    lines = []
    lines.append("=== FRONTMATTER ===")
    for name, blocks in parsed["frontmatter"].items():
        for b in blocks:
            lines.append(_preview_line(name, b))

    for exp_label, sections in parsed["experiments"].items():
        lines.append(f"\n=== {exp_label.upper()} ===")
        for name, blocks in sections.items():
            for b in blocks:
                lines.append(_preview_line(f"{exp_label}/{name}", b))

    lines.append("\n=== BACKMATTER ===")
    for name, blocks in parsed["backmatter"].items():
        for b in blocks:
            lines.append(_preview_line(name, b))

    (paper_out / "_debug.txt").write_text("\n".join(lines), encoding="utf-8")


def _preview_line(label: str, block: dict) -> str:
    btype = block.get("type", "")
    if btype == "paragraph":
        preview = get_paragraph_text(block)[:120].replace("\n", " ")
    elif btype == "title":
        info = get_title_info(block)
        preview = f"<H{info[1]}> {info[0]}" if info else "<title>"
    else:
        preview = f"<{btype}>"
    return f"[{label}] {preview}"


def find_content_list(paper_dir: Path) -> Path | None:
    auto_dir = paper_dir / "auto"
    if not auto_dir.exists():
        return None
    v2 = list(auto_dir.glob("*_content_list_v2.json"))
    if v2:
        return v2[0]
    v1 = list(auto_dir.glob("*_content_list.json"))
    return v1[0] if v1 else None


def load_v2(path: Path) -> list[dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not raw:
        return []
    if isinstance(raw[0], list):
        return flatten_pages(raw)
    return [b for b in raw if b.get("type") not in SKIP_BLOCK_TYPES]


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

        content_list = find_content_list(paper_dir)
        if not content_list:
            log.warning(f"NO content_list found for: {paper_name}")
            failed += 1
            continue

        log.info(f"SPLITTING: {paper_name} ← {content_list.name}")
        try:
            blocks = load_v2(content_list)
            parsed = parse_paper(blocks)
            write_paper(paper_out, parsed)
            write_debug(paper_out, parsed)
            n_exp = len(parsed["experiments"])
            log.info(f"  DONE: {n_exp} experiment(s) → {list(parsed['experiments'].keys())}")
            done += 1
        except Exception as e:
            log.exception(f"  FAILED: {paper_name} — {e}")
            failed += 1

    log.info(f"Summary: done={done} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()