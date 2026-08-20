"""
Copy abstract.md verbatim from sections_output/ to summaries_output/,
prepending a header noting it is preserved without summarization.

No LLM, no schema, no template. Abstracts are the authors' own distillation
and re-summarizing them would only lose information.

Usage:
  # Copy for one paper:
  uv run python -m scripts.section_summarizer.copy_abstracts "<paper_name>"

  # Copy for all papers with sections_output/:
  uv run python -m scripts.section_summarizer.copy_abstracts

  # Force overwrite existing outputs:
  uv run python -m scripts.section_summarizer.copy_abstracts --force
"""

from __future__ import annotations

import logging
import sys

from .config_loader import load_config, AppConfig
from .io_utils import list_papers, paper_input_dir, paper_output_dir


logger = logging.getLogger(__name__)

HEADER = "# Abstract (Verbatim)\n\n*Preserved from source without summarization.*\n\n"


def copy_abstract(cfg: AppConfig, paper_name: str, force: bool = False) -> bool:
    """
    Copy abstract.md for one paper, prepending the preservation header.

    Returns True if a copy was written, False if skipped (missing source
    or already cached).
    """
    src = paper_input_dir(cfg, paper_name) / "abstract.md"
    dst = paper_output_dir(cfg, paper_name) / "abstract.md"

    if not src.exists():
        logger.info(f"[skip missing] {paper_name}/abstract.md")
        return False
    if dst.exists() and not force:
        logger.info(f"[skip cached]  {paper_name}/abstract.md")
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)
    body = src.read_text(encoding="utf-8")
    dst.write_text(HEADER + body, encoding="utf-8")
    logger.info(f"[copied]       {paper_name}/abstract.md")
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    cfg = load_config()

    args = sys.argv[1:]
    force = "--force" in args
    paper_args = [a for a in args if a != "--force"]

    papers = paper_args if paper_args else list_papers(cfg)
    if not papers:
        print("No papers found in sections_output/.")
        sys.exit(0)

    copied = 0
    for p in papers:
        if copy_abstract(cfg, p, force=force):
            copied += 1
    print(f"\nDone. Copied: {copied} / {len(papers)}")