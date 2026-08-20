"""
Paper-level synthesis processor.

Reads all section JSONs plus the critique JSON and produces a reader-facing
paper-level overview via split-by-category calls with sequential accumulation.

Each call receives the accumulated outputs of previous calls in its context,
so downstream synthesis is informed by upstream synthesis. This mirrors how
a scholar builds up understanding of a paper.

Call order:
  1. background_and_motivation
  2. theories_and_stance
  3. study_design
  4. findings_summary
  5. evidence_claim_alignment
  6. strengths_and_weaknesses
  7. key_references
  8. reading_recommendation
  9. executive_summary (runs LAST — uses all prior pieces as context)
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
from ..schemas.paper_synthesis import PaperSynthesis


logger = logging.getLogger(__name__)


_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_PROMPTS_DIR = Path(__file__).parent.parent / "prompts" / "paper_synthesis"

_JINJA_ENV = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)


# Call sequence. Executive summary runs after these, with the full accumulated
# synthesis as context.
SYNTHESIS_CALLS = [
    "background_and_motivation",
    "theories_and_stance",
    "study_design",
    "findings_summary",
    "evidence_claim_alignment",
    "strengths_and_weaknesses",
    "key_references",
    "reading_recommendation",
]


class PaperSynthesisProcessor:
    task_name = "paper_synthesis"
    output_stem = "paper_overview"

    def __init__(self, cfg: AppConfig, client: LLMClient) -> None:
        self.cfg = cfg
        self.client = client
        self.task_config = cfg.task(self.task_name)
        self.common_prompt = (_PROMPTS_DIR / "_common.txt").read_text(encoding="utf-8")

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def process(self, paper_name: str, *, force: bool = False) -> bool:
        """
        Produce paper-level synthesis via sequential accumulation.

        Each call receives the accumulated outputs of previous calls in its
        context, so downstream synthesis is informed by upstream synthesis.
        """
        json_path, md_path = output_paths(
            self.cfg,
            paper_name=paper_name,
            task_name=self.task_name,
            experiment=None,
            filename_override=self.output_stem,
        )

        if should_skip(json_path, force=force):
            logger.info(f"[skip cached] {paper_name}/paper_overview")
            return False

        logger.info(f"[process]     {paper_name}/paper_overview")

        base_content = self._gather_all_content(paper_name)
        if not base_content:
            logger.warning(
                f"No content found for '{paper_name}'; skipping synthesis."
            )
            return False

        synthesis_data: dict[str, Any] = {}
        total_tokens = 0

        # Sequential accumulation: each call sees prior synthesis outputs.
        for call_name in SYNTHESIS_CALLS:
            logger.info(f"[synthesis]   {paper_name}/{call_name}")
            call_content = self._build_call_content(base_content, synthesis_data)
            fragment, tokens = self._run_call(call_name, paper_name, call_content)
            synthesis_data.update(fragment)
            total_tokens += tokens

        # Executive summary runs last with the full accumulated synthesis.
        logger.info(f"[synthesis]   {paper_name}/executive_summary")
        exec_content = self._build_call_content(base_content, synthesis_data)
        fragment, tokens = self._run_call("executive_summary", paper_name, exec_content)
        synthesis_data.update(fragment)
        total_tokens += tokens

        # Validate the assembled synthesis.
        try:
            validated = PaperSynthesis.model_validate(synthesis_data)
        except ValidationError as e:
            raise RuntimeError(
                f"Synthesis schema validation failed for '{paper_name}':\n{e}"
            ) from e

        # Render markdown.
        template_render = _JINJA_ENV.get_template("paper_synthesis.md.j2")
        markdown = template_render.render(data=validated, paper_name=paper_name)

        # Atomic write.
        json_path.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(
            json_path,
            json.dumps(validated.model_dump(), indent=2, ensure_ascii=False) + "\n",
        )
        _atomic_write_text(md_path, markdown)

        logger.info(
            f"[done]        {paper_name}/paper_overview  total_tokens={total_tokens}"
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
            logger.info(f"[rerender skip] {paper_name}/paper_overview (no JSON yet)")
            return False

        raw = json.loads(json_path.read_text(encoding="utf-8"))
        validated = PaperSynthesis.model_validate(raw)
        template_render = _JINJA_ENV.get_template("paper_synthesis.md.j2")
        markdown = template_render.render(data=validated, paper_name=paper_name)

        md_path.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(md_path, markdown)
        logger.info(f"[rerendered]    {paper_name}/paper_overview")
        return True

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------

    def _run_call(
        self,
        call_name: str,
        paper_name: str,
        content: str,
    ) -> tuple[dict, int]:
        """Run one synthesis call. Returns (parsed_fragment, tokens_used)."""
        prompt_file = _PROMPTS_DIR / f"{call_name}.txt"
        call_prompt = prompt_file.read_text(encoding="utf-8")
        full_prompt = self.common_prompt + "\n\n" + call_prompt
        full_prompt = full_prompt.replace(
            "{paper_name}", paper_name
        ).replace(
            "{content}", content
        )

        response = self.client.complete_json(
            self.task_config,
            system_prompt=full_prompt,
            user_prompt="Return the JSON now.",
        )

        return response.parsed, response.total_tokens

    def _build_call_content(
        self,
        base_content: str,
        synthesis_so_far: dict[str, Any],
    ) -> str:
        """
        Assemble the content string for one call.

        Includes the base content (all section JSONs + critique + abstract)
        plus any synthesis pieces already produced by earlier calls.
        """
        if not synthesis_so_far:
            return base_content

        prior_synthesis = json.dumps(synthesis_so_far, indent=2, ensure_ascii=False)
        return (
            base_content
            + "\n\n---\n\n## SYNTHESIS PIECES COMPLETED SO FAR\n\n```json\n"
            + prior_synthesis
            + "\n```"
        )

    def _gather_all_content(self, paper_name: str) -> str:
        """Collect all section JSONs, abstract, and critique into one block."""
        base = paper_output_dir(self.cfg, paper_name)
        if not base.exists():
            return ""

        chunks: list[str] = []

        # Abstract — markdown, not JSON.
        abstract_path = base / "abstract.md"
        if abstract_path.exists():
            chunks.append("## ABSTRACT\n\n" + abstract_path.read_text(encoding="utf-8"))

        # Paper-level JSONs.
        for key, filename in [
            ("introduction", "introduction.json"),
            ("general_discussion", "general_discussion.json"),
            ("critique", "critique.json"),
        ]:
            path = base / filename
            if path.exists():
                chunks.append(
                    f"## PAPER-LEVEL {key.upper()}\n\n```json\n"
                    + path.read_text(encoding="utf-8")
                    + "\n```"
                )

        # Per-experiment JSONs.
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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Usage:
      uv run python -m scripts.section_summarizer.processors.paper_synthesis <paper> [--force] [--rerender]
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
            "paper_synthesis <paper_name> [--force] [--rerender]"
        )
        sys.exit(1)

    paper_name = args[0]
    cfg = load_config()
    client = LLMClient()
    processor = PaperSynthesisProcessor(cfg, client)

    if rerender_only:
        did = processor.rerender(paper_name)
    else:
        did = processor.process(paper_name, force=force)

    print(f"\nDone. Processed: {'yes' if did else 'skipped/no content'}")