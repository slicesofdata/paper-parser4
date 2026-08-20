"""
Paper-level discussion processor.

Injects paper-level introduction context into the prompt so the LLM can
distinguish restatements of the intro's theoretical framework from
genuine refinements based on the results.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from ..config_loader import AppConfig
from ..io_utils import SectionFile, paper_output_dir
from ..llm_client import LLMClient
from ..schemas.discussion_paper import DiscussionPaperSummary
from .base import BaseProcessor


logger = logging.getLogger(__name__)


NO_PRIOR_CONTEXT_MESSAGE = (
    "(No paper-level introduction summary is available for this paper. "
    "Judge theoretical claims conservatively based only on the discussion text.)"
)


class DiscussionPaperProcessor(BaseProcessor):
    task_name = "discussion_paper"
    schema_cls = DiscussionPaperSummary
    prompt_filename = "discussion_paper.txt"
    template_filename = "discussion_paper.md.j2"
    output_stem = "general_discussion"

    def _build_prompts(self, section: SectionFile) -> tuple[str, str]:
        prior_context = self._load_prior_context(self.cfg, section.paper_name)

        prompt_path = Path(__file__).parent.parent / "prompts" / self.prompt_filename
        template = prompt_path.read_text(encoding="utf-8")

        section_location = section.experiment or "paper-level"
        replacements = {
            "{paper_name}": section.paper_name,
            "{section_location}": section_location,
            "{section_text}": section.content,
            "{prior_context}": prior_context,
        }
        filled = template
        for placeholder, value in replacements.items():
            filled = filled.replace(placeholder, value)

        return filled, "Return the JSON now."

    @staticmethod
    def _load_prior_context(cfg: AppConfig, paper_name: str) -> str:
        json_path = paper_output_dir(cfg, paper_name) / "introduction.json"
        if not json_path.exists():
            logger.warning(
                f"Paper-level introduction.json not found for '{paper_name}'; "
                f"proceeding without prior context."
            )
            return NO_PRIOR_CONTEXT_MESSAGE

        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(
                f"Failed to load prior context from {json_path}: {e}. "
                f"Proceeding without prior context."
            )
            return NO_PRIOR_CONTEXT_MESSAGE

        return _format_prior_context(data)


def _format_prior_context(intro_data: dict) -> str:
    lines: list[str] = []

    tf = intro_data.get("theoretical_framework") or []
    if tf:
        lines.append("Theoretical framework (already established):")
        for e in tf:
            # Support both new (topic_label) and legacy (statement) keys
            label = e.get("topic_label") or e.get("statement", "")
            label = label.strip()
            if label:
                lines.append(f"- {label}")
        lines.append("")

    hyp = intro_data.get("specific_hypotheses") or []
    if hyp:
        lines.append("Overarching hypotheses (already established):")
        for e in hyp:
            label = e.get("topic_label") or e.get("statement", "")
            label = label.strip()
            if label:
                lines.append(f"- {label}")
        lines.append("")

    mech = intro_data.get("mechanistic_claims") or []
    if mech:
        lines.append("Mechanistic claims (already established):")
        for e in mech:
            label = e.get("topic_label") or e.get("statement", "")
            label = label.strip()
            if label:
                lines.append(f"- {label}")
        lines.append("")

    alt = intro_data.get("alternative_theories") or []
    if alt:
        lines.append("Alternative theories already discussed at the paper level:")
        for a in alt:
            name = a.get("name", "").strip()
            desc = a.get("description", "").strip()
            if name:
                lines.append(f"- {name}: {desc}")
        lines.append("")

    if not lines:
        return NO_PRIOR_CONTEXT_MESSAGE

    return "\n".join(lines).strip()

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Usage:
      uv run python -m scripts.section_summarizer.processors.discussion_paper <paper> [--force] [--rerender]
    """
    import sys

    from ..config_loader import load_config
    from ..io_utils import discover_sections

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
            "discussion_paper <paper_name> [--force] [--rerender]"
        )
        sys.exit(1)

    paper_name = args[0]
    cfg = load_config()
    client = LLMClient()
    processor = DiscussionPaperProcessor(cfg, client)

    processed = 0
    skipped = 0
    for section in discover_sections(cfg, paper_name):
        if section.task_name != "discussion_paper":
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