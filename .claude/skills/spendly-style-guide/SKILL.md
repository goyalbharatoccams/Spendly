---
name: spendly-style-guide
description: Keep Spendly's visual theme consistent when editing or adding frontend pages
---

# Spendly Style Guide

Use this skill whenever you add a new page, update HTML/CSS, or make any frontend change to the Spendly Flask expense tracker.

**Read these companion files when relevant:**
- `refs/tokens.md` — full design token reference with usage examples
- `refs/components.md` — every reusable CSS class with copy-paste markup
- `refs/responsive.md` — breakpoints, mobile checklist, layout patterns
- `examples/new-landing-page.html` — boilerplate for hero/content pages
- `examples/new-auth-page.html` — boilerplate for login/register-style pages
- `examples/new-static-page.html` — boilerplate for terms/privacy-style pages
- `scripts/verify.ps1` — HTTP status check after changes
- `scripts/validate_theme.py` — detect hardcoded colors in templates and CSS

---

## Quick rules

1. Every page **extends `templates/base.html`** — no exceptions.
2. Title block: `{% block title %}Page Name — Spendly{% endblock %}`.
3. Use only `var(--token)` — never hardcode colors, fonts, or radii.
4. Before writing new CSS, check `refs/components.md` for an existing class.
5. New CSS goes in `static/css/style.css` under a `/* --- Section Name --- */` label.
6. New responsive rules go inside the **existing** `@media` blocks at the bottom of `style.css`.
7. After any change, run the verification steps below.

---

## Design tokens (quick reference)

Full table with usage examples → `refs/tokens.md`

| Token | Value | Use for |
|---|---|---|
| `--ink` | `#0f0f0f` | Primary text, filled button text |
| `--ink-soft` | `#2d2d2d` | Secondary text, headings |
| `--ink-muted` | `#6b6b6b` | Body copy, subtitles |
| `--ink-faint` | `#a0a0a0` | Placeholders, fine print |
| `--paper` | `#f7f6f3` | Page background |
| `--paper-warm` | `#f0ede6` | Alternate section background |
| `--paper-card` | `#ffffff` | Card backgrounds |
| `--accent` | `#1a472a` | Brand green — links, highlights |
| `--accent-light` | `#e8f0eb` | Green tint backgrounds |
| `--accent-2` | `#c17f24` | Amber accent |
| `--danger` | `#c0392b` | Errors, destructive actions |
| `--border` | `#e4e1da` | Card / input borders |
| `--font-display` | DM Serif Display | h1, h2, display text |
| `--font-body` | DM Sans | All body text and UI |
| `--max-width` | `1200px` | Content width cap |
| `--radius-sm/md/lg` | 6 / 12 / 20px | Buttons / cards / panels |

---

## Page structure

`base.html` provides automatically:
- Sticky navbar (brand + Sign in / Get started)
- `<main class="main-content">` wrapping `{% block content %}`
- Footer (brand, tagline, Terms / Privacy links)
- `static/css/style.css` globally
- `{% block head %}` — page-specific CSS (use only if >50 unique rules)
- `{% block scripts %}` — page-specific JS

---

## Spacing rhythm

| Context | Value |
|---|---|
| Section padding | `5rem 2rem` |
| Card padding | `2rem` |
| Element gap | `1rem – 1.5rem` |
| Content cap | `var(--max-width)` with `margin: 0 auto` |

---

## Adding a new page — checklist

- [ ] `{% extends "base.html" %}`
- [ ] `{% block title %}Name — Spendly{% endblock %}`
- [ ] Layout copied from the right file in `examples/`
- [ ] Headings use `var(--font-display)`; everything else uses `var(--font-body)`
- [ ] No hardcoded color values anywhere
- [ ] New route added to `app.py` if needed
- [ ] Responsive rules added inside existing `@media` blocks
- [ ] Verification passed (see below)

---

## Verification

```powershell
# Check HTTP 200 for a route
.\.claude\skills\spendly-style-guide\scripts\verify.ps1 -Route "/"

# Scan for hardcoded colors
python .\.claude\skills\spendly-style-guide\scripts\validate_theme.py
```

Manual fallback:
```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/<route>
```

Flask auto-reloads `.py` changes in debug mode. After adding **new routes**, restart manually:
```bash
python app.py
```