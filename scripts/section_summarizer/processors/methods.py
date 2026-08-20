"""Methods section processor."""

from __future__ import annotations

from ..schemas.methods import MethodsSummary
from .base import BaseProcessor


class MethodsProcessor(BaseProcessor):
    task_name = "methods"
    schema_cls = MethodsSummary
    prompt_filename = "methods.txt"
    template_filename = "methods.md.j2"
    output_stem = "methods"


# ---------------------------------------------------------------------------
# CLI: process methods sections for one paper
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Usage:
      uv run python -m scripts.section_summarizer.processors.methods <paper> [--force] [--rerender]

    Modes:
      (default)   Process methods sections; skip if cached.
      --force     Reprocess even if cached (calls LLM again).
      --rerender  Skip LLM; re-render markdown from existing JSON only.
    """
    import logging
    import sys

    from ..config_loader import load_config
    from ..io_utils import discover_sections
    from ..llm_client import LLMClient

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    args = sys.argv[1:]
    force = "--force" in args
    rerender_only = "--rerender" in args
    args = [a for a in args if a not in ("--force", "--rerender")]

    if not args:
        print(
            "Usage: uv run python -m scripts.section_summarizer.processors.methods "
            "<paper_name> [--force] [--rerender]"
        )
        sys.exit(1)

    paper_name = args[0]
    cfg = load_config()
    client = LLMClient()
    processor = MethodsProcessor(cfg, client)

    processed = 0
    skipped = 0
    for section in discover_sections(cfg, paper_name):
        if section.task_name != "methods":
            continue
        if rerender_only:
            did_work = processor.rerender(section)
        else:
            did_work = processor.process(section, force=force)
        if did_work:
            processed += 1
        else:
            skipped += 1

    verb = "Rerendered" if rerender_only else "Processed"
    print(f"\nDone. {verb}: {processed}, Skipped: {skipped}")
