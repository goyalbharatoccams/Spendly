#!/usr/bin/env python3
"""
validate_theme.py — Detect hardcoded colors in Spendly templates and CSS.

Scans templates/ and static/css/ for hex color literals and common named
colors that should be replaced with CSS custom properties (design tokens).

Usage (run from project root):
    python .claude/skills/spendly-style-guide/scripts/validate_theme.py

Exit codes:
    0  — no violations found
    1  — one or more violations found
"""
import re
import sys
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

SCAN_DIRS = [
    Path("templates"),
    Path("static/css"),
    Path("static/js"),
]

SCAN_EXTENSIONS = {".html", ".css", ".js"}

# Hex values that ARE allowed — the token definitions inside :root {}
# and intentional decorative colors with no token equivalent.
ALLOWED_HEX = {
    "#0f0f0f", "#2d2d2d", "#6b6b6b", "#a0a0a0",   # ink scale
    "#f7f6f3", "#f0ede6", "#ffffff",                # paper scale
    "#1a472a", "#e8f0eb", "#c17f24", "#fdf3e3",    # accent
    "#c0392b", "#fdecea", "#e4e1da", "#eeebe4",    # danger / border
    "#ece9e3", "#e2dfd9",                           # mockup browser chrome
    "#e8a838", "#4a90d9", "#7b6cc4",                # chart category bars
    "#f5c6c2",                                      # danger border
    "#ff5f57", "#ffbd2e", "#28c840",                # macOS chrome dots (decorative)
    "#000",                                         # video modal backdrop
}

# Named colors that should not appear in CSS property values
FLAGGED_NAMED = {
    "black", "white", "red", "green", "blue",
    "gray", "grey", "orange", "yellow", "purple",
}

# Lines matching these patterns are skipped (comments, token definitions)
SKIP_PATTERNS = [
    re.compile(r"^\s*(/\*|\*|<!--|-->|{#|#})"),   # comment lines
    re.compile(r"--[\w-]+\s*:"),                    # CSS custom property definitions
]

HEX_RE   = re.compile(r"(?<![&\w])#([0-9a-fA-F]{3,8})\b")
NAMED_RE = re.compile(
    r"(?:color|background|border|fill|stroke)[^:]*:\s*(" +
    "|".join(FLAGGED_NAMED) +
    r")\b",
    re.IGNORECASE,
)

# ── Scanner ────────────────────────────────────────────────────────────────────

def should_skip(line: str) -> bool:
    return any(p.search(line) for p in SKIP_PATTERNS)


def scan() -> list[str]:
    issues: list[str] = []

    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for path in sorted(scan_dir.rglob("*")):
            if path.suffix not in SCAN_EXTENSIONS or not path.is_file():
                continue

            text = path.read_text(encoding="utf-8", errors="ignore")
            for lineno, line in enumerate(text.splitlines(), 1):
                if should_skip(line):
                    continue

                # Hex colors
                for match in HEX_RE.finditer(line):
                    value = match.group(0).lower()
                    if value not in ALLOWED_HEX:
                        issues.append(
                            f"{path}:{lineno}  hardcoded hex {value}"
                            f"\n           -> replace with the matching var(--token)"
                        )

                # Named colors in property values
                named_match = NAMED_RE.search(line)
                if named_match:
                    issues.append(
                        f"{path}:{lineno}  named color '{named_match.group(1)}'"
                        f"\n           -> replace with the matching var(--token)"
                    )

    return issues


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    print("Scanning for hardcoded colors...\n")
    issues = scan()

    if not issues:
        print("  All good — no hardcoded colors found.")
        sys.exit(0)

    print(f"  {len(issues)} violation(s) found:\n")
    for issue in issues:
        print(f"  {issue}\n")

    print(
        "Design token reference: "
        ".claude/skills/spendly-style-guide/refs/tokens.md"
    )
    sys.exit(1)


if __name__ == "__main__":
    main()