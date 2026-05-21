# Responsive Design Rules — Spendly

---

## Breakpoints

Two breakpoints exist in `static/css/style.css`. **Always add new rules inside these existing blocks** — never create new `@media` queries elsewhere in the file.

| Breakpoint | Purpose |
|---|---|
| `max-width: 900px` | Stack feature grid to 1 column; adjust multi-column layouts |
| `max-width: 600px` | Hide nav links, reduce hero padding, stack mockup stats, simplify forms |

---

## How to add responsive rules

Find the blocks at the very bottom of `style.css`:

```css
/* These blocks already exist — add inside them */

@media (max-width: 900px) {
  /* tablet / small desktop rules */
}

@media (max-width: 600px) {
  /* mobile rules */
}
```

**Never** scatter new `@media` declarations through the middle of `style.css`.

---

## Mobile-first checklist

Test at **375px viewport width** before committing any frontend change:

- [ ] All text is readable (min effective size ~14px, sufficient line-height)
- [ ] All tap targets are large enough (min 44px height for buttons and links)
- [ ] No horizontal overflow (nothing pushes past the viewport edge)
- [ ] Forms are usable — inputs not too small, labels visible above fields
- [ ] Multi-column cards stack to single column
- [ ] Images or mockup graphics scale or are hidden gracefully
- [ ] Navbar collapses properly (links hidden at 600px)

---

## Typography scaling

Use `clamp()` for responsive heading sizes to avoid abrupt jumps:

```css
/* Pattern used on the hero title */
font-size: clamp(1.8rem, 5vw, 3.5rem);

/* General pattern */
font-size: clamp(<min>, <fluid>, <max>);
```

---

## Common responsive layout patterns

### Grid → single column

```css
.my-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

@media (max-width: 900px) {
  .my-grid {
    grid-template-columns: 1fr;
  }
}
```

### Flex row → column

```css
.my-row {
  display: flex;
  gap: 1rem;
  align-items: center;
}

@media (max-width: 600px) {
  .my-row {
    flex-direction: column;
    align-items: stretch;
  }
}
```

### Reduce section padding on mobile

```css
@media (max-width: 600px) {
  .my-section {
    padding: 3rem 1.25rem;  /* reduce from 5rem 2rem */
  }
}
```

### Hide decorative elements on mobile

```css
@media (max-width: 600px) {
  .hero-mockup {
    display: none;
  }
}
```

---

## Viewport meta tag

Already included in `base.html` — do not add it again in child templates:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```