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

# Elsevier and similar publishers append a copyright line to the abstract body.
# Strip these trailers so downstream consumers see clean abstract text.
_ABSTRACT_TRAILER_PATTERNS = [
    # "\- 2014 Elsevier Inc. All rights reserved." with escaped hyphen
    re.compile(
        r"\n+\\?[-\u2010-\u2015]?\s*\d{4}\s+[^\n]*?\.\s*All rights reserved\.\s*$",
        re.IGNORECASE
    ),
    # "© 2014 Elsevier Inc. All rights reserved."
    re.compile(
        r"\n+©\s*\d{4}[^\n]*?\.\s*All rights reserved\.\s*$",
        re.IGNORECASE
    ),
    # "Published by Elsevier" variants
    re.compile(r"\n+Published by\s+[^\n]+\s*\.\s*$", re.IGNORECASE),
]


def _strip_abstract_trailer(text: str) -> str:
    """Remove publisher copyright trailers from the abstract body."""
    result = text
    for pattern in _ABSTRACT_TRAILER_PATTERNS:
        result = pattern.sub("", result)
    return result.strip()

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
    """
    Detect an author-list paragraph.

    Positive signals:
    - Contains institution keywords (university, department, etc.)
    - Short paragraph (< 100 chars)
    - Multiple <sup> tags (affiliation footnote markers)
    - Corresponding-author marker (⇑ or †)
    - Comma-separated list of name-like segments
    """
    lower = text.lower()
    if any(kw in lower for kw in INSTITUTION_KEYWORDS):
        return True
    if len(text) < 100:
        return True
    if text.count("<sup>") >= 2:
        return True
    if "⇑" in text or "†" in text:
        return True
    # Comma-separated list of segments that look like personal names.
    segments = [s.strip() for s in re.split(r"[,;]", text) if s.strip()]
    if len(segments) >= 3:
        name_like = sum(
            1 for s in segments
            if re.match(r"^[A-Z]\.\s*[A-Z]", s)      # "J. Smith"
            or re.match(r"^[A-Z][a-z]+\s+[A-Z]", s)  # "John Smith"
        )
        if name_like >= 2:
            return True
    return False


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


# ---- Paper parsing ----

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
    parsed, routing_log = parse_paper(raw_sections)
    write_paper(paper_out, parsed)
    write_debug(paper_out, parsed, raw_sections, routing_log)
    n_exp = len(parsed["experiments"])
    log.info(f"  DONE: {n_exp} experiment(s) -> {list(parsed['experiments'].keys())}")
    return True

def parse_paper(sections: list[tuple[int, str, str]]) -> tuple[dict, list[dict]]:
    """
    Route each (level, heading, body) tuple into the paper structure.

    Returns (parsed_paper, routing_log) where routing_log records the
    routing decision for each heading:
        [{"pos": 1, "level": 2, "heading": "...", "dest": "frontmatter.introduction",
          "reason": "matched canonical", "flag": ""}, ...]

    The `flag` field is "ROUTED-UNMATCHED" for unmatched headings that were
    routed into a canonical bucket via context inference (rather than
    matched by name). Useful for auditing across a corpus.
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

    routing_log: list[dict] = []

    stage = "prelude"
    current_experiment = None
    current_section = None
    pending_body_paras: list[str] = []

    def log_route(pos: int, level: int, heading: str, dest: str,
                  reason: str, flag: str = "") -> None:
        routing_log.append({
            "pos": pos,
            "level": level,
            "heading": heading,
            "dest": dest,
            "reason": reason,
            "flag": flag,
        })

    def append(bucket_dict: dict, key: str, heading: str, body: str, level: int = 2):
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

    for pos, (level, heading, body) in enumerate(sections, start=1):

        if level == 0:
            if body:
                result["backmatter"]["unmatched"] += body + "\n\n"
                log_route(pos, level, "(pre-title body)",
                          "backmatter.unmatched", "content before any heading")
            continue

        if level == 1:
            result["frontmatter"]["title"] = heading
            log_route(pos, level, heading, "frontmatter.title",
                      "H1 = paper title")
            if body:
                paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
                for p in paragraphs:
                    if looks_like_author_block(p):
                        existing = result["frontmatter"]["authors"]
                        result["frontmatter"]["authors"] = (
                            existing + "\n\n" + p if existing else p
                        )
                    else:
                        pending_body_paras.append(p)
            stage = "post_title"
            continue

        heading_text = heading
        is_exp, exp_label = is_experiment_heading(heading_text)
        if is_exp:
            current_experiment = exp_label
            current_section = "introduction"
            ensure_exp(exp_label)
            append(result["experiments"][exp_label], "introduction",
                   heading_text, body, level)
            log_route(pos, level, heading_text,
                      f"experiments.{exp_label}.introduction",
                      "experiment heading matched")
            stage = "in_experiment"
            continue

        section_type = classify_section(heading_text)

        if section_type == "article_info":
            append(result["frontmatter"], "article_info", heading_text, body, level)
            log_route(pos, level, heading_text, "frontmatter.article_info",
                      "matched canonical (article_info)")
            stage = "article_info"
            if body:
                for line in body.splitlines():
                    if re.match(r"^\s*key\s*words?\s*[:\-]", line, re.IGNORECASE):
                        existing = result["frontmatter"]["keywords"]
                        result["frontmatter"]["keywords"] = (
                            existing + "\n" + line if existing else line
                        )
            continue

        if section_type == "abstract":
            if body:
                result["frontmatter"]["abstract"] = _strip_abstract_trailer(body)
            log_route(pos, level, heading_text, "frontmatter.abstract",
                      "matched canonical (abstract)")
            pending_body_paras.clear()
            stage = "post_abstract"
            continue

        if section_type == "introduction":
            append(result["frontmatter"], "introduction", heading_text, body, level)
            log_route(pos, level, heading_text, "frontmatter.introduction",
                      "matched canonical (introduction)")
            stage = "extended_intro"
            current_experiment = None
            current_section = None
            continue

        if section_type in ("general_discussion", "references",
                            "acknowledgments", "conclusion", "appendix"):
            append(result["backmatter"], section_type, heading_text, body, level)
            log_route(pos, level, heading_text, f"backmatter.{section_type}",
                      f"matched canonical ({section_type})")
            current_experiment = None
            current_section = section_type
            stage = "in_backmatter"
            continue

        if section_type in ("methods", "results", "discussion", "results_and_discussion"):
            if current_experiment is None:
                current_experiment = "exp_1"
                ensure_exp(current_experiment)
                log_route(pos, level, heading_text,
                          f"experiments.{current_experiment}.{section_type}",
                          f"matched canonical ({section_type}); auto-created exp_1 (single-experiment paper)")
            else:
                log_route(pos, level, heading_text,
                          f"experiments.{current_experiment}.{section_type}",
                          f"matched canonical ({section_type})")
            current_section = section_type
            append(result["experiments"][current_experiment], section_type,
                   heading_text, body, level)
            stage = "in_experiment"
            continue

        # ---- Unmatched heading: route by current stage ----
        if stage == "in_experiment" and current_experiment and current_section:
            append(result["experiments"][current_experiment], current_section,
                   heading_text, body, level)
            log_route(pos, level, heading_text,
                      f"experiments.{current_experiment}.{current_section}",
                      f"unmatched; merged into current experiment section",
                      flag="ROUTED-UNMATCHED")
        elif stage == "in_backmatter" and current_section:
            append(result["backmatter"], current_section, heading_text, body, level)
            log_route(pos, level, heading_text,
                      f"backmatter.{current_section}",
                      "unmatched; merged into current backmatter section",
                      flag="ROUTED-UNMATCHED")
        elif stage in ("extended_intro", "post_abstract", "post_title", "article_info"):
            append(result["frontmatter"], "introduction", heading_text, body, level)
            log_route(pos, level, heading_text, "frontmatter.introduction",
                      "unmatched; merged into introduction (pre-experiment stage)",
                      flag="ROUTED-UNMATCHED")
            stage = "extended_intro"
        else:
            append(result["backmatter"], "unmatched", heading_text, body, level)
            log_route(pos, level, heading_text, "backmatter.unmatched",
                      f"unmatched; no context (stage={stage})",
                      flag="ROUTED-UNMATCHED")

    # Fallback: promote pending body content if no explicit abstract found.
    if pending_body_paras:
        if not result["frontmatter"]["abstract"].strip():
            result["frontmatter"]["abstract"] = pending_body_paras[0]
            remaining = pending_body_paras[1:]
            if remaining:
                new_intro = "\n\n".join(remaining)
                existing_intro = result["frontmatter"]["introduction"]
                result["frontmatter"]["introduction"] = (
                    existing_intro + "\n\n" + new_intro
                    if existing_intro else new_intro
                )
        else:
            pending_text = "\n\n".join(pending_body_paras)
            existing = result["backmatter"]["unmatched"]
            result["backmatter"]["unmatched"] = (
                existing + "\n\n" + pending_text if existing else pending_text
            )

    return result, routing_log

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


def write_debug(paper_out: Path, parsed: dict, raw_sections: list,
                routing_log: list[dict]):
    lines = []

    lines.append("=" * 78)
    lines.append("HEADING SCAN (raw)")
    lines.append("=" * 78)
    for level, heading, body in raw_sections:
        if heading:
            preview = body[:80].replace("\n", " ") if body else ""
            lines.append(f"  H{level}: {heading!r}  body:{preview!r}")
        else:
            preview = body[:80].replace("\n", " ") if body else ""
            lines.append(f"  L{level} (no heading)  body:{preview!r}")

    lines.append("")
    lines.append("=" * 78)
    lines.append("ROUTING DECISIONS")
    lines.append("=" * 78)
    for entry in routing_log:
        flag_str = f"  [{entry['flag']}]" if entry['flag'] else ""
        lines.append(
            f"  POS {entry['pos']:02d} | H{entry['level']}: {entry['heading']!r}"
            f"\n         -> {entry['dest']}  ({entry['reason']}){flag_str}"
        )

    lines.append("")
    lines.append("=" * 78)
    lines.append("FRONTMATTER SUMMARY")
    lines.append("=" * 78)
    for name, text in parsed["frontmatter"].items():
        if text.strip():
            preview = text[:150].replace("\n", " ")
            lines.append(f"  [{name}] {preview}")

    for exp_label, sections in parsed["experiments"].items():
        lines.append("")
        lines.append(f"=== {exp_label.upper()} ===")
        for name, text in sections.items():
            if text.strip():
                preview = text[:150].replace("\n", " ")
                lines.append(f"  [{name}] {preview}")

    lines.append("")
    lines.append("=== BACKMATTER ===")
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
            parsed, routing_log = parse_paper(raw_sections)
            write_paper(paper_out, parsed)
            write_debug(paper_out, parsed, raw_sections, routing_log)
            n_exp = len(parsed["experiments"])
            log.info(f"  DONE: {n_exp} experiment(s) → {list(parsed['experiments'].keys())}")
            done += 1
        except Exception as e:
            log.exception(f"  FAILED: {paper_name} — {e}")
            failed += 1

    log.info(f"Summary: done={done} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()