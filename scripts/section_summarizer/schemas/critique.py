"""
Schema for paper-level critique output.

Critique is a novel-analysis task (not extraction). Each entry captures a
scholarly concern with its category, severity, evidence grounding to
specific section JSONs, and reasoning.
"""

from __future__ import annotations

import re

from typing import Literal

from pydantic import BaseModel, Field, field_validator



# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------

SectionRef = Literal[
    "abstract",
    "introduction",             # paper-level introduction.json
    "general_discussion",       # paper-level general_discussion.json
    "exp_introduction",         # exp_N/introduction.json
    "methods",                  # exp_N/methods.json
    "results_and_discussion",   # exp_N/results_and_discussion.json
    "cross_section",            # concern spans multiple sections
]

CritiqueCategory = Literal[
    "design_theory_alignment",
    "evidence_theory_alignment",
    "internal_consistency",
    "alternative_accounts",
    "statistical_completeness",
    "methodological_concerns",
    "statistical_robustness",
]

Severity = Literal["high", "moderate", "minor"]


class SupportingEvidence(BaseModel):
    section: SectionRef = Field(
        description="Which section JSON the evidence comes from."
    )
    experiment: str | None = Field(
        default=None,
        description=(
            "Experiment identifier (e.g., 'exp_1', 'exp_2') when the evidence "
            "is experiment-level. Null for paper-level sections."
        )
    )
    field: str | None = Field(
        default=None,
        description=(
            "The specific field within the section JSON, e.g. 'power_analysis', "
            "'key_findings', 'theoretical_framework'. Null when the concern "
            "is about the section as a whole."
        )
    )
    detail: str = Field(
        description=(
            "Compact description of what was found (or missing) at this "
            "location that motivates the critique. May quote or paraphrase."
        )
    )

    @field_validator("section", mode="before")
    @classmethod
    def _coerce_section(cls, v):
        """
        Salvage common LLM mistakes: paths, field names used as section values.
        Maps known problematic values to their canonical section.
        """
        if not isinstance(v, str):
            return v

        # Path form: "exp_1/methods" -> take the section-shaped part
        if "/" in v:
            for part in v.split("/"):
                if part in ("abstract", "introduction", "general_discussion",
                            "exp_introduction", "methods", "results_and_discussion",
                            "cross_section"):
                    return part

        # Field name used as section — remap to parent
        field_to_section = {
            # Methods fields
            "materials": "methods",
            "outcome_measures": "methods",
            "procedure": "methods",
            "design": "methods",
            "participants": "methods",
            "power_analysis": "methods",
            "rationale_for_choices": "methods",
            "data_analysis_plan": "methods",
            # Introduction fields (paper-level)
            "theoretical_framework": "introduction",
            "specific_hypotheses": "introduction",
            "mechanistic_claims": "introduction",
            "background_research_summary": "introduction",
            "key_terminology": "introduction",
            "alternative_theories": "introduction",
            "constructs_of_interest": "introduction",
            # Introduction fields (experiment-level)
            "specific_predictions": "exp_introduction",
            "theoretical_refinements": "exp_introduction",
            "new_alternative_theories": "exp_introduction",
            # Results fields
            "key_findings": "results_and_discussion",
            "authors_interpretations": "results_and_discussion",
            "statistical_approach_summary": "results_and_discussion",
            "authors_stated_link_to_predictions": "results_and_discussion",
            "limitations_stated_by_authors": "results_and_discussion",
            # Discussion fields
            "theoretical_conclusions": "general_discussion",
            "cross_experiment_integration": "general_discussion",
            "implications_for_field": "general_discussion",
            "results_stated_to_support_theory": "general_discussion",
            "results_stated_to_challenge_theory": "general_discussion",
            "alternative_accounts_addressed": "general_discussion",
        }
        if v in field_to_section:
            return field_to_section[v]

        # Experiment identifier used as section — coerce to a valid section.
        # We can't know which section within the experiment; use cross_section.
        if re.match(r"^exp_[0-9a-z_]+$", v):
            return "cross_section"

        return v


class CritiqueEntry(BaseModel):
    """A single scholarly concern about the paper."""
    concern: str = Field(
        description="One-sentence summary of the issue. Skimmable."
    )
    category: CritiqueCategory = Field(
        description="Which category this concern falls under."
    )
    severity: Severity = Field(
        description=(
            "'high' = questions the paper's core claim or validity. "
            "'moderate' = notable concern that should be considered. "
            "'minor' = worth noting but does not undermine the paper."
        )
    )
    supporting_evidence: list[SupportingEvidence] = Field(
        default_factory=list,
        description=(
            "One or more references to section JSONs where the concern is "
            "grounded. Multiple entries when a concern spans sections."
        )
    )
    justification: str = Field(
        description=(
            "Two to four sentences explaining why this constitutes a concern. "
            "This is where the scholarly reasoning lives. Be specific: name "
            "the analytical or theoretical principle at stake."
        )
    )


# ---------------------------------------------------------------------------
# Top-level schema
# ---------------------------------------------------------------------------

class CritiqueSummary(BaseModel):
    """Complete critique of a paper, organized by category."""

    # Categories are stored as separate lists so the LLM must classify each
    # concern into exactly one category rather than tagging retroactively.
    design_theory_alignment: list[CritiqueEntry] = Field(
        default_factory=list,
        description=(
            "Concerns about whether the predictor, outcome, and materials "
            "are appropriate for testing the stated theory. Includes whether "
            "the operationalizations match the theoretical constructs."
        )
    )
    evidence_theory_alignment: list[CritiqueEntry] = Field(
        default_factory=list,
        description=(
            "Concerns about whether the results actually support the "
            "theoretical claims the paper advances. Includes overreach in "
            "the discussion, selective emphasis, results that contradict "
            "claims but are not integrated, and theoretical stretches."
        )
    )
    internal_consistency: list[CritiqueEntry] = Field(
        default_factory=list,
        description=(
            "Concerns about consistency ACROSS sections: intro predictions "
            "vs. what was tested, intro theory vs. discussion theory, whether "
            "each experiment addresses the paper's research question."
        )
    )
    alternative_accounts: list[CritiqueEntry] = Field(
        default_factory=list,
        description=(
            "Concerns about alternative theoretical accounts the authors "
            "should have considered but did not, or addressed poorly. "
            "Includes plausible competing explanations not ruled out by the "
            "design."
        )
    )
    statistical_completeness: list[CritiqueEntry] = Field(
        default_factory=list,
        description=(
            "Concerns about incomplete reporting of implied analyses. "
            "Given the design, what effects should have been reported? "
            "Are follow-up comparisons missing where a significant "
            "interaction or a multi-level main effect was found?"
        )
    )
    methodological_concerns: list[CritiqueEntry] = Field(
        default_factory=list,
        description=(
            "Concerns about method transparency and rigor: missing power "
            "analysis, vague exclusion criteria, unclear counterbalancing, "
            "missing reliability estimates, no preregistration, small N."
        )
    )
    statistical_robustness: list[CritiqueEntry] = Field(
        default_factory=list,
        description=(
            "Concerns about how the reported statistics were interpreted or "
            "framed: marginal effects treated as significant, missing "
            "multiple-comparison corrections, missing effect sizes or "
            "confidence intervals, inflated inferences from small effects."
        )
    )
    overall_assessment: str | None = Field(
        default=None,
        description=(
            "Two to five sentences characterizing the paper's overall "
            "scholarly standing based on the critique above. Avoid summary "
            "statements about findings; focus on the paper's rigor, "
            "theoretical clarity, and evidentiary support for its claims."
        )
    )