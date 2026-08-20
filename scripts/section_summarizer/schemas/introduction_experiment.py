"""
Pydantic schema for experiment-level introduction summarization.

Per-experiment introductions are transitional — they connect the paper-level
theory to the specific experiment, and may introduce refinements or new
alternative theories.

This schema is designed to be evaluated with paper-level context injected
into the prompt, so `theoretical_refinements` and `new_alternative_theories`
can be genuinely judged as "new" relative to the paper-level intro.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from ._shared import AlternativeTheory, Citation, Evidenced


class IntroductionExperimentSummary(BaseModel):
    """Structured extraction of an experiment-level introduction paragraph."""

    # ----- Grounded (Evidenced) fields -----

    specific_predictions: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Testable predictions stated specifically for this experiment. "
            "May differ from paper-level hypotheses in measurement specificity "
            "or scope. Each with verbatim quote."
        )
    )
    theoretical_refinements: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Extensions, refinements, or new mechanistic details added to the "
            "focal theory at this experiment. Empty when the experiment merely "
            "restates the paper-level theory. Judge relative to the prior "
            "context provided in the prompt."
        )
    )
    new_alternative_theories: list[AlternativeTheory] = Field(
        default_factory=list,
        description=(
            "Competing or alternative accounts introduced for the FIRST TIME "
            "at this experiment (not present in the paper-level introduction). "
            "Empty when no new alternatives are introduced."
        )
    )

    # ----- Non-grounded fields -----

    rationale_for_this_experiment: str | None = Field(
        default=None,
        description=(
            "Why this experiment is being run: what did the prior experiment(s) "
            "leave unresolved, or what specific question does this experiment "
            "address?"
        )
    )
    relation_to_prior_experiments: str | None = Field(
        default=None,
        description=(
            "How this experiment builds on, extends, replicates, or addresses "
            "issues raised by prior experiments in the same paper. Reference "
            "prior experiments by number when the paper does."
        )
    )
    new_elements_introduced: list[str] = Field(
        default_factory=list,
        description=(
            "New elements at this experiment relative to the previous one: "
            "new manipulation, new sample type, new stimuli, new measure, "
            "new procedural change."
        )
    )
    constraints_addressed: list[str] = Field(
        default_factory=list,
        description=(
            "If this experiment tests a boundary condition, rules out an "
            "alternative explanation from a prior experiment, or responds to "
            "a limitation, describe what is being addressed."
        )
    )
    citations_referenced: list[Citation] = Field(
        default_factory=list,
        description="Works cited in this experiment-level introduction."
    )
    missing_or_unclear: list[str] = Field(
        default_factory=list,
        description=(
            "Elements normally expected in a per-experiment intro but absent "
            "or ambiguous. Examples: 'no explicit rationale for running this "
            "experiment', 'no predictions stated', 'no clear link to prior "
            "experiment'."
        )
    )

