"""
Post-process MinerU markdown output using the character normalization config.

Reads:  markdown_output/<paper>/auto/<paper>.md
Writes: normalized version back to the same file, with a backup at
        markdown_output/<paper>/auto/<paper>.md.original

Applies (in order):
  1. char_substitutions from config/char_normalization.yaml
  2. pattern_substitutions (regex)

Usage:
  # Process all papers
  uv run --no-sync python scripts/mineru_postprocess.py

  # Process one paper
  uv run --no-sync python scripts/mineru_postprocess.py "<paper_name>"

  # Dry run: show what would change without writing
  uv run --no-sync python scripts/mineru_postprocess.py --dry-run

  # Restore originals (revert normalization)
  uv run --no-sync python scripts/mineru_postprocess.py --restore
"""

from __future__ import annotations

import logging
import re
import shutil
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "markdown_output"
CONFIG_PATH = PROJECT_ROOT / "config" / "char_normalization.yaml"
LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "mineru_postprocess.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


def load_config() -> dict:
    """Load character normalization config."""
    if not CONFIG_PATH.exists():
        log.warning(f"Config missing at {CONFIG_PATH}; nothing to normalize.")
        return {"char_substitutions": {}, "pattern_substitutions": {}}
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return {
        "char_substitutions": data.get("char_substitutions") or {},
        "pattern_substitutions": data.get("pattern_substitutions") or {},
    }


def normalize_text(text: str, config: dict) -> tuple[str, dict]:
    """
    Apply all normalization rules to text.

    Returns (normalized_text, stats) where stats counts substitutions applied.
    """
    stats: dict[str, int] = {}
    result = text

    # Single-character substitutions first.
    for src, dst in config["char_substitutions"].items():
        count = result.count(src)
        if count > 0:
            result = result.replace(src, dst)
            stats[f"char {src!r} -> {dst!r}"] = count

    # Then regex pattern substitutions.
    # Use a lambda for replacement to treat it as literal, avoiding backslash
    # escape interpretation. This way config authors don't need to double-escape
    # backslashes in replacement values.
    for pattern, replacement in config["pattern_substitutions"].items():
        try:
            compiled = re.compile(pattern)
        except re.error as e:
            log.error(f"Invalid regex pattern in config: {pattern!r} — {e}")
            continue
        try:
            new_result, count = compiled.subn(lambda m: replacement, result)
        except re.error as e:
            log.error(
                f"Invalid replacement string in config for {pattern!r}: {e}"
            )
            continue
        if count > 0:
            result = new_result
            stats[f"pattern {pattern!r} -> {replacement!r}"] = count

    return result, stats


def find_markdown(paper_dir: Path) -> Path | None:
    """Locate the primary markdown file in <paper>/auto/."""
    auto_dir = paper_dir / "auto"
    if not auto_dir.exists():
        return None
    md_files = list(auto_dir.glob("*.md"))
    # Prefer one that matches the paper name.
    for md in md_files:
        if md.stem == paper_dir.name:
            return md
    return md_files[0] if md_files else None


def process_paper(paper_dir: Path, config: dict, *, dry_run: bool = False) -> bool:
    """Process one paper. Returns True if changes were made (or would be)."""
    md_file = find_markdown(paper_dir)
    if not md_file:
        log.warning(f"No markdown for: {paper_dir.name}")
        return False

    original_text = md_file.read_text(encoding="utf-8")
    normalized_text, stats = normalize_text(original_text, config)

    if original_text == normalized_text:
        log.info(f"NO CHANGE: {paper_dir.name}")
        return False

    total_subs = sum(stats.values())
    log.info(f"NORMALIZE: {paper_dir.name} ({total_subs} substitutions)")
    for rule, count in stats.items():
        log.info(f"    {count:5d} x {rule}")

    if dry_run:
        log.info("  (dry run — no files written)")
        return True

    # Write backup if not already present.
    backup_path = md_file.with_suffix(md_file.suffix + ".original")
    if not backup_path.exists():
        shutil.copy2(md_file, backup_path)
        log.info(f"  Backup: {backup_path.name}")

    # Write normalized version.
    md_file.write_text(normalized_text, encoding="utf-8")
    log.info(f"  Written: {md_file.name}")
    return True


def restore_paper(paper_dir: Path) -> bool:
    """Restore original markdown from backup. Returns True if restored."""
    md_file = find_markdown(paper_dir)
    if not md_file:
        return False
    backup_path = md_file.with_suffix(md_file.suffix + ".original")
    if not backup_path.exists():
        log.info(f"No backup for: {paper_dir.name}")
        return False
    shutil.copy2(backup_path, md_file)
    log.info(f"RESTORE: {paper_dir.name}")
    return True

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
    
def main() -> None:
    if not INPUT_DIR.exists():
        log.error(f"Input directory missing: {INPUT_DIR}")
        sys.exit(1)

    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    restore_mode = "--restore" in args
    paper_args = [a for a in args if a not in ("--dry-run", "--restore")]

    if paper_args:
        paper_dirs = [INPUT_DIR / name for name in paper_args]
        paper_dirs = [p for p in paper_dirs if p.is_dir()]
    else:
        paper_dirs = sorted(p for p in INPUT_DIR.iterdir() if p.is_dir())

    if not paper_dirs:
        log.info("No papers found.")
        return

    log.info(f"Processing {len(paper_dirs)} paper(s); dry_run={dry_run}, restore={restore_mode}")

    if restore_mode:
        n = sum(1 for p in paper_dirs if restore_paper(p))
        log.info(f"Restored: {n} / {len(paper_dirs)}")
        return

    config = load_config()
    changed = sum(1 for p in paper_dirs if process_paper(p, config, dry_run=dry_run))
    log.info(f"Changed: {changed} / {len(paper_dirs)}")


if __name__ == "__main__":
    main()