"""
Base class for section processors.

Each concrete processor (methods, introduction_paper, etc.) inherits from
BaseProcessor and provides:
  - task_name (str): the key in models.yaml
  - schema_cls (Pydantic model): validates the LLM's JSON output
  - prompt_filename (str): under prompts/
  - template_filename (str): under templates/
  - output_stem (str): the filename stem (without extension) for outputs
  
The base handles the common flow:
  read section -> load prompt -> call LLM -> validate -> render md -> write.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import ClassVar, Type

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pydantic import BaseModel, ValidationError

from ..config_loader import AppConfig, TaskConfig
from ..io_utils import SectionFile, output_paths, write_output
from ..cache import should_skip
from ..llm_client import LLMClient, LLMResponse


logger = logging.getLogger(__name__)


# Module-level Jinja2 environment. Templates live in ../templates.
_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_JINJA_ENV = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)


class ProcessorError(RuntimeError):
    pass


class BaseProcessor:
    """Abstract base for section processors. Subclass and set the ClassVars."""

    # -- Subclass configuration --------------------------------------------
    task_name: ClassVar[str]              # must match a key in models.yaml
    schema_cls: ClassVar[Type[BaseModel]] # pydantic model for output
    prompt_filename: ClassVar[str]        # e.g. "methods.txt"
    template_filename: ClassVar[str]      # e.g. "methods.md.j2"
    output_stem: ClassVar[str]            # e.g. "methods" -> methods.{json,md}

    # -- Constructor -------------------------------------------------------

    def __init__(self, cfg: AppConfig, client: LLMClient) -> None:
        self.cfg = cfg
        self.client = client
        self.task_config: TaskConfig = cfg.task(self.task_name)

    # -- Public API --------------------------------------------------------

    def process(self, section: SectionFile, *, force: bool = False) -> bool:
        """
        Process a single SectionFile.

        Returns True if work was performed, False if skipped due to cache.
        """
        json_path, md_path = output_paths(
            self.cfg,
            paper_name=section.paper_name,
            task_name=self.task_name,
            experiment=section.experiment,
            filename_override=self.output_stem,
        )

        if should_skip(json_path, force=force):
            logger.info(f"[skip cached] {section.short_id}")
            return False

        logger.info(f"[process]     {section.short_id}")

        system_prompt, user_prompt = self._build_prompts(section)
        response = self.client.complete_json(
            self.task_config,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        validated = self._validate(response, section)
        markdown = self._render_markdown(validated, section)

        write_output(
            json_path=json_path,
            md_path=md_path,
            json_data=validated.model_dump(),
            md_content=markdown,
        )

        logger.info(
            f"[done]        {section.short_id}  "
            f"tokens={response.total_tokens}"
        )
        return True


    def rerender(self, section: SectionFile) -> bool:
        """
        Re-render markdown from the existing JSON output without calling the LLM.

        Useful during template development. Returns True if a re-render was
        performed, False if no JSON exists yet (nothing to re-render).
        """
        import json as _json

        json_path, md_path = output_paths(
            self.cfg,
            paper_name=section.paper_name,
            task_name=self.task_name,
            experiment=section.experiment,
            filename_override=self.output_stem,
        )
        if not json_path.exists():
            logger.info(f"[rerender skip] {section.short_id}  (no JSON yet)")
            return False

        raw = _json.loads(json_path.read_text(encoding="utf-8"))
        validated = self.schema_cls.model_validate(raw)
        markdown = self._render_markdown(validated, section)

        # Only rewrite the markdown; leave JSON untouched.
        md_path.parent.mkdir(parents=True, exist_ok=True)
        from ..io_utils import _atomic_write_text
        _atomic_write_text(md_path, markdown)

        logger.info(f"[rerendered]    {section.short_id}")
        return True

    # -- Overridable hooks -------------------------------------------------

    def _build_prompts(self, section: SectionFile) -> tuple[str, str]:
        """
        Return (system_prompt, user_prompt) for the LLM call.

        Uses explicit placeholder substitution (not str.format) so that
        JSON braces inside the prompt template are not mis-interpreted
        as format spec fields.
        """
        prompt_path = Path(__file__).parent.parent / "prompts" / self.prompt_filename
        template = prompt_path.read_text(encoding="utf-8")

        section_location = section.experiment or "paper-level"
        replacements = {
            "{paper_name}": section.paper_name,
            "{section_location}": section_location,
            "{section_text}": section.content,
        }
        filled = template
        for placeholder, value in replacements.items():
            filled = filled.replace(placeholder, value)

        return filled, "Return the JSON now."

    def _validate(self, response: LLMResponse, section: SectionFile) -> BaseModel:
        try:
            return self.schema_cls.model_validate(response.parsed)
        except ValidationError as e:
            raise ProcessorError(
                f"Schema validation failed for {section.short_id}:\n{e}\n\n"
                f"Raw JSON keys: {list(response.parsed.keys())}"
            ) from e

    def _render_markdown(self, data: BaseModel, section: SectionFile) -> str:
        template = _JINJA_ENV.get_template(self.template_filename)
        context = {
            "data": data,
            "paper_name": section.paper_name,
            "section_location": section.experiment or "paper-level",
        }
        return template.render(**context)