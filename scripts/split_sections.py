"""
Split MinerU content_list_v2.json into canonical section markdown files.

Reads:  markdown_output/<paper>/auto/<paper>_content_list_v2.json
Writes: sections_output/<paper>/{title,authors,abstract,keywords,
                                 introduction,methods,results,discussion,
                                 general_discussion,references,
                                 experiment_intros,footnotes,unmatched}.md
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


# ---- Section alias table ----
SECTION_ALIASES = {
    "introduction": ["introduction", "background"],
    "methods": ["methods", "method", "materials and methods", "experimental",
                "methodology", "materials & methods", "study design",
                "materials and procedure", "participants", "procedure"],
    "results": ["results", "findings", "results and analysis",
                "results and discussion"],
    "discussion": ["discussion"],
    "general_discussion": ["general discussion"],
    "conclusion": ["conclusion", "conclusions", "concluding remarks"],
    "references": ["references", "bibliography", "works cited"],
    "acknowledgments": ["acknowledgments", "acknowledgements"],
}

INSTITUTION_KEYWORDS = [
    "university", "college", "institute", "department",
    "school", "laboratory", "hospital", "center", "centre",
]

# Block types to drop entirely
SKIP_BLOCK_TYPES = {"page_header", "page_footer", "page_number", "page_aside_text"}


def normalize_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"^\d+(\.\d+)*\.?\s*", "", text)
    text = re.sub(r"[:\.\-–—]+$", "", text)
    return text.strip()


def map_to_canonical(heading: str) -> str | None:
    normalized = normalize_heading(heading)
    for canonical, aliases in SECTION_ALIASES.items():
        if normalized in aliases:
            return canonical
    return None


def is_experiment_heading(text: str) -> bool:
    return bool(re.match(r"^\s*experiment[s]?\s+\d", text.strip(), re.IGNORECASE))


def looks_like_author_block(text: str) -> bool:
    lower = text.lower()
    if any(kw in lower for kw in INSTITUTION_KEYWORDS):
        return True
    return len(text) < 100


def render_inline_content(items: list) -> str:
    """Render mixed text + equation_inline content."""
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
        items = content.get("paragraph_content", [])
        return render_inline_content(items)

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
        text = render_inline_content(content.get("page_footnote_content", []))
        return text

    if btype == "equation":
        text = content.get("text", "").strip()
        return f"$$\n{text}\n$$"

    return ""


def get_paragraph_text(block: dict) -> str:
    """Extract just the text from a paragraph block."""
    if block.get("type") != "paragraph":
        return ""
    return render_inline_content(block.get("content", {}).get("paragraph_content", []))


def get_title_info(block: dict) -> tuple[str, int] | None:
    """Return (text, level) if title, else None."""
    if block.get("type") != "title":
        return None
    content = block.get("content", {})
    text = render_inline_content(content.get("title_content", []))
    level = content.get("level", 2)
    return text, level


def flatten_pages(pages: list) -> list[dict]:
    """v2 is [page[blocks], page[blocks], ...]. Flatten to single block list."""
    flat = []
    for page in pages:
        for block in page:
            btype = block.get("type", "")
            if btype in SKIP_BLOCK_TYPES:
                continue
            # skip empty paragraphs
            if btype == "paragraph":
                if not block.get("content", {}).get("paragraph_content"):
                    continue
            flat.append(block)
    return flat


def split_paper(blocks: list[dict]) -> dict[str, list[dict]]:
    sections: dict[str, list[dict]] = {}

    def append(name: str, block: dict):
        sections.setdefault(name, []).append(block)

    stage = "title"
    current_section = None  # canonical section once we cross frontmatter

    for block in blocks:
        btype = block.get("type", "")

        # ---- Footnotes: always to their own bucket ----
        if btype == "page_footnote":
            append("footnotes", block)
            continue

        # ---- Titles: potential section boundaries ----
        title_info = get_title_info(block)
        if title_info:
            text, level = title_info

            # Level 1 = paper title
            if level == 1:
                append("title", block)
                stage = "authors"
                continue

            # Level 2+ headings past frontmatter
            if is_experiment_heading(text):
                current_section = "experiment_intros"
                append(current_section, block)
                stage = "body"
                continue

            canonical = map_to_canonical(text)
            if canonical:
                current_section = canonical
            else:
                current_section = "unmatched"
            append(current_section, block)
            stage = "body"
            continue

        # ---- Once in body sections, route everything to current ----
        if stage == "body" and current_section:
            append(current_section, block)
            continue

        # ---- Frontmatter routing (before first level-2 heading) ----
        if btype == "paragraph":
            text = get_paragraph_text(block)

            # Keywords line
            if re.match(r"^\s*key\s*words?\s*[:\-]", text, re.IGNORECASE):
                append("keywords", block)
                stage = "introduction"
                continue

            if stage == "authors":
                if looks_like_author_block(text):
                    append("authors", block)
                    continue
                # First non-author paragraph → abstract
                stage = "abstract"

            if stage == "abstract":
                append("abstract", block)
                stage = "post_abstract"
                continue

            if stage == "post_abstract":
                stage = "introduction"

            append("introduction", block)
            continue

        # ---- Anything else in frontmatter (tables, lists) → intro ----
        append("introduction", block)

    return sections


def write_section_files(paper_out: Path, sections: dict[str, list[dict]]):
    paper_out.mkdir(parents=True, exist_ok=True)
    for name, blocks in sections.items():
        if not blocks:
            continue
        md_parts = [block_to_markdown(b) for b in blocks]
        md_text = "\n\n".join(p for p in md_parts if p)
        (paper_out / f"{name}.md").write_text(md_text, encoding="utf-8")


def write_debug(paper_out: Path, sections: dict[str, list[dict]]):
    lines = []
    for name, blocks in sections.items():
        for b in blocks:
            btype = b.get("type", "")
            if btype == "paragraph":
                preview = get_paragraph_text(b)[:120].replace("\n", " ")
            elif btype == "title":
                info = get_title_info(b)
                preview = f"<H{info[1]}> {info[0]}" if info else "<title>"
            else:
                preview = f"<{btype}>"
            lines.append(f"[{name.upper()}] {preview}")
    (paper_out / "_debug.txt").write_text("\n".join(lines), encoding="utf-8")


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
    """Load v2 JSON, flatten pages into a single block list."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not raw:
        return []
    # v2 top-level is list of pages; each page is list of blocks
    if isinstance(raw[0], list):
        return flatten_pages(raw)
    # fallback: v1 flat structure
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
            sections = split_paper(blocks)
            write_section_files(paper_out, sections)
            write_debug(paper_out, sections)
            nonempty = sum(1 for v in sections.values() if v)
            log.info(f"  DONE: {nonempty} sections → {list(sections.keys())}")
            done += 1
        except Exception as e:
            log.exception(f"  FAILED: {paper_name} — {e}")
            failed += 1

    log.info(f"Summary: done={done} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()