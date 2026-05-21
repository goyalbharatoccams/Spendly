# Design Tokens — Spendly

Defined in `static/css/style.css` under `:root { }`. Always reference via `var(--token-name)`. Never hardcode values these tokens already cover.

---

## Color — Text

| Token | Value | Use |
|---|---|---|
| `--ink` | `#0f0f0f` | Primary text, filled button labels |
| `--ink-soft` | `#2d2d2d` | Secondary text, card headings |
| `--ink-muted` | `#6b6b6b` | Body copy, subtitles, descriptions |
| `--ink-faint` | `#a0a0a0` | Placeholders, captions, fine print |

**Hierarchy rule:** Use `--ink` for high-emphasis text, `--ink-muted` for supporting text. Rarely use `--ink-soft` directly — it is between the two.

---

## Color — Backgrounds

| Token | Value | Use |
|---|---|---|
| `--paper` | `#f7f6f3` | Default page background (set on `body`) |
| `--paper-warm` | `#f0ede6` | Alternate section background (features, bands) |
| `--paper-card` | `#ffffff` | Card and modal backgrounds |

---

## Color — Brand & Accent

| Token | Value | Use |
|---|---|---|
| `--accent` | `#1a472a` | Brand green — primary links, focus rings, hover states |
| `--accent-light` | `#e8f0eb` | Green tint background (badges, tags, highlights) |
| `--accent-2` | `#c17f24` | Amber — secondary accent, stat labels |
| `--accent-2-light` | (light amber) | Amber tint backgrounds |

---

## Color — Feedback

| Token | Value | Use |
|---|---|---|
| `--danger` | `#c0392b` | Error messages, destructive action buttons |
| `--danger-light` | (light red) | Error background tint |

---

## Color — Borders

| Token | Value | Use |
|---|---|---|
| `--border` | `#e4e1da` | Card borders, input borders |
| `--border-soft` | (lighter) | Subtle dividers, section separators |

---

## Typography

| Token | Value | Use |
|---|---|---|
| `--font-display` | `'DM Serif Display', Georgia, serif` | `h1`, `h2`, large display headings |
| `--font-body` | `'DM Sans', system-ui, sans-serif` | All body text, labels, buttons, nav |

**Rule:** `--font-display` is for headings only. `--font-body` is the default on `body` — everything else inherits it automatically.

---

## Layout

| Token | Value | Use |
|---|---|---|
| `--max-width` | `1200px` | Max content width — pair with `margin: 0 auto` |
| `--auth-width` | `440px` | Auth/form container max-width |

---

## Border Radius

| Token | Value | Use |
|---|---|---|
| `--radius-sm` | `6px` | Buttons, tags, small chips |
| `--radius-md` | `12px` | Cards, inputs, dropdowns |
| `--radius-lg` | `20px` | Large panels, modals, hero mockup |

---

## Usage examples

```css
/* Correct — tokens only */
.expense-card {
  background: var(--paper-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--ink-muted);
  font-family: var(--font-body);
  padding: 2rem;
}

.expense-card h2 {
  font-family: var(--font-display);
  color: var(--ink-soft);
}

.expense-card:hover {
  border-color: var(--accent);
}

/* WRONG — hardcoded values */
.expense-card {
  background: #ffffff;        /* → var(--paper-card) */
  border-color: #e4e1da;      /* → var(--border) */
  color: #6b6b6b;             /* → var(--ink-muted) */
  border-radius: 12px;        /* → var(--radius-md) */
  font-family: 'DM Sans';     /* → var(--font-body) */
}
```