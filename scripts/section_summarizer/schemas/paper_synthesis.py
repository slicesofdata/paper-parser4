"""
Schema for paper-level synthesis output.

This is the final reader-facing artifact — a compressed overview of the
paper designed to let a senior researcher decide whether to read the full
paper and, if so, which sections to prioritize.
"""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


TheoreticalStance = Literal[
    "consistent_theoretical",
    "theory_abandoned",
    "post_hoc_theorizing",
    "consistently_atheoretical",
    "ambiguous",
]

ReadingRecommendation = Literal[
    "read_fully",
    "read_selectively",
    "skim",
    "reference_only",
]


class KeyReference(BaseModel):
    """A high-impact reference for the paper."""
    authors: str = Field(description="Author list as written.")
    year: str = Field(description="Publication year.")
    role: str = Field(
        description=(
            "Why this reference matters to the paper. Examples: "
            "'foundational theory', 'primary methodological reference', "
            "'competing theoretical account', 'key empirical precedent'."
        )
    )


class TheoryDescription(BaseModel):
    """Description of a theory or explanatory account discussed in the paper."""
    name: str = Field(
        description=(
            "Name of the theory as used in the paper. Use a short descriptor "
            "if unnamed."
        )
    )
    role: Literal["focal", "alternative", "background"] = Field(
        description=(
            "'focal' = the paper's own theoretical position. "
            "'alternative' = a competing account the paper discusses. "
            "'background' = a theory cited but not centrally engaged."
        )
    )
    description: str = Field(
        description="Brief description of what the theory claims."
    )


class StudyDesignOverview(BaseModel):
    """Compact description of the paper's empirical strategy."""
    n_experiments: int = Field(description="Number of experiments in the paper.")
    predictors_examined: list[str] = Field(
        default_factory=list,
        description="The predictor variables across the experiments."
    )
    outcomes_examined: list[str] = Field(
        default_factory=list,
        description="The outcome variables across the experiments."
    )
    materials_summary: str | None = Field(
        default=None,
        description="Brief description of stimuli/materials used."
    )
    design_types: list[str] = Field(
        default_factory=list,
        description=(
            "Design types across experiments: e.g., 'exp_1: within-subjects 2x2', "
            "'exp_2: mixed 2x2x3'."
        )
    )


class EvidenceClaimAlignment(BaseModel):
    """Where the paper's evidence supports or diverges from its claims."""
    supported_claims: list[str] = Field(
        default_factory=list,
        description="Claims well-supported by evidence."
    )
    unsupported_or_weakly_supported_claims: list[str] = Field(
        default_factory=list,
        description="Claims where evidence is ambiguous or weakly supportive."
    )
    contradictions_or_tensions: list[str] = Field(
        default_factory=list,
        description="Places where claims across sections are in tension."
    )


class PaperSynthesis(BaseModel):
    """Complete paper-level overview."""

    executive_summary: str = Field(
        description="2-3 sentence high-level statement of what the paper does and found."
    )

    background_and_motivation: str = Field(
        description="Synthesis of research gap and motivating prior work. 2-4 sentences."
    )

    theories_discussed: list[TheoryDescription] = Field(
        default_factory=list,
        description="All theories/accounts discussed, tagged by role."
    )

    theoretical_stance: TheoreticalStance = Field(
        description="Overall theoretical stance judgment."
    )

    theoretical_stance_justification: str = Field(
        description="1-3 sentence justification for the stance."
    )

    study_design: StudyDesignOverview = Field(
        description="Compact overview of the empirical strategy."
    )

    findings_summary: str = Field(
        description="Cross-experiment synthesis of key findings. 3-6 sentences."
    )

    evidence_claim_alignment: EvidenceClaimAlignment = Field(
        description="Structured assessment of evidence-claim alignment."
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="What the paper does well. 3-8 items."
    )

    weaknesses_and_concerns: list[str] = Field(
        default_factory=list,
        description="Curated top concerns from the critique. 3-8 items."
    )

    key_references: list[KeyReference] = Field(
        default_factory=list,
        description="5-15 references most central to the paper."
    )

    reading_recommendation: ReadingRecommendation = Field(
        description="How deeply to read: fully, selectively, skim, reference-only."
    )

    reading_recommendation_justification: str = Field(
        description="1-3 sentence justification. Name sections if 'read_selectively'."
    )