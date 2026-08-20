"""
End-to-end pipeline orchestrator.

Runs all pipeline stages in order for one or more papers:

  1. parse       -- PDF -> markdown (MinerU)
  2. postprocess -- character normalization of MinerU output
  3. split       -- markdown -> per-section files
  4. abstract    -- copy abstract verbatim
  5. extraction  -- per-section LLM processors
  6. critique    -- paper-level critique
  7. synthesis   -- paper-level synthesis
  8. report      -- markdown + PDF assembly

Cache behavior:
  Respects existing cached outputs by default (skips completed stages).
  Set `pipeline.force_by_default: true` in config/models.yaml, OR pass
  --force on the command line, to regenerate everything.
  --no-force overrides a `force_by_default: true` config back to safe mode.

Selective stages:
  --stages parse,postprocess,split,extraction,critique,synthesis,report
    Runs only the named stages.

Error handling:
  Errors are logged and the pipeline continues to the next paper.
  Final summary lists which papers succeeded and which failed at which stage.

Paper identification:
  Papers are identified by their BASE NAME (the PDF filename without .pdf).
  For example: "Meeks, Knight, Brewer, Cook 2014 - Marsh Investigating..."
  This name must match the PDF file in pdfs_input/ (minus .pdf).

Usage:
  # Single paper (name matches pdfs_input/<name>.pdf)
  uv run --no-sync python -m scripts.section_summarizer.run_pipeline "<paper>"

  # All PDFs in pdfs_input/
  uv run --no-sync python -m scripts.section_summarizer.run_pipeline --all

  # Force regeneration
  uv run --no-sync python -m scripts.section_summarizer.run_pipeline "<paper>" --force

  # Only extraction, critique, synthesis, and report (skip parse/postprocess/split)
  uv run --no-sync python -m scripts.section_summarizer.run_pipeline "<paper>" --stages extraction,critique,synthesis,report

  # Skip PDF output in report stage
  uv run --no-sync python -m scripts.section_summarizer.run_pipeline "<paper>" --no-pdf
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .config_loader import AppConfig, load_config
from .copy_abstracts import copy_abstract
from .io_utils import discover_sections, list_papers, paper_input_dir
from .llm_client import LLMClient
from .build_paper_report import build_report

# Section processors
from .processors.introduction_paper import IntroductionPaperProcessor
from .processors.introduction_experiment import IntroductionExperimentProcessor
from .processors.methods import MethodsProcessor
from .processors.results_and_discussion import ResultsAndDiscussionProcessor
from .processors.discussion_paper import DiscussionPaperProcessor
from .processors.critique import CritiqueProcessor
from .processors.paper_synthesis import PaperSynthesisProcessor


logger = logging.getLogger(__name__)


ALL_STAGES = [
    "parse",
    "postprocess",
    "split",
    "abstract",
    "extraction",
    "critique",
    "synthesis",
    "report",
]


@dataclass
class PipelineResult:
    """Track pipeline execution for one paper."""
    paper_name: str
    stages_completed: list[str] = field(default_factory=list)
    stages_failed: list[tuple[str, str]] = field(default_factory=list)

    @property
    def succeeded(self) -> bool:
        return not self.stages_failed


def _list_pdfs(cfg: AppConfig) -> list[str]:
    """Return paper names (PDF stems) present in pdfs_input/."""
    pdfs_dir = cfg.project_root / "pdfs_input"
    if not pdfs_dir.exists():
        return []
    return sorted(p.stem for p in pdfs_dir.glob("*.pdf"))


def run_pipeline_for_paper(
    cfg: AppConfig,
    paper_name: str,
    client: LLMClient,
    *,
    force: bool,
    stages: list[str],
    include_critique_in_report: bool = True,
    write_pdf: bool = True,
) -> PipelineResult:
    """Run selected pipeline stages for one paper."""
    result = PipelineResult(paper_name=paper_name)

    def _run(stage_name: str, work: Callable[[], None]) -> None:
        if stage_name not in stages:
            logger.info(f"[skip stage]  {paper_name}/{stage_name}")
            return
        try:
            work()
            result.stages_completed.append(stage_name)
        except Exception as e:
            logger.error(f"[stage error] {paper_name}/{stage_name}: {e}", exc_info=True)
            result.stages_failed.append((stage_name, str(e)))

    # ---- Stage 1: parse (PDF -> markdown via MinerU) ----
    def _parse() -> None:
        # Import here so MinerU-heavy dependencies are only loaded if needed.
        from parse_batch import already_done, parse_one

        pdf_path = cfg.project_root / "pdfs_input" / f"{paper_name}.pdf"
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        if already_done(pdf_path) and not force:
            logger.info(f"[skip cached] {paper_name}/parse (markdown exists)")
            return

        success = parse_one(pdf_path)
        if not success:
            raise RuntimeError(f"MinerU parse failed for {paper_name}")

    _run("parse", _parse)

    # ---- Stage 2: postprocess (character normalization) ----
    def _postprocess() -> None:
        from mineru_postprocess import load_config as load_norm_config, process_paper

        paper_md_dir = cfg.project_root / "markdown_output" / paper_name
        if not paper_md_dir.exists():
            raise FileNotFoundError(f"Markdown dir not found: {paper_md_dir}")

        norm_config = load_norm_config()
        # dry_run=False; process_paper handles its own backup/skip logic
        process_paper(paper_md_dir, norm_config, dry_run=False)

    _run("postprocess", _postprocess)

    # ---- Stage 3: split (markdown -> sections) ----
    def _split() -> None:
        from split_sections_of_mineru_md import split_one_paper, OUTPUT_DIR as split_output_dir

        paper_md_dir = cfg.project_root / "markdown_output" / paper_name
        if not paper_md_dir.exists():
            raise FileNotFoundError(f"Markdown dir not found: {paper_md_dir}")

        # Cache check
        sections_dir = split_output_dir / paper_name
        if sections_dir.exists() and (sections_dir / "_debug.txt").exists() and not force:
            logger.info(f"[skip cached] {paper_name}/split (sections exist)")
            return

        success = split_one_paper(paper_md_dir, split_output_dir)
        if not success:
            raise RuntimeError(f"Splitter failed for {paper_name}")

    _run("split", _split)

    # ---- Stage 4: abstract ----
    def _abstract() -> None:
        copy_abstract(cfg, paper_name, force=force)

    _run("abstract", _abstract)

    # ---- Stage 5: extraction ----
    def _extraction() -> None:
        section_processors = {
            "introduction_paper": IntroductionPaperProcessor(cfg, client),
            "introduction_experiment": IntroductionExperimentProcessor(cfg, client),
            "methods": MethodsProcessor(cfg, client),
            "results_and_discussion": ResultsAndDiscussionProcessor(cfg, client),
            "discussion_paper": DiscussionPaperProcessor(cfg, client),
        }
        for section in discover_sections(cfg, paper_name):
            if section.task_name not in section_processors:
                logger.warning(
                    f"No processor for task '{section.task_name}'; skipping "
                    f"{section.short_id}"
                )
                continue
            section_processors[section.task_name].process(section, force=force)

    _run("extraction", _extraction)

    # ---- Stage 6: critique ----
    def _critique() -> None:
        processor = CritiqueProcessor(cfg, client)
        processor.process(paper_name, force=force)

    _run("critique", _critique)

    # ---- Stage 7: synthesis ----
    def _synthesis() -> None:
        processor = PaperSynthesisProcessor(cfg, client)
        processor.process(paper_name, force=force)

    _run("synthesis", _synthesis)

    # ---- Stage 8: report ----
    def _report() -> None:
        build_report(
            cfg, paper_name,
            include_critique=include_critique_in_report,
            write_pdf=write_pdf,
            force=force,
        )

    _run("report", _report)

    return result


def _print_summary(results: list[PipelineResult]) -> None:
    print("\n" + "=" * 78)
    print("PIPELINE SUMMARY")
    print("=" * 78)

    successes = [r for r in results if r.succeeded]
    failures = [r for r in results if not r.succeeded]

    print(f"\nSucceeded: {len(successes)} / {len(results)}")
    for r in successes:
        stages_str = ", ".join(r.stages_completed) if r.stages_completed else "(none)"
        print(f"  - {r.paper_name}")
        print(f"      completed: {stages_str}")

    if failures:
        print(f"\nFailed: {len(failures)} / {len(results)}")
        for r in failures:
            print(f"  - {r.paper_name}")
            if r.stages_completed:
                print(f"      completed: {', '.join(r.stages_completed)}")
            for stage, err in r.stages_failed:
                short_err = err if len(err) < 200 else err[:200] + "..."
                print(f"      FAILED at {stage}: {short_err}")


def _parse_stages(stages_arg: str | None) -> list[str]:
    if not stages_arg:
        return list(ALL_STAGES)
    requested = [s.strip() for s in stages_arg.split(",") if s.strip()]
    unknown = [s for s in requested if s not in ALL_STAGES]
    if unknown:
        raise ValueError(
            f"Unknown stage(s): {unknown}. Known stages: {ALL_STAGES}"
        )
    return requested


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    # Add scripts/ to sys.path so we can import parse_batch, mineru_postprocess,
    # and split_sections_of_mineru_md by name.
    scripts_dir = Path(__file__).resolve().parent.parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    cfg = load_config()

    args = sys.argv[1:]

    force_flag = "--force" in args
    no_force_flag = "--no-force" in args
    all_mode = "--all" in args
    no_pdf = "--no-pdf" in args
    no_critique_in_report = "--no-critique" in args

    stages_arg = None
    if "--stages" in args:
        idx = args.index("--stages")
        if idx + 1 >= len(args):
            print("--stages requires a value")
            sys.exit(1)
        stages_arg = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    paper_args = [
        a for a in args
        if a not in ("--force", "--no-force", "--all", "--no-pdf", "--no-critique")
    ]

    if force_flag and no_force_flag:
        print("Cannot use --force and --no-force together.")
        sys.exit(1)
    if force_flag:
        force = True
    elif no_force_flag:
        force = False
    else:
        force = cfg.pipeline.force_by_default

    try:
        stages = _parse_stages(stages_arg)
    except ValueError as e:
        print(str(e))
        sys.exit(1)

    # Determine paper list.
    # If we're running parse stage, look at pdfs_input/. Otherwise look at
    # sections_output/ (papers that have been split at least).
    if all_mode:
        if "parse" in stages:
            papers = _list_pdfs(cfg)
        else:
            papers = list_papers(cfg)
    elif paper_args:
        papers = paper_args
    else:
        print(
            "Usage:\n"
            "  uv run --no-sync python -m scripts.section_summarizer.run_pipeline <paper> [options]\n"
            "  uv run --no-sync python -m scripts.section_summarizer.run_pipeline --all [options]\n"
            "\n"
            "Options:\n"
            "  --force                 Regenerate all outputs (overrides config)\n"
            "  --no-force              Respect cache (overrides config)\n"
            "  --stages <s1,s2,...>    Run only named stages\n"
            f"                          Available: {','.join(ALL_STAGES)}\n"
            "  --no-critique           Exclude critique from report\n"
            "  --no-pdf                Skip PDF generation in report stage\n"
            "  --all                   Process every paper\n"
            "                          (from pdfs_input/ if 'parse' stage included,\n"
            "                          from sections_output/ otherwise)"
        )
        sys.exit(1)
    
    papers = [p[:-4] if p.lower().endswith(".pdf") else p for p in papers]

    if not papers:
        print("No papers found.")
        sys.exit(0)

    client = LLMClient()

    logger.info(f"Running pipeline for {len(papers)} paper(s)")
    logger.info(f"Force mode: {force}")
    logger.info(f"Stages: {stages}")

    results: list[PipelineResult] = []
    for paper_name in papers:
        logger.info(f"\n{'=' * 78}\nProcessing: {paper_name}\n{'=' * 78}")
        result = run_pipeline_for_paper(
            cfg, paper_name, client,
            force=force,
            stages=stages,
            include_critique_in_report=(not no_critique_in_report),
            write_pdf=(not no_pdf),
        )
        results.append(result)

    _print_summary(results)