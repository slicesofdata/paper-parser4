"""
Audit non-ASCII characters across MinerU markdown output.

Scans markdown_output/<paper>/auto/*.md and produces a report showing:
  - Which characters appear
  - How often each appears
  - Whether each character is in the normalization config (and if so, what
    substitution is applied)

Usage:
  # Audit all papers
  uv run --no-sync python scripts/character_audit.py

  # Audit a single paper
  uv run --no-sync python scripts/character_audit.py "<paper_name>"

  # Save report to a file
  uv run --no-sync python scripts/character_audit.py --output report.txt

The report is written to logs/character_audit.log by default (and printed
to stdout).
"""

from __future__ import annotations

import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "markdown_output"
CONFIG_PATH = PROJECT_ROOT / "config" / "char_normalization.yaml"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "logs" / "character_audit.log"


def load_normalization_config() -> dict:
    """Load the character normalization config, tolerating absence."""
    if not CONFIG_PATH.exists():
        return {"char_substitutions": {}, "pattern_substitutions": {}}
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return {
        "char_substitutions": data.get("char_substitutions") or {},
        "pattern_substitutions": data.get("pattern_substitutions") or {},
    }


def collect_characters(paper_filter: str | None = None) -> tuple[Counter, dict]:
    """
    Scan MinerU markdown output. Returns:
      - Counter mapping each non-ASCII character to total count
      - dict mapping each character to sorted list of papers it appears in
    """
    counts: Counter = Counter()
    papers: dict[str, set[str]] = defaultdict(set)

    if not INPUT_DIR.exists():
        print(f"Input directory missing: {INPUT_DIR}", file=sys.stderr)
        return counts, {}

    for paper_dir in sorted(INPUT_DIR.iterdir()):
        if not paper_dir.is_dir():
            continue
        if paper_filter and paper_dir.name != paper_filter:
            continue
        auto_dir = paper_dir / "auto"
        if not auto_dir.exists():
            continue
        for md_file in auto_dir.glob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as e:
                print(f"Skip unreadable {md_file}: {e}", file=sys.stderr)
                continue
            for ch in text:
                if ord(ch) > 127:
                    counts[ch] += 1
                    papers[ch].add(paper_dir.name)

    return counts, {ch: sorted(pset) for ch, pset in papers.items()}


def char_display(ch: str) -> str:
    """Return a printable representation of a character with its Unicode name."""
    codepoint = f"U+{ord(ch):04X}"
    try:
        name = unicodedata.name(ch)
    except ValueError:
        name = "UNKNOWN"
    # Wrap the character in visible delimiters for terminals that swallow it.
    return f"'{ch}' [{codepoint}, {name}]"


def build_report(
    counts: Counter,
    papers: dict[str, list[str]],
    config: dict,
) -> str:
    """Build the audit report as a string."""
    char_subs = config["char_substitutions"]
    pattern_subs = config["pattern_substitutions"]

    lines: list[str] = []
    lines.append("=" * 78)
    lines.append("CHARACTER AUDIT REPORT")
    lines.append("=" * 78)
    lines.append(f"Total distinct non-ASCII characters: {len(counts)}")
    lines.append(f"Total non-ASCII character occurrences: {sum(counts.values())}")
    lines.append(f"Papers scanned: {len({p for ps in papers.values() for p in ps})}")
    lines.append("")

    # Split characters into normalized-in-config vs. pass-through.
    in_config: list[tuple[str, int]] = []
    pass_through: list[tuple[str, int]] = []
    for ch, n in counts.most_common():
        if ch in char_subs:
            in_config.append((ch, n))
        else:
            pass_through.append((ch, n))

    # --- Normalized characters ---
    lines.append("-" * 78)
    lines.append(f"Characters WITH single-char substitution rules ({len(in_config)}):")
    lines.append("-" * 78)
    if in_config:
        for ch, n in in_config:
            replacement = char_subs[ch]
            replacement_display = repr(replacement) if replacement else "(delete)"
            paper_list = papers[ch]
            n_papers = len(paper_list)
            lines.append(
                f"  {char_display(ch)}  x{n} in {n_papers} paper(s) -> {replacement_display}"
            )
    else:
        lines.append("  (none)")
    lines.append("")

    # --- Pass-through characters ---
    lines.append("-" * 78)
    lines.append(f"Characters WITHOUT substitution rules ({len(pass_through)}):")
    lines.append("-" * 78)
    if pass_through:
        for ch, n in pass_through:
            paper_list = papers[ch]
            n_papers = len(paper_list)
            lines.append(
                f"  {char_display(ch)}  x{n} in {n_papers} paper(s)  [pass-through]"
            )
    else:
        lines.append("  (none)")
    lines.append("")

    # --- Pattern substitutions listed for reference ---
    lines.append("-" * 78)
    lines.append(f"Pattern substitutions (regex) in config ({len(pattern_subs)}):")
    lines.append("-" * 78)
    if pattern_subs:
        for pattern, replacement in pattern_subs.items():
            lines.append(f"  {pattern!r} -> {replacement!r}")
    else:
        lines.append("  (none)")
    lines.append("")

    lines.append("=" * 78)
    lines.append("End of report.")
    lines.append("=" * 78)

    return "\n".join(lines)


def main() -> None:
    args = sys.argv[1:]

    output_path: Path | None = DEFAULT_REPORT_PATH
    paper_filter: str | None = None

    # Extract --output <path> if present.
    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 >= len(args):
            print("--output requires a path", file=sys.stderr)
            sys.exit(1)
        output_path = Path(args[idx + 1])
        args = args[:idx] + args[idx + 2:]

    if args:
        paper_filter = args[0]

    config = load_normalization_config()
    counts, papers = collect_characters(paper_filter)

    if not counts:
        print("No non-ASCII characters found.")
        return

    report = build_report(counts, papers, config)
    print(report)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"\nReport also written to: {output_path}")


if __name__ == "__main__":
    main()