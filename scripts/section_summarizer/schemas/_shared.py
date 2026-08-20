"""
Shared Pydantic types used across multiple section schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

class Citation(BaseModel):
    """A reference to another work cited within a section."""
    authors: str = Field(
        description="Author list as written, e.g. 'Meeks and Marsh' or 'Smith et al.'"
    )
    year: str = Field(
        description="Publication year as a string (may include 'a'/'b' suffixes)."
    )
    context: str = Field(
        default="",
        description=(
            "What this citation supports in the current section. May be empty "
            "if the citation appears in a general reference list without a "
            "specific claim it supports."
        )
    )

    @field_validator("authors", "year", mode="before")
    @classmethod
    def _coerce_missing_to_string(cls, v):
        """Coerce null/None to a placeholder string so validation passes."""
        if v is None:
            return "(not specified)"
        return v


class Evidenced(BaseModel):
    """
    A verbatim quote paired with a short topic label for browsability.

    The verbatim quote is the authoritative content — the exact text from
    the source. The topic label is a short DESCRIPTIVE tag identifying
    what the quote is about; it must not paraphrase the claim, add
    interpretation, or invent language beyond what the source states.

    Used for extractions where wording matters (theoretical claims,
    hypotheses, findings, interpretations).
    """
    topic_label: str = Field(
        description=(
            "Short descriptive tag identifying the subject matter of the "
            "quote (typically 2-8 words). This is NOT a claim, paraphrase, "
            "or interpretation. It just names the topic. Examples: "
            "'memorability of low-frequency items', 'hit rates in pure "
            "lists', 'role of context variability'. Do NOT include "
            "interpretive words like 'robust', 'supports', 'confirms', "
            "'indicates', unless they name the topic itself."
        )
    )
    verbatim_quote: str = Field(
        description=(
            "Verbatim text from the source that supports the topic_label. "
            "Preserve exact wording, punctuation, and capitalization. "
            "Under 300 characters. If multiple sentences are needed, keep "
            "them consecutive. This is the authoritative record. "
            "The quote MUST match the topic_label — do NOT reuse a quote "
            "from one topic under a different topic_label. If two distinct "
            "constructs are both worth extracting, they need separate quotes "
            "from separate parts of the source. If the source only has one "
            "sentence covering both, use one entry with a combined label."
        )
    )
    citations_inline: list[Citation] = Field(
        default_factory=list,
        description=(
            "Citations that appear within this verbatim quote or immediately "
            "adjacent to it in the source. ONLY external works — do NOT "
            "cite the current paper itself. If no citation appears in the "
            "quote, this array must be empty."
        )
    )

    @field_validator("topic_label", mode="before")
    @classmethod
    def _accept_legacy_statement(cls, v, info):
        """
        Accept legacy 'statement' key from older JSON outputs.
        Allows re-loading pre-migration outputs without regeneration.
        """
        if v is None or v == "":
            # Check if the caller passed 'statement' (legacy field name)
            values = info.data if hasattr(info, "data") else {}
            legacy = values.get("statement")
            if legacy:
                return legacy
        return v


class AlternativeTheory(BaseModel):
    """A competing theoretical account discussed in a paper or experiment."""
    name: str = Field(
        description=(
            "Name of the theory or account (as used in the paper). "
            "If unnamed, provide a short descriptor like 'attention-based account'."
        )
    )
    description: str = Field(
        description="Brief description of what the theory claims."
    )
    difference_from_focal_theory: str = Field(
        description=(
            "How this alternative differs from the focal theory of the paper: "
            "different variables invoked, different mechanism, different scope, "
            "different predictions, etc."
        )
    )
    citations: list[Citation] = Field(
        default_factory=list,
        description="Citations associated with this alternative theory."
    )


class StatisticalFinding(BaseModel):
    """
    A single reported statistical result, preserving the authors' exact
    reported values verbatim.

    Used for results extraction where wording AND numerical precision matter.
    """
    finding_statement: str = Field(
        description=(
            "Concise statement of what the test showed, in the authors' framing. "
            "Light paraphrase for readability, but preserve direction, "
            "which variables/conditions differ, and significance status."
        )
    )
    statistical_test: str = Field(
        description=(
            "The statistical test as the authors named it, e.g. "
            "'2 (word frequency: low vs high) x 2 (context variability: low vs high) "
            "mixed ANOVA', 'paired-samples t-test', 'linear mixed-effects model'."
        )
    )
    variables_in_model: list[str] = Field(
        default_factory=list,
        description=(
            "The predictor and outcome variables involved in this specific test. "
            "Include both factors and the dependent measure."
        )
    )
    effect_type: str | None = Field(
        default=None,
        description=(
            "The type of effect this finding represents: 'main effect', "
            "'two-way interaction', 'three-way interaction', 'simple effect', "
            "'planned comparison', 'post-hoc comparison', 't-test', "
            "'correlation', 'other'. Use the authors' language when they specify."
        )
    )
    verbatim_statistical_report: str = Field(
        description=(
            "The exact sentence(s) from the source reporting this result, "
            "including test statistic, degrees of freedom, p-value, effect "
            "size, confidence intervals — everything numeric the authors "
            "reported. Preserve EXACTLY as written. Do not round, reformat, "
            "or paraphrase numbers."
        )
    )
    verbatim_descriptives: str | None = Field(
        default=None,
        description=(
            "Verbatim descriptive statistics reported alongside this finding "
            "(Ms, SDs, %s, CIs for each condition). Null if none reported. "
            "Preserve EXACTLY as written."
        )
    )
    citations_inline: list[Citation] = Field(
        default_factory=list,
        description="Citations within or immediately adjacent to this finding's report."
    )

    @field_validator("verbatim_descriptives", mode="before")
    @classmethod
    def _normalize_null_strings(cls, v):
        """Convert stringified nulls back to actual None."""
        if isinstance(v, str) and v.strip().lower() in {"null", "none", ""}:
            return None
        return v

class AlternativeAddressed(BaseModel):
    """
    An alternative explanation or theory that the authors address in the
    discussion. May be a formally named theory with citations, or an
    unnamed alternative explanation the authors raise.
    """
    label: str = Field(
        description=(
            "Short label for the alternative. May be a formal theory name "
            "(e.g., 'dual-process account'), an author-provided name, or a "
            "brief descriptor of an unnamed alternative (e.g., 'demand "
            "characteristics explanation')."
        )
    )
    is_named_theory: bool = Field(
        description=(
            "True if this is a formally named theory or account with an "
            "established literature. False if this is an unnamed alternative "
            "explanation the authors raise."
        )
    )
    description: str = Field(
        description="What the alternative claims or would predict."
    )
    how_authors_addressed_it: str = Field(
        description=(
            "How the authors handle this alternative: rule it out based on "
            "results, acknowledge it as compatible, argue against it, etc. "
            "Use the authors' framing."
        )
    )
    citations: list[Citation] = Field(
        default_factory=list,
        description="Citations paired with this alternative, if any."
    )
