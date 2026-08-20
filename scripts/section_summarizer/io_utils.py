"""
File I/O utilities for section_summarizer.

Responsibilities:
  - Discover section files produced by split_sections.py for a given paper.
  - Read section markdown content.
  - Write per-section JSON outputs (canonical data) and rendered markdown
    (human-readable) to summaries_output/<paper>/[exp_N/]<section>.{json,md}.
  - Provide a consistent path scheme used by processors and the cache.

Directory conventions (input side, from stage 2):
  sections_output/<paper>/
      abstract.md
      introduction.md              (paper-level)
      general_discussion.md        (paper-level, may be absent)
      exp_1/
          introduction.md          (per-experiment)
          methods.md
          results_and_discussion.md
      exp_2/
          ...

Directory conventions (output side, this stage):
  summaries_output/<paper>/
      abstract.json / abstract.md
      introduction.json / introduction.md
      general_discussion.json / general_discussion.md
      critique.json / critique.md
      paper_overview.json / paper_overview.md
      exp_1/
          introduction.json / introduction.md
          methods.json / methods.md
          results_and_discussion.json / results_and_discussion.md
      exp_2/
          ...

Design notes:
  - All paths are absolute Path objects, derived from AppConfig.project_root.
  - Reads are UTF-8 with strict decoding (we produced these files, so failures
    signal a real problem).
  - Writes are atomic: write to <target>.tmp, fsync, then rename.
  - Empty section files are treated as "missing" — callers can skip them.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from .config_loader import AppConfig


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SECTIONS_INPUT_DIR   = "sections_output"
SUMMARIES_OUTPUT_DIR = "summaries_output"

# Regex for canonical experiment folder names (exp_1, exp_2a, exp_3a_and_3b, ...)
EXP_DIR_PATTERN = re.compile(r"^exp_[0-9a-z_]+$", re.IGNORECASE)

# Paper-level section file names we care about (input side).
PAPER_LEVEL_INPUTS = {
    "abstract":            "abstract.md",
    "introduction_paper":  "introduction.md",
    "discussion_paper":    "general_discussion.md",
}

# Per-experiment section file names (input side).
EXPERIMENT_LEVEL_INPUTS = {
    "introduction_experiment": "introduction.md",
    "methods":                 "methods.md",
    "results_and_discussion":  "results_and_discussion.md",
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SectionFile:
    """A single input markdown section discovered on disk."""
    paper_name: str
    task_name: str              # e.g. 'methods', 'introduction_paper'
    experiment: str | None      # e.g. 'exp_1' or None for paper-level
    input_path: Path            # absolute path to the .md file
    content: str                # UTF-8 text content, already read

    @property
    def is_experiment_level(self) -> bool:
        return self.experiment is not None

    @property
    def short_id(self) -> str:
        """Human-friendly identifier used in logs, e.g. 'paper/exp_1/methods'."""
        if self.experiment:
            return f"{self.paper_name}/{self.experiment}/{self.task_name}"
        return f"{self.paper_name}/{self.task_name}"


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def sections_input_root(cfg: AppConfig) -> Path:
    return cfg.project_root / SECTIONS_INPUT_DIR


def summaries_output_root(cfg: AppConfig) -> Path:
    return cfg.project_root / SUMMARIES_OUTPUT_DIR


def paper_input_dir(cfg: AppConfig, paper_name: str) -> Path:
    return sections_input_root(cfg) / paper_name


def paper_output_dir(cfg: AppConfig, paper_name: str) -> Path:
    return summaries_output_root(cfg) / paper_name


def output_paths(
    cfg: AppConfig,
    paper_name: str,
    task_name: str,
    experiment: str | None = None,
    filename_override: str | None = None,
) -> tuple[Path, Path]:
    """
    Return the (json_path, md_path) pair for a given output.

    - Paper-level outputs go to summaries_output/<paper>/<task>.{json,md}
    - Experiment-level outputs go to summaries_output/<paper>/<exp>/<task>.{json,md}

    `filename_override` lets processors write to a name that differs from the
    task name (e.g. task='introduction_paper' → filename 'introduction').
    """
    stem = filename_override or task_name
    base = paper_output_dir(cfg, paper_name)
    if experiment:
        base = base / experiment
    return (base / f"{stem}.json", base / f"{stem}.md")


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def list_papers(cfg: AppConfig) -> list[str]:
    """Return sorted list of paper directory names in sections_output/."""
    root = sections_input_root(cfg)
    if not root.exists():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir())


def list_experiments(cfg: AppConfig, paper_name: str) -> list[str]:
    """Return sorted list of exp_* subdirectories for a paper."""
    root = paper_input_dir(cfg, paper_name)
    if not root.exists():
        return []
    return sorted(
        p.name for p in root.iterdir()
        if p.is_dir() and EXP_DIR_PATTERN.match(p.name)
    )


def discover_sections(cfg: AppConfig, paper_name: str) -> Iterator[SectionFile]:
    """
    Yield every SectionFile that exists on disk for the given paper.

    Missing files are silently skipped — the pipeline processes what exists.
    Empty files are also skipped (with a warning).
    """
    paper_root = paper_input_dir(cfg, paper_name)
    if not paper_root.exists():
        logger.warning(f"Paper input dir missing: {paper_root}")
        return

    # Paper-level sections.
    for task_name, filename in PAPER_LEVEL_INPUTS.items():
        path = paper_root / filename
        section = _try_read_section(paper_name, task_name, None, path)
        if section is not None:
            yield section

    # Per-experiment sections.
    for exp in list_experiments(cfg, paper_name):
        exp_root = paper_root / exp
        for task_name, filename in EXPERIMENT_LEVEL_INPUTS.items():
            path = exp_root / filename
            section = _try_read_section(paper_name, task_name, exp, path)
            if section is not None:
                yield section


# Minimum content length for a section to be considered worth processing.
# Files shorter than this are almost certainly splitter artifacts
# (orphan headings, stray sentences) rather than real content.
MIN_SECTION_CHARS = 100

# ---------------------------------------------------------------------------
# Text sanitization for MinerU/OCR artifacts
# ---------------------------------------------------------------------------
# Sanitization is applied on read to all section content so downstream
# processors (LLM calls, template rendering) see cleaner text. Not a
# violation of "verbatim to authors' writing" — these are extraction
# artifacts, not the authors' own typography.
#
# TODO: When split_sections.py is refactored, move sanitization upstream
# so raw section files on disk are already clean.

# Non-printable control characters (except tab, newline, carriage return).
# These occasionally leak in from PDF extraction and can cause LLM
# generation loops or JSON parse failures.
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")

# Match a space that sits between two "numeric-ish" characters
# (digits, dots, commas, parens). MinerU renders letter-spaced typography
# (common in Elsevier statistical reports) as "F ( 1 , 6 7 ) = 3 1 . 9 7 2".
# Collapsing these spaces reverts to normal "F(1,67) = 31.972".
_LETTER_SPACED_NUM_RE = re.compile(r"(?<=[\d(.,])\s(?=[\d).,])")

# LaTeX math-mode delimiters that MinerU sometimes inserts mid-expression
# when a statistical formula spans a PDF line break.
_LATEX_MATH_DELIMS_RE = re.compile(r"\$")

# LaTeX size modifiers on parentheses/brackets/braces
# (\big, \Big, \bigg, \Bigg, \left, \right followed by a bracketing char).
# Safe to strip — they're formatting only.
_LATEX_SIZE_MODIFIERS_RE = re.compile(
    r"\\(?:big|Big|bigg|Bigg|left|right)\s*(?=[()\[\]{}|])"
)

# LaTeX text-in-math wrappers: \mathrm{X}, \mathsf{X}, \mathit{X}, etc.
# Common for MinerU rendering plain identifiers inside math mode
# (e.g., \mathsf{WF} for the variable name WF). Unwrap the content.
_LATEX_TEXT_WRAPPERS_RE = re.compile(
    r"\\math(?:rm|sf|it|bf|tt|cal|frak|scr)\s*\{([^}]*)\}"
)


def _strip_control_chars(text: str) -> str:
    """Remove non-printable control characters from extracted text."""
    return _CONTROL_CHAR_RE.sub("", text)


def _collapse_letter_spaced_numerics(text: str) -> str:
    """
    Collapse single spaces between digits/decimals/commas/parens that appear
    to be OCR artifacts of letter-spaced typography.

    Example:
      Before: 'F ( 1 , 6 7 ) = 3 1 . 9 7 2 , p < . 0 0 1'
      After:  'F(1,67) = 31.972, p < .001'

    Iterative: sequences like '3 1 . 9 7 2' need multiple passes to fully
    close up. Bounded for safety.
    """
    prev = None
    result = text
    for _ in range(10):
        if prev == result:
            break
        prev = result
        result = _LETTER_SPACED_NUM_RE.sub("", result)
    return result


def _sanitize_section_content(text: str) -> str:
    r"""
    Apply all cleanup passes for text produced by MinerU / PDF extraction.

    Order matters:
      1. Strip control chars first — they can otherwise confuse later regexes.
      2. Unwrap \mathrm{X}, \mathsf{X}, etc. so the plain identifiers
         participate in later cleanup.
      3. Strip LaTeX size modifiers (\big, \left, etc.).
      4. Strip stray $ math-mode delimiters.
      5. Collapse letter-spaced numerics last, once other noise is gone.
    """
    text = _strip_control_chars(text)
    text = _LATEX_TEXT_WRAPPERS_RE.sub(r"\1", text)
    text = _LATEX_SIZE_MODIFIERS_RE.sub("", text)
    text = _LATEX_MATH_DELIMS_RE.sub("", text)
    text = _collapse_letter_spaced_numerics(text)
    return text


def _try_read_section(
    paper_name: str,
    task_name: str,
    experiment: str | None,
    path: Path,
) -> SectionFile | None:
    """Read a section file if it exists and has non-trivial content."""
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8")
    content = _sanitize_section_content(raw).strip()
    if not content:
        logger.warning(f"Empty section file skipped: {path}")
        return None
    if len(content) < MIN_SECTION_CHARS:
        logger.warning(
            f"Section too short ({len(content)} chars < {MIN_SECTION_CHARS}), "
            f"skipping: {path}"
        )
        return None
    return SectionFile(
        paper_name=paper_name,
        task_name=task_name,
        experiment=experiment,
        input_path=path,
        content=content,
    )

def _try_read_section_old(
    paper_name: str,
    task_name: str,
    experiment: str | None,
    path: Path,
) -> SectionFile | None:
    """Read a section file if it exists and has non-trivial content."""
    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        logger.warning(f"Empty section file skipped: {path}")
        return None
    if len(content) < MIN_SECTION_CHARS:
        logger.warning(
            f"Section too short ({len(content)} chars < {MIN_SECTION_CHARS}), "
            f"skipping: {path}"
        )
        return None
    return SectionFile(
        paper_name=paper_name,
        task_name=task_name,
        experiment=experiment,
        input_path=path,
        content=content,
    )


# ---------------------------------------------------------------------------
# Writes
# ---------------------------------------------------------------------------

def write_output(
    json_path: Path,
    md_path: Path,
    json_data: dict,
    md_content: str,
) -> None:
    """
    Write both JSON and markdown outputs atomically.

    Creates parent directories as needed. Uses write-to-temp-then-rename so
    partial writes never leave a corrupted file on disk.
    """
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    _atomic_write_text(
        json_path,
        json.dumps(json_data, indent=2, ensure_ascii=False) + "\n",
    )
    _atomic_write_text(md_path, md_content)


def _atomic_write_text(path: Path, content: str) -> None:
    """Write text to `path` atomically via a .tmp file + rename."""
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    tmp_path.replace(path)


# ---------------------------------------------------------------------------
# CLI: preview what would be processed for a given paper
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Usage:
      uv run python -m scripts.section_summarizer.io_utils                 # list papers
      uv run python -m scripts.section_summarizer.io_utils <paper_name>    # list sections
    """
    import sys

    from .config_loader import load_config

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    cfg = load_config()

    if len(sys.argv) == 1:
        papers = list_papers(cfg)
        print(f"Found {len(papers)} papers in {sections_input_root(cfg)}:")
        for p in papers:
            exps = list_experiments(cfg, p)
            print(f"  - {p}  ({len(exps)} experiments)")
    else:
        paper = sys.argv[1]
        print(f"Sections discovered for '{paper}':\n")
        count = 0
        for sec in discover_sections(cfg, paper):
            count += 1
            print(
                f"  [{count:2d}] {sec.short_id:60s}  "
                f"({len(sec.content):6d} chars)"
            )
        if count == 0:
            print("  (none)")