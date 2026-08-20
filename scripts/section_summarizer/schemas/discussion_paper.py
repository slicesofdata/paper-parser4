"""
Pydantic schema for paper-level discussion (general_discussion.md).

Design principles:
- Faithful extraction; no fabrication of theoretical claims.
- Grounded fields require verbatim quotes.
- Explicit atheoretical flag catches "see what happens" papers where
  the LLM might otherwise fabricate theoretical content.
- Field descriptions include disambiguation examples so the LLM
  distinguishes findings from theoretical conclusions.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from ._shared import AlternativeAddressed, Citation, Evidenced


class DiscussionPaperSummary(BaseModel):
    """Structured extraction of a paper-level general discussion."""
  
    # ----- Grounded (Evidenced) fields -----

    theoretical_conclusions: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Statements advancing an EXPLANATION for why the observed "
            "patterns occurred. Must invoke a mechanism, process, or "
            "theoretical account. This is NOT a directional or descriptive "
            "finding statement. 'X increases Y' is a finding, not a "
            "theoretical conclusion. 'X increases Y because of process Z' "
            "IS a theoretical conclusion. Empty for descriptive/exploratory "
            "papers that do not advance theoretical explanations."
        )
    )
    cross_experiment_integration: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Statements that synthesize evidence ACROSS multiple experiments "
            "in this paper (e.g., 'Experiments 1-3 converge on...', "
            "'across all three studies, we found...'). Not statements about "
            "a single experiment's finding. Each with verbatim quote."
        )
    )
    implications_for_field: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Broader claims about what this work means for the field or a "
            "research area. Must go BEYOND restating the specific findings. "
            "'These results extend our understanding of memory processes' "
            "is an implication. 'We found X' is not. Empty when authors "
            "do not draw broader implications."
        )
    )
    results_stated_to_support_theory: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Verbatim moments where the authors themselves explicitly state "
            "that a specific result supports their theoretical account "
            "(e.g., 'this result supports the memorability-based rejection "
            "account'). Do NOT infer such statements — extract only when "
            "the authors themselves make the connection explicitly."
        )
    )
    results_stated_to_challenge_theory: list[Evidenced] = Field(
        default_factory=list,
        description=(
            "Verbatim moments where the authors acknowledge that a result "
            "challenges or complicates a theoretical account — their own "
            "or an alternative (e.g., 'this null result is inconsistent "
            "with a strict familiarity account'). Do NOT infer challenges — "
            "extract only when authors themselves acknowledge them."
        )
    )

    # ----- Structured alternative accounts field -----

    alternative_accounts_addressed: list[AlternativeAddressed] = Field(
        default_factory=list,
        description=(
            "Alternative explanations the authors themselves raise and "
            "address in the discussion. May be named theories with "
            "citations, or unnamed alternatives (e.g., demand characteristics, "
            "measurement artifacts). Do NOT introduce alternatives the "
            "authors did not raise."
        )
    )

    # ----- Non-grounded, author-only fields -----

    summary_of_findings: str | None = Field(
        default=None,
        description=(
            "The authors' own compressed retelling of what they found across "
            "the paper. Usually populated even for descriptive papers — "
            "authors always describe their findings even when they don't "
            "advance theoretical claims."
        )
    )
    limitations_stated_by_authors: list[str] = Field(
        default_factory=list,
        description=(
            "Limitations the authors themselves acknowledge. Do NOT add "
            "your own observations of limitations."
        )
    )
    future_directions: list[str] = Field(
        default_factory=list,
        description=(
            "Future studies or directions the authors themselves suggest. "
            "Do NOT invent directions the authors do not propose."
        )
    )
    applied_implications: list[str] = Field(
        default_factory=list,
        description=(
            "Practical or applied implications the authors themselves state "
            "(clinical, educational, policy, applied research, etc.). "
            "Empty when authors do not draw applied implications."
        )
    )
    citations_referenced: list[Citation] = Field(
        default_factory=list,
        description="All external works cited in this section with context."
    )
    missing_or_unclear: list[str] = Field(
        default_factory=list,
        description=(
            "Elements normally expected in a discussion but absent or "
            "ambiguous. Examples: 'authors describe findings but do not "
            "advance a theoretical explanation', 'no limitations "
            "acknowledged', 'no future directions proposed'."
        )
    )