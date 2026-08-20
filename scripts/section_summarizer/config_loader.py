"""
Configuration loader for section_summarizer.

Reads:
  - .env at project root (via python-dotenv) for API keys.
  - config/models.yaml for provider/task/model routing.

Produces:
  - AppConfig object with resolved, validated per-task configurations.

Design notes:
  - Task configs inherit missing fields from `defaults`.
  - API keys are resolved at load time from environment variables named in
    the provider's `api_key_env` field.
  - Missing API keys raise a clear error at load time, not at request time.
  - Unknown providers or missing required fields raise on load.
"""

from __future__ import annotations

import os
#from dataclasses import dataclass, field
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProviderConfig:
    """Configuration for a single LLM provider (Venice, OpenRouter, etc.)."""
    name: str
    base_url: str
    api_key: str  # resolved from env at load time


@dataclass(frozen=True)
class TaskConfig:
    """Resolved configuration for a single task (e.g. 'methods', 'critique')."""
    task_name: str
    provider: ProviderConfig
    model: str
    temperature: float
    max_tokens: int
    timeout_seconds: int


@dataclass(frozen=True)
class PipelineConfig:
    """Pipeline orchestration settings."""
    force_by_default: bool = False


@dataclass(frozen=True)
class AppConfig:
    """Top-level config exposed to the rest of the application."""
    providers: dict[str, ProviderConfig]
    tasks: dict[str, TaskConfig]
    project_root: Path
    pipeline: PipelineConfig = PipelineConfig()

    def task(self, name: str) -> TaskConfig:
        if name not in self.tasks:
            raise KeyError(
                f"Task '{name}' not defined in models.yaml. "
                f"Known tasks: {sorted(self.tasks.keys())}"
            )
        return self.tasks[name]


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

REQUIRED_DEFAULTS = {"provider", "model", "temperature", "max_tokens", "timeout_seconds"}


def _find_project_root(start: Path) -> Path:
    """Walk upward from `start` to find the directory containing pyproject.toml."""
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError(
        "Could not locate project root (no pyproject.toml found in parent dirs)."
    )


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Config file {path} did not parse to a mapping.")
    return data

def _resolve_pipeline(raw: dict[str, Any]) -> PipelineConfig:
    """Read the pipeline block. All fields optional with defaults."""
    pipeline_raw = raw.get("pipeline") or {}
    if not isinstance(pipeline_raw, dict):
        raise ValueError("`pipeline:` must be a mapping.")
    return PipelineConfig(
        force_by_default=bool(pipeline_raw.get("force_by_default", False)),
    )
    
def _resolve_providers(raw: dict[str, Any]) -> dict[str, ProviderConfig]:
    """Turn the `providers:` block into ProviderConfig objects with resolved keys."""
    if "providers" not in raw or not isinstance(raw["providers"], dict):
        raise ValueError("models.yaml must contain a `providers:` mapping.")

    resolved: dict[str, ProviderConfig] = {}
    for name, spec in raw["providers"].items():
        if not isinstance(spec, dict):
            raise ValueError(f"Provider '{name}' must be a mapping.")
        base_url = spec.get("base_url")
        api_key_env = spec.get("api_key_env")
        if not base_url or not api_key_env:
            raise ValueError(
                f"Provider '{name}' requires 'base_url' and 'api_key_env' fields."
            )
        api_key = os.environ.get(api_key_env, "").strip()
        # Empty key is allowed here — we defer failure until a task actually
        # tries to USE this provider. That way you can define OpenRouter in the
        # config without having a key yet.
        resolved[name] = ProviderConfig(
            name=name,
            base_url=base_url,
            api_key=api_key,
        )
    return resolved


def _validate_defaults(defaults: dict[str, Any]) -> None:
    missing = REQUIRED_DEFAULTS - set(defaults.keys())
    if missing:
        raise ValueError(
            f"`defaults:` block missing required fields: {sorted(missing)}"
        )


def _resolve_tasks(
    raw: dict[str, Any],
    providers: dict[str, ProviderConfig],
) -> dict[str, TaskConfig]:
    """Merge each task's config with `defaults` and resolve its provider."""
    defaults = raw.get("defaults", {})
    if not isinstance(defaults, dict):
        raise ValueError("`defaults:` must be a mapping.")
    _validate_defaults(defaults)

    tasks_raw = raw.get("tasks", {})
    if not isinstance(tasks_raw, dict):
        raise ValueError("`tasks:` must be a mapping.")

    resolved: dict[str, TaskConfig] = {}
    for task_name, task_spec in tasks_raw.items():
        task_spec = task_spec or {}
        if not isinstance(task_spec, dict):
            raise ValueError(f"Task '{task_name}' must be a mapping or empty.")

        # Merge: task-level overrides defaults.
        merged = {**defaults, **task_spec}
        provider_name = merged["provider"]
        if provider_name not in providers:
            raise ValueError(
                f"Task '{task_name}' references unknown provider '{provider_name}'. "
                f"Known providers: {sorted(providers.keys())}"
            )

        resolved[task_name] = TaskConfig(
            task_name=task_name,
            provider=providers[provider_name],
            model=merged["model"],
            temperature=float(merged["temperature"]),
            max_tokens=int(merged["max_tokens"]),
            timeout_seconds=int(merged["timeout_seconds"]),
        )
    return resolved


def load_config(
    models_yaml_path: Path | str | None = None,
    env_path: Path | str | None = None,
) -> AppConfig:
    """
    Load and validate the application configuration.

    Parameters
    ----------
    models_yaml_path : path to models.yaml (default: <project_root>/config/models.yaml)
    env_path         : path to .env file  (default: <project_root>/.env)

    Returns
    -------
    AppConfig
    """
    # Locate project root using this file's location.
    project_root = _find_project_root(Path(__file__).parent)

    # Load env vars from .env if present. Does not overwrite existing env vars.
    dotenv_file = Path(env_path) if env_path else project_root / ".env"
    load_dotenv(dotenv_path=dotenv_file, override=False)

    # Load YAML config.
    yaml_path = Path(models_yaml_path) if models_yaml_path else project_root / "config" / "models.yaml"
    raw = _load_yaml(yaml_path)

    providers = _resolve_providers(raw)
    tasks = _resolve_tasks(raw, providers)
    pipeline_cfg = _resolve_pipeline(raw)

    return AppConfig(
        providers=providers,
        tasks=tasks,
        project_root=project_root,
        pipeline=pipeline_cfg,
    )


# ---------------------------------------------------------------------------
# CLI test harness
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """Run `python -m scripts.section_summarizer.config_loader` to verify config."""
    cfg = load_config()
    print(f"Project root: {cfg.project_root}")
    print(f"\nProviders ({len(cfg.providers)}):")
    for name, p in cfg.providers.items():
        key_status = "SET" if p.api_key else "MISSING"
        print(f"  - {name}: {p.base_url}  [API key: {key_status}]")
    print(f"\nTasks ({len(cfg.tasks)}):")
    for name, t in cfg.tasks.items():
        print(
            f"  - {name:28s} provider={t.provider.name:12s} "
            f"model={t.model:35s} temp={t.temperature} "
            f"max_tokens={t.max_tokens}"
        )
