"""
Provider-agnostic LLM client wrapper.

Uses the OpenAI Python SDK, which speaks OpenAI-compatible HTTP for any
provider that implements that interface (Venice, OpenRouter, OpenAI itself,
Ollama, LM Studio, etc.).

Public interface:
  - LLMClient.complete_json(task_config, system_prompt, user_prompt, ...)
        Returns parsed JSON dict, retrying on transient failures.

Design notes:
  - One OpenAI() client per provider, cached by provider name.
  - JSON output is requested via `response_format={"type": "json_object"}`.
    If the model doesn't support that, we still get a string back and parse it.
  - Retries with exponential backoff via tenacity. Non-retriable errors
    (auth, bad request) fail fast.
  - Token usage is logged for cost tracking.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from openai import OpenAI, APIError, APIConnectionError, RateLimitError, APITimeoutError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

from .config_loader import TaskConfig, ProviderConfig


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Response container
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LLMResponse:
    """Result of a single LLM call."""
    parsed: dict[str, Any]       # parsed JSON payload
    raw_text: str                # raw string returned by the model
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    model: str                   # actual model id used
    finish_reason: str | None


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class LLMError(RuntimeError):
    """Base class for LLM client errors."""


class LLMConfigError(LLMError):
    """Configuration problem (missing key, bad provider, etc.)."""


class LLMResponseError(LLMError):
    """Response could not be parsed as expected."""


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

# Exceptions that indicate a transient failure and should be retried.
RETRIABLE_EXCEPTIONS = (
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
)


class LLMClient:
    """
    Thin wrapper around OpenAI-compatible chat completion APIs.

    Instantiate once per run; reuse across calls. Internal OpenAI clients are
    cached per provider to avoid reconnection overhead.
    """

    def __init__(self) -> None:
        self._clients: dict[str, OpenAI] = {}

    # -- Internal ---------------------------------------------------------

    def _get_client(self, provider: ProviderConfig) -> OpenAI:
        if provider.name not in self._clients:
            if not provider.api_key:
                raise LLMConfigError(
                    f"Provider '{provider.name}' has no API key. "
                    f"Set the corresponding env var in .env."
                )
            self._clients[provider.name] = OpenAI(
                api_key=provider.api_key,
                base_url=provider.base_url,
            )
        return self._clients[provider.name]

    # -- Public -----------------------------------------------------------

    def complete_json(
        self,
        task: TaskConfig,
        system_prompt: str,
        user_prompt: str,
        *,
        extra_params: dict[str, Any] | None = None,
    ) -> LLMResponse:
        """
        Make a chat completion call requesting JSON output.

        Parameters
        ----------
        task          : TaskConfig from config_loader (provides model, temp, etc.)
        system_prompt : system role message (task instructions, output schema)
        user_prompt   : user role message (the actual section text to process)
        extra_params  : optional dict merged into the request payload (e.g. seed)

        Returns
        -------
        LLMResponse with parsed JSON, raw text, and token usage.
        """
        return self._call_with_retry(task, system_prompt, user_prompt, extra_params or {})

    # -- Retry wrapper ----------------------------------------------------

    @retry(
        retry=retry_if_exception_type(RETRIABLE_EXCEPTIONS),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def _call_with_retry(
        self,
        task: TaskConfig,
        system_prompt: str,
        user_prompt: str,
        extra_params: dict[str, Any],
    ) -> LLMResponse:
        client = self._get_client(task.provider)

        request_kwargs: dict[str, Any] = {
            "model": task.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": task.temperature,
            "max_tokens": task.max_tokens,
            "timeout": task.timeout_seconds,
            "response_format": {"type": "json_object"},
        }
        request_kwargs.update(extra_params)

        try:
            response = client.chat.completions.create(**request_kwargs)
        except APIError as e:
            # Non-retriable API errors (400, 401, 403, 404, etc.)
            # If the provider rejects response_format, retry without it once.
            if "response_format" in str(e).lower():
                logger.warning(
                    f"Provider '{task.provider.name}' rejected response_format; "
                    f"retrying without it."
                )
                request_kwargs.pop("response_format", None)
                response = client.chat.completions.create(**request_kwargs)
            else:
                raise LLMError(
                    f"API error from {task.provider.name}/{task.model}: {e}"
                ) from e

        # Extract text content.
        if not response.choices:
            raise LLMResponseError("Response contained no choices.")

        choice = response.choices[0]
        raw_text = (choice.message.content or "").strip()
        if not raw_text:
            raise LLMResponseError("Model returned empty content.")

        # Parse JSON. If it fails, try to strip common wrappers (markdown fences).
        parsed = _parse_json_lenient(raw_text)

        usage = response.usage
        return LLMResponse(
            parsed=parsed,
            raw_text=raw_text,
            prompt_tokens=getattr(usage, "prompt_tokens", 0) if usage else 0,
            completion_tokens=getattr(usage, "completion_tokens", 0) if usage else 0,
            total_tokens=getattr(usage, "total_tokens", 0) if usage else 0,
            model=response.model or task.model,
            finish_reason=choice.finish_reason,
        )


# ---------------------------------------------------------------------------
# JSON parsing helpers
# ---------------------------------------------------------------------------

def _parse_json_lenient(text: str) -> dict[str, Any]:
    """
    Parse JSON, tolerating common LLM output artifacts:
      - markdown code fences (```json ... ```)
      - leading/trailing prose before/after the JSON
    """
    # Fast path.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip markdown fences.
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.split("\n")
        # Drop first line (```json or ```) and last line if it's ```
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass

    # Find the first { and last } and try to parse the substring.
    first = text.find("{")
    last = text.rfind("}")
    if first != -1 and last != -1 and last > first:
        try:
            return json.loads(text[first : last + 1])
        except json.JSONDecodeError:
            pass

    raise LLMResponseError(
        f"Could not parse model output as JSON. First 500 chars:\n{text[:500]}"
    )


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Smoke test: send a trivial JSON extraction request to the `abstract` task's
    configured model. Verifies key/network/model are all working.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from .config_loader import load_config

    cfg = load_config()
    task = cfg.task("abstract")  # any task works for the smoke test

    client = LLMClient()
    system = (
        "You are a test assistant. Reply with a JSON object containing a "
        "single key 'status' with the value 'ok'."
    )
    user = "Please confirm you can reply with JSON."

    print(f"Calling {task.provider.name}/{task.model} ...")
    resp = client.complete_json(task, system, user)
    print(f"Parsed JSON: {resp.parsed}")
    print(
        f"Tokens: prompt={resp.prompt_tokens} "
        f"completion={resp.completion_tokens} "
        f"total={resp.total_tokens}"
    )
    print(f"Finish reason: {resp.finish_reason}")