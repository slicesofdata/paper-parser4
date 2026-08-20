"""
Pydantic schema for results and discussion extraction.

Design principle: pure faithful extraction of what the authors wrote.
- Statistical values preserved verbatim (no rounding, no reformatting).
- Interpretations captured ONLY when the authors themselves interpret.
- No inference about whether results support predictions unless the authors
  explicitly say so.
- No completeness judgment — that is a separate downstream audit stage.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from ._shared import Citation, Evidenced, StatisticalFinding


class ResultsAndDiscussionSummary(BaseModel):
    """Structured extraction of a merged Results + Discussion section."""

    # ----- Grounded (verbatim-required) fields -----

    key_findings: list[StatisticalFinding] = Field(
        default_factory=list,
        description=(
            "Every statistical result the authors report, with exact test, "
            "variables in the model, effect type, and verbatim reported "
            "statistics. One entry per reported effect (main effect, "
            "interaction, simple effect, comparison, etc.)."
        )
    )
    authors_interpretations: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Statements where the authors themselves interpret what a result "
            "means. Do NOT create entries for results the authors merely "
            "report without commenting on. Each with verbatim quote."
        )
    )
    authors_stated_link_to_predictions: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Verbatim moments where the authors explicitly connect a result "
            "to their own predictions or hypotheses (e.g., 'this supports our "
            "prediction that...', 'contrary to our hypothesis, we found...'). "
            "Empty when the authors do not draw this connection themselves. "
            "Do NOT judge alignment yourself — extract only what authors state."
        )
    )

    # ----- Non-grounded, author-only fields -----

    statistical_approach_summary: str | None = Field(
        default=None,
        description=(
            "How the authors describe their overall analytic approach in this "
            "section: types of analyses run, software used if stated, any "
            "deviations from a pre-stated analysis plan the authors mention. "
            "Use the authors' own language."
        )
    )
    anomalous_or_unexpected_results: list[str] = Field(
        default_factory=list,
        description=(
            "Results the authors themselves describe as unexpected, "
            "surprising, or anomalous. Do NOT include results simply because "
            "they seem noteworthy to you. Only include if the authors "
            "characterize them as such."
        )
    )
    alternative_interpretations_discussed: list[str] = Field(
        default_factory=list,
        description=(
            "Alternative explanations the authors themselves consider and "
            "discuss for their findings. Do NOT invent alternatives the "
            "authors did not raise."
        )
    )
    limitations_stated_by_authors: list[str] = Field(
        default_factory=list,
        description=(
            "Limitations, caveats, or constraints the authors explicitly "
            "acknowledge about their results or their interpretation. Do NOT "
            "add limitations you notice; only what the authors state."
        )
    )
    preview_of_next_experiment: str | None = Field(
        default=None,
        description=(
            "If the authors preview a follow-up experiment or study within "
            "this section, describe what they preview. Null if not previewed."
        )
    )
    citations_referenced: list[Citation] = Field(
        default_factory=list,
        description="All external works cited in this section, with context."
    )
    missing_or_unclear: list[str] = Field(
        default_factory=list,
        description=(
            "Non-statistical elements normally expected in a results section "
            "but absent (e.g., 'sample sizes per condition not reported for "
            "the subgroup analysis', 'descriptive statistics not given for "
            "Condition X', 'no reliability estimate reported for the coding "
            "of subjective responses'). Do NOT list missing statistical "
            "effects here — that is a separate audit stage. Focus on "
            "descriptive and structural omissions."
        )
    )

    @field_validator("preview_of_next_experiment", mode="before")
    @classmethod
    def _normalize_null_strings(cls, v):
        """Convert stringified nulls back to actual None."""
        if isinstance(v, str) and v.strip().lower() in {"null", "none", ""}:
            return None
        return v
