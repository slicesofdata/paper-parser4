"""
Pydantic schema for paper-level introduction section extraction.

Grounded fields (Evidenced type) apply to theoretical/mechanistic content
where verbatim preservation matters for scholarly interpretation. Other
fields tolerate paraphrase.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from ._shared import AlternativeTheory, Citation, Evidenced


# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------

class KeyTerm(BaseModel):
    """A term defined by the authors in the introduction."""
    term: str = Field(description="The term as introduced.")
    definition: str = Field(description="The authors' definition of the term.")
    verbatim_definition: str | None = Field(
        default=None,
        description=(
            "Verbatim quote of the definition when the authors explicitly "
            "define the term. Null if only implicitly used."
        )
    )


# AlternativeTheory now in _shared.py
#class AlternativeTheory(BaseModel):
#    """A competing theoretical account the authors mention."""
#    name: str = Field(
#        description=(
#            "Name of the theory or account (as used in the paper). "
#            "If unnamed, provide a short descriptor like 'attention-based account'."
#        )
#    )
#    description: str = Field(
#        description="Brief description of what the theory claims."
#    )
#    difference_from_focal_theory: str = Field(
#        description=(
#            "How this alternative differs from the focal theory of the paper: "
#            "different variables invoked, different mechanism, different scope, "
#            "different predictions, etc."
#        )
#    )
#    citations: list[Citation] = Field(
#        default_factory=list,
#        description="Citations associated with this alternative theory."
#    )

class ConstructOfInterest(BaseModel):
    """A predictor or outcome construct as defined by the authors."""
    role: str = Field(
        description="'predictor' or 'outcome'."
    )
    name: str = Field(description="Name of the construct.")
    definition: str = Field(
        description="How the authors conceptualize this construct in the introduction."
    )


# ---------------------------------------------------------------------------
# Top-level schema
# ---------------------------------------------------------------------------

class IntroductionPaperSummary(BaseModel):
    """Complete structured extraction of a paper-level introduction."""

    # ----- Grounded (Evidenced) fields -----

    theoretical_framework: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "The theory or explanatory framework the paper advances or tests. "
            "Include the mechanism explaining why the predictor should influence "
            "the outcome. May be named ('distinctiveness heuristic') or unnamed. "
            "May be presented as a hypothesis. Include ALL statements that "
            "articulate the framework, each with its verbatim quote."
        )
    )
    specific_hypotheses: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Testable predictions derived from the theory. Often measure-specific "
            "(e.g., 'we predict higher hit rates for low-frequency items'). Each "
            "hypothesis with its verbatim quote."
        )
    )
    mechanistic_claims: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Statements about HOW the predictor influences the outcome: "
            "mediating processes, moderating conditions, boundary conditions, "
            "causal pathways. Each with verbatim support."
        )
    )

    # ----- Non-grounded fields -----

    research_gap: str | None = Field(
        default=None,
        description=(
            "The unresolved question or unaddressed issue the paper takes up. "
            "One or two sentences."
        )
    )
    background_research_summary: list[str] = Field(
        default_factory=list,
        description=(
            "Key findings from prior work that set up the current study. Each "
            "bullet should include the substantive finding and cite its source "
            "inline, e.g., 'Meeks and Marsh (2003) showed that ...'."
        )
    )
    key_terminology: list[KeyTerm] = Field(
        default_factory=list,
        description=(
            "Specialized terms the authors define or introduce (e.g., "
            "'distinctiveness heuristic', 'expected memorability')."
        )
    )
    alternative_theories: list[AlternativeTheory] = Field(
        default_factory=list,
        description=(
            "Competing theoretical accounts the authors discuss, with a "
            "description and explicit comparison to the focal theory."
        )
    )
    constructs_of_interest: list[ConstructOfInterest] = Field(
        default_factory=list,
        description=(
            "Predictor and outcome constructs as conceptualized by the authors."
        )
    )
    rationale_for_predictor: str | None = Field(
        default=None,
        description=(
            "Why the authors chose this predictor variable, as they explain it. "
            "Include any prior findings or theoretical reasoning they cite."
        )
    )
    rationale_for_outcome: str | None = Field(
        default=None,
        description=(
            "Why the authors chose this outcome variable, as they explain it."
        )
    )
    overview_of_studies: str | None = Field(
        default=None,
        description=(
            "If the intro previews the experiments (common in multi-experiment "
            "papers), summarize the roadmap: what each experiment does and how "
            "they connect."
        )
    )
    citations_referenced: list[Citation] = Field(
        default_factory=list,
        description=(
            "Aggregated list of all works cited in the introduction with their "
            "context. Includes citations already listed inline elsewhere."
        )
    )
    missing_or_unclear: list[str] = Field(
        default_factory=list,
        description=(
            "Elements normally expected in a scholarly introduction but not "
            "present or ambiguously stated. Examples: 'no explicit hypothesis "
            "stated', 'theoretical framework not named', 'predictor rationale "
            "not provided', 'no clear research gap identified'."
        )
    )
    quoted_evidence: list[str] = Field(
        default_factory=list,
        description=(
            "1-3 short verbatim quotes that best capture the introduction's "
            "core theoretical stance. Supplementary to Evidenced fields above."
        )
    )