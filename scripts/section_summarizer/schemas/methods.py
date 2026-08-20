"""
Pydantic schema for methods section extraction output.

This is the data contract between the LLM's JSON output and everything
downstream (markdown rendering, paper synthesis, critique). Fields are
designed to capture what an expert scholar needs to evaluate methodological
rigor without re-reading the source.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------

class Citation(BaseModel):
    """A reference to another work cited within this section."""
    authors: str = Field(
        description="Author list as written, e.g. 'Meeks and Marsh' or 'Smith et al.'"
    )
    year: str = Field(
        description="Publication year as a string (may include 'a'/'b' suffixes)."
    )
    context: str = Field(
        description="What this citation supports in the current section."
    )


class Participants(BaseModel):
    """Who participated and how they were obtained."""
    n_total: str | None = Field(
        default=None,
        description="Total N as reported, e.g. '45' or '45 (23 female)'."
    )
    n_per_condition: str | None = Field(
        default=None,
        description="Per-cell N if reported for between-subjects designs."
    )
    demographics: str | None = Field(
        default=None,
        description="Age, gender, education, language, or other demographics as reported."
    )
    recruitment_source: str | None = Field(
        default=None,
        description="Where participants came from (e.g., undergraduate pool, MTurk, Prolific)."
    )
    compensation: str | None = Field(
        default=None,
        description="Payment, course credit, or other compensation."
    )
    exclusions: list[str] = Field(
        default_factory=list,
        description="Exclusion criteria and/or number excluded and why."
    )
    testing_context: str | None = Field(
        default=None,
        description="Individual vs. group testing, session length, lab vs. online."
    )

    @field_validator("n_per_condition", mode="before")
    @classmethod
    def _coerce_n_per_condition(cls, v):
        """Coerce dict form to a semicolon-separated string."""
        if isinstance(v, dict):
            parts = [f"{k}: {n}" for k, n in v.items()]
            return "; ".join(parts)
        return v


class PredictorVariable(BaseModel):
    """A single predictor (independent variable) in the design."""
    name: str = Field(description="Name of the predictor as used by the authors.")
    levels: list[str] = Field(
        default_factory=list,
        description="Levels of the predictor, in the order presented."
    )
    manipulation_type: str | None = Field(
        default=None,
        description="'between-subjects', 'within-subjects', 'mixed', or other."
    )
    factor_type: str | None = Field(
        default=None,
        description="Nominal, ordered/ordinal, continuous, etc."
    )


class Design(BaseModel):
    """Experimental design structure."""
    design_statement: str | None = Field(
        default=None,
        description=(
            "The exact design expressed compactly, e.g. "
            "'2 (word frequency: high vs. low) x 2 (encoding: deep vs. shallow) "
            "mixed design with word frequency within-subjects and encoding "
            "between-subjects'."
        )
    )
    predictors: list[PredictorVariable] = Field(
        default_factory=list,
        description="Each predictor variable with its levels and structure."
    )
    counterbalancing: str | None = Field(
        default=None,
        description="Counterbalancing scheme used, or 'not reported' if absent."
    )


class OutcomeMeasure(BaseModel):
    """A single outcome/dependent variable."""
    name: str = Field(description="Name of the outcome measure.")
    operationalization: str = Field(
        description="How the measure was operationally defined and computed."
    )


class Materials(BaseModel):
    """Stimuli and materials used."""
    description: str | None = Field(
        default=None,
        description="Nature of the stimuli/materials (words, images, videos, etc.)."
    )
    source: str | None = Field(
        default=None,
        description="Origin of stimuli: created in-house, adapted from prior work, standardized battery, etc."
    )
    n_stimuli_pool: str | None = Field(
        default=None,
        description="Total stimuli in the pool from which items were drawn."
    )
    n_stimuli_presented: str | None = Field(
        default=None,
        description="Number of stimuli each participant actually saw."
    )
    additional_details: list[str] = Field(
        default_factory=list,
        description="Other relevant material details (length, difficulty, norms used, etc.)."
    )


class Procedure(BaseModel):
    """How the study was run."""
    ordered_steps: list[str] = Field(
        default_factory=list,
        description="Sequential steps of the experimental procedure."
    )
    apparatus: str | None = Field(
        default=None,
        description="Hardware, software, or environment used (e.g., E-Prime, MTurk, PsychoPy)."
    )
    experimenter_presence: str | None = Field(
        default=None,
        description="Whether an experimenter was present, remote, or absent."
    )
    verbatim_instructions: list[str] = Field(
        default_factory=list,
        description=(
            "Direct verbatim quotes of experimenter instructions when presented "
            "in the paper. Include only if actually quoted; do not paraphrase."
        )
    )
    presentation_format: str | None = Field(
        default=None,
        description="Blocked, counterbalanced, fully randomized, random per participant, etc."
    )
    stimulus_timing: str | None = Field(
        default=None,
        description="Fixed duration, self-paced, ISIs, etc."
    )
    session_duration: str | None = Field(
        default=None,
        description="Total testing time if reported."
    )


# ---------------------------------------------------------------------------
# Top-level schema
# ---------------------------------------------------------------------------

class MethodsSummary(BaseModel):
    """Complete structured extraction of a methods section."""

    participants: Participants = Field(default_factory=Participants)
    design: Design = Field(default_factory=Design)
    outcome_measures: list[OutcomeMeasure] = Field(default_factory=list)
    materials: Materials = Field(default_factory=Materials)
    procedure: Procedure = Field(default_factory=Procedure)

    preregistration_status: str | None = Field(
        default=None,
        description=(
            "One of: 'preregistered (link/OSF provided)', "
            "'preregistered (no link)', 'not preregistered', 'not reported'."
        )
    )
    data_analysis_plan: list[str] = Field(
        default_factory=list,
        description="Steps or approach of the planned statistical analysis."
    )
    power_analysis: str | None = Field(
        default=None,
        description="Power analysis details if reported (target power, effect size, resulting N)."
    )
    rationale_for_choices: list[str] = Field(
        default_factory=list,
        description=(
            "Any methodological choices the authors explicitly justified "
            "(e.g., 'chose 500ms SOA based on prior pilot')."
        )
    )
    missing_or_unclear: list[str] = Field(
        default_factory=list,
        description=(
            "Elements normally expected in a methods section but not reported "
            "or ambiguously described. Examples: 'no power analysis reported', "
            "'exclusion criteria not specified', 'counterbalancing not described'."
        )
    )
    citations_referenced: list[Citation] = Field(
        default_factory=list,
        description="All external works cited in this section, aggregated."
    )
    quoted_evidence: list[str] = Field(
        default_factory=list,
        description=(
            "Short verbatim quotes from the source text supporting the extracted "
            "content. 1-3 quotes covering the most important reported facts "
            "(participants, key design features, critical materials, or timing)."
        )
    )