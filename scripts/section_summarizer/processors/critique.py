"""
Paper-level critique processor.

Reads all section JSON extractions for a paper and produces a structured
critical evaluation across seven categories.

Split-by-category design: each category gets its own LLM call, bounded
in output size. Avoids truncation on long critiques and gives cleaner
per-category reasoning.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pydantic import ValidationError

from ..cache import should_skip
from ..config_loader import AppConfig
from ..io_utils import _atomic_write_text, output_paths, paper_output_dir
from ..llm_client import LLMClient
from ..schemas.critique import CritiqueEntry, CritiqueSummary


logger = logging.getLogger(__name__)


_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_PROMPTS_DIR = Path(__file__).parent.parent / "prompts" / "critique"

_JINJA_ENV = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)


# The seven category names, in the order they appear in the output.
CATEGORY_NAMES = [
    "design_theory_alignment",
    "evidence_theory_alignment",
    "internal_consistency",
    "alternative_accounts",
    "statistical_completeness",
    "methodological_concerns",
    "statistical_robustness",
]


class CritiqueProcessor:
    task_name = "critique"
    output_stem = "critique"

    def __init__(self, cfg: AppConfig, client: LLMClient) -> None:
        self.cfg = cfg
        self.client = client
        self.task_config = cfg.task(self.task_name)
        self.common_prompt = (_PROMPTS_DIR / "_common.txt").read_text(encoding="utf-8")

    def process(self, paper_name: str, *, force: bool = False) -> bool:
        """Produce paper-level critique via split-by-category calls."""
        json_path, md_path = output_paths(
            self.cfg,
            paper_name=paper_name,
            task_name=self.task_name,
            experiment=None,
            filename_override=self.output_stem,
        )

        if should_skip(json_path, force=force):
            logger.info(f"[skip cached] {paper_name}/critique")
            return False

        logger.info(f"[process]     {paper_name}/critique")

        section_content = self._gather_section_content(paper_name)
        if not section_content:
            logger.warning(
                f"No section content found for '{paper_name}'; skipping critique."
            )
            return False

        # Run one call per category.
        critique_data: dict[str, Any] = {}
        total_tokens = 0

        for category in CATEGORY_NAMES:
            logger.info(f"[category]    {paper_name}/{category}")
            entries, tokens = self._run_category_call(
                category, paper_name, section_content
            )
            critique_data[category] = entries
            total_tokens += tokens

        # Overall assessment call — feeds in the compiled concerns.
        logger.info(f"[category]    {paper_name}/overall_assessment")
        overall, tokens = self._run_overall_assessment_call(
            paper_name, critique_data
        )
        critique_data["overall_assessment"] = overall
        total_tokens += tokens

        # Validate against schema.
        try:
            validated = CritiqueSummary.model_validate(critique_data)
        except ValidationError as e:
            raise RuntimeError(
                f"Critique schema validation failed for '{paper_name}':\n{e}"
            ) from e

        # Render markdown.
        template_render = _JINJA_ENV.get_template("critique.md.j2")
        markdown = template_render.render(data=validated, paper_name=paper_name)

        json_path.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(
            json_path,
            json.dumps(validated.model_dump(), indent=2, ensure_ascii=False) + "\n",
        )
        _atomic_write_text(md_path, markdown)

        logger.info(
            f"[done]        {paper_name}/critique  total_tokens={total_tokens}"
        )
        return True

    def rerender(self, paper_name: str) -> bool:
        """Re-render markdown from existing JSON without calling the LLM."""
        json_path, md_path = output_paths(
            self.cfg,
            paper_name=paper_name,
            task_name=self.task_name,
            experiment=None,
            filename_override=self.output_stem,
        )
        if not json_path.exists():
            logger.info(f"[rerender skip] {paper_name}/critique (no JSON yet)")
            return False

        raw = json.loads(json_path.read_text(encoding="utf-8"))
        validated = CritiqueSummary.model_validate(raw)
        template_render = _JINJA_ENV.get_template("critique.md.j2")
        markdown = template_render.render(data=validated, paper_name=paper_name)

        md_path.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(md_path, markdown)
        logger.info(f"[rerendered]    {paper_name}/critique")
        return True

    # -- Per-category call -------------------------------------------------

    def _run_category_call(
        self,
        category: str,
        paper_name: str,
        section_content: str,
    ) -> tuple[list[dict], int]:
        """
        Run one LLM call for one category. Returns (entries, tokens_used).
        Returns empty list if the LLM produced no legitimate concerns.
        """
        category_prompt = (_PROMPTS_DIR / f"{category}.txt").read_text(encoding="utf-8")
        full_prompt = self.common_prompt + "\n\n" + category_prompt
        full_prompt = full_prompt.replace(
            "{paper_name}", paper_name
        ).replace(
            "{section_content}", section_content
        )

        response = self.client.complete_json(
            self.task_config,
            system_prompt=full_prompt,
            user_prompt="Return the JSON now.",
        )

        # The LLM returns {"<category>": [entries]}. Extract the array.
        parsed = response.parsed
        entries = parsed.get(category, [])
        if not isinstance(entries, list):
            logger.warning(
                f"Unexpected format for category '{category}': not a list. "
                f"Treating as empty."
            )
            entries = []

        # Validate each entry individually so we surface bad entries cleanly.
        validated_entries: list[dict] = []
        for i, entry in enumerate(entries):
            try:
                validated = CritiqueEntry.model_validate(entry)
                validated_entries.append(validated.model_dump())
            except ValidationError as e:
                logger.warning(
                    f"Skipping malformed entry {i} in '{category}': {e}"
                )

        return validated_entries, response.total_tokens

    # -- Overall assessment call ------------------------------------------

    def _run_overall_assessment_call(
        self,
        paper_name: str,
        critique_data: dict[str, list],
    ) -> tuple[str | None, int]:
        """Generate the overall_assessment string. Returns (text, tokens_used)."""
        # Compile the concerns into a compact string for the prompt.
        compiled = _compile_concerns(critique_data)
        if not compiled.strip():
            logger.info(
                f"No concerns identified; skipping overall_assessment call."
            )
            return None, 0

        prompt = (_PROMPTS_DIR / "overall_assessment.txt").read_text(encoding="utf-8")
        prompt = prompt.replace(
            "{paper_name}", paper_name
        ).replace(
            "{compiled_concerns}", compiled
        )

        response = self.client.complete_json(
            self.task_config,
            system_prompt=prompt,
            user_prompt="Return the JSON now.",
        )
        text = response.parsed.get("overall_assessment")
        return text, response.total_tokens

    # -- Gathering section content into a single string for the prompt ----

    def _gather_section_content(self, paper_name: str) -> str:
        """Collect all section JSONs (and abstract as text) into a single block."""
        base = paper_output_dir(self.cfg, paper_name)
        if not base.exists():
            return ""

        chunks: list[str] = []

        abstract_path = base / "abstract.md"
        if abstract_path.exists():
            chunks.append("## ABSTRACT\n\n" + abstract_path.read_text(encoding="utf-8"))

        for key, filename in [
            ("introduction", "introduction.json"),
            ("general_discussion", "general_discussion.json"),
        ]:
            path = base / filename
            if path.exists():
                chunks.append(
                    f"## PAPER-LEVEL {key.upper()}\n\n```json\n"
                    + path.read_text(encoding="utf-8")
                    + "\n```"
                )

        for exp_dir in sorted(
            p for p in base.iterdir() if p.is_dir() and p.name.startswith("exp_")
        ):
            exp_name = exp_dir.name
            for key, filename in [
                ("exp_introduction", "introduction.json"),
                ("methods", "methods.json"),
                ("results_and_discussion", "results_and_discussion.json"),
            ]:
                path = exp_dir / filename
                if path.exists():
                    chunks.append(
                        f"## {exp_name.upper()} — {key.upper()}\n\n```json\n"
                        + path.read_text(encoding="utf-8")
                        + "\n```"
                    )

        return "\n\n---\n\n".join(chunks)


def _compile_concerns(critique_data: dict[str, list]) -> str:
    """Compact serialization of category concerns for the overall assessment prompt."""
    lines: list[str] = []
    for category in CATEGORY_NAMES:
        entries = critique_data.get(category, [])
        if not entries:
            continue
        lines.append(f"## {category}")
        for e in entries:
            lines.append(
                f"- [{e.get('severity', '?')}] {e.get('concern', '')}"
            )
        lines.append("")
    return "\n".join(lines).strip()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Usage:
      uv run python -m scripts.section_summarizer.processors.critique <paper> [--force] [--rerender]
    """
    import sys

    from ..config_loader import load_config

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
            "critique <paper_name> [--force] [--rerender]"
        )
        sys.exit(1)

    paper_name = args[0]
    cfg = load_config()
    client = LLMClient()
    processor = CritiqueProcessor(cfg, client)

    if rerender_only:
        did = processor.rerender(paper_name)
    else:
        did = processor.process(paper_name, force=force)

    print(f"\nDone. Processed: {'yes' if did else 'skipped/no content'}")