"""
Find all Greek eta subscript variants in MinerU markdown output.
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "markdown_output"

PATTERN = re.compile(r"\\eta\s*_\s*\{[^}]*\}\s*\^\s*\{\s*2\s*\}")


def main() -> None:
    if not INPUT_DIR.exists():
        print(f"No {INPUT_DIR}")
        return

    all_variants: dict[str, int] = {}

    for md in sorted(INPUT_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        matches = PATTERN.findall(text)
        if not matches:
            continue

        file_variants: dict[str, int] = {}
        for m in matches:
            file_variants[m] = file_variants.get(m, 0) + 1
            all_variants[m] = all_variants.get(m, 0) + 1

        rel = md.relative_to(INPUT_DIR)
        print(f"\n{rel}:")
        for variant, count in sorted(file_variants.items()):
            print(f"    {variant!r}  (x{count})")

    if not all_variants:
        print("\nNo \\eta patterns found in any file.")
        return

    print("\n" + "=" * 78)
    print("SUMMARY - unique variants across all papers:")
    print("=" * 78)
    for variant, count in sorted(all_variants.items(), key=lambda x: -x[1]):
        print(f"  {variant!r}  (total x{count})")


if __name__ == "__main__":
    main()
