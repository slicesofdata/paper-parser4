"""Results and Discussion section processor."""

from __future__ import annotations

from ..schemas.results_and_discussion import ResultsAndDiscussionSummary
from .base import BaseProcessor


class ResultsAndDiscussionProcessor(BaseProcessor):
    task_name = "results_and_discussion"
    schema_cls = ResultsAndDiscussionSummary
    prompt_filename = "results_and_discussion.txt"
    template_filename = "results_and_discussion.md.j2"
    output_stem = "results_and_discussion"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Usage:
      uv run python -m scripts.section_summarizer.processors.results_and_discussion <paper> [--force] [--rerender]
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
            "Usage: uv run python -m scripts.section_summarizer.processors."
            "results_and_discussion <paper_name> [--force] [--rerender]"
        )
        sys.exit(1)

    paper_name = args[0]
    cfg = load_config()
    client = LLMClient()
    processor = ResultsAndDiscussionProcessor(cfg, client)

    processed = 0
    skipped = 0
    for section in discover_sections(cfg, paper_name):
        if section.task_name != "results_and_discussion":
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
