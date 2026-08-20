"""
Cache / resume logic for section_summarizer.

The pipeline is expensive (LLM calls) and long-running (many papers, many
sections each). We want re-runs to skip anything already completed and only
process what's missing or explicitly invalidated.

Design:
  - Output existence IS the cache. If summaries_output/<paper>/<...>.json
    exists and is non-empty and valid JSON, we consider the section done.
  - No separate cache database, no hashing of inputs. Simple, transparent,
    inspectable via `ls`.
  - Callers can force reprocessing by passing force=True or by deleting
    the output file(s).

What we deliberately do NOT do (for now):
  - Input-hash-based invalidation. If you change split_sections.py and
    regenerate a section, the old summary will still be considered valid.
    Trade-off: simplicity vs. correctness. Acceptable because the user
    can always `rm -rf summaries_output/<paper>/` to force a full rerun.
  - Schema-version tracking. If we change a schema, old outputs may not
    match. Same mitigation.

Public API:
  - is_cached(json_path)              -> bool
  - should_skip(json_path, force)     -> bool
  - invalidate(json_path, md_path)    -> None  (delete outputs)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def is_cached(json_path: Path) -> bool:
    """
    Return True if the JSON output at `json_path` exists and looks valid.

    "Valid" here means: file exists, is non-empty, and parses as JSON.
    A corrupt or truncated file (e.g. from a killed process) is treated
    as not cached, so the next run will regenerate it.
    """
    if not json_path.exists():
        return False
    if json_path.stat().st_size == 0:
        logger.warning(f"Cached JSON is empty, treating as missing: {json_path}")
        return False
    try:
        with json_path.open("r", encoding="utf-8") as f:
            json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(
            f"Cached JSON is corrupt ({type(e).__name__}), treating as missing: "
            f"{json_path}"
        )
        return False
    return True


def should_skip(json_path: Path, force: bool = False) -> bool:
    """
    Decide whether a processor should skip its work.

    Parameters
    ----------
    json_path : Path to the primary output (the .json file).
    force     : If True, always process regardless of cache state.

    Returns
    -------
    True if the caller should skip; False if it should process.
    """
    if force:
        return False
    return is_cached(json_path)


def invalidate(json_path: Path, md_path: Path | None = None) -> None:
    """
    Delete cached outputs for a section so the next run will regenerate.

    Safe to call even if the files do not exist.
    """
    for p in (json_path, md_path):
        if p is None:
            continue
        try:
            p.unlink()
            logger.info(f"Invalidated cache: {p}")
        except FileNotFoundError:
            pass
        except OSError as e:
            logger.warning(f"Failed to invalidate {p}: {e}")


# ---------------------------------------------------------------------------
# CLI: inspect and manage the cache
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Usage:
      uv run python -m scripts.section_summarizer.cache                       # summary
      uv run python -m scripts.section_summarizer.cache <paper_name>          # detail
      uv run python -m scripts.section_summarizer.cache <paper_name> --clear  # invalidate
    """
    import sys

    from .config_loader import load_config
    from .io_utils import (
        list_papers,
        paper_output_dir,
        summaries_output_root,
    )

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    cfg = load_config()

    args = sys.argv[1:]
    clear = "--clear" in args
    args = [a for a in args if a != "--clear"]

    if not args:
        # Summary across all papers.
        root = summaries_output_root(cfg)
        papers = list_papers(cfg)
        print(f"Cache summary ({root}):\n")
        if not root.exists():
            print("  (no summaries_output/ directory yet)")
        else:
            for p in papers:
                out_dir = paper_output_dir(cfg, p)
                if not out_dir.exists():
                    print(f"  {p}: (not started)")
                    continue
                json_files = list(out_dir.rglob("*.json"))
                valid = sum(1 for j in json_files if is_cached(j))
                print(f"  {p}: {valid}/{len(json_files)} valid cached outputs")
    else:
        paper = args[0]
        out_dir = paper_output_dir(cfg, paper)
        if not out_dir.exists():
            print(f"No output directory for '{paper}' at {out_dir}")
            sys.exit(0)

        json_files = sorted(out_dir.rglob("*.json"))
        print(f"Cached outputs for '{paper}' ({len(json_files)} files):\n")
        for j in json_files:
            status = "VALID" if is_cached(j) else "INVALID"
            rel = j.relative_to(out_dir)
            print(f"  [{status}] {rel}")
            if clear:
                md = j.with_suffix(".md")
                invalidate(j, md)
        if clear:
            print(f"\nCleared cache for '{paper}'.")
            