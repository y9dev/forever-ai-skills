# Design system methodology (Stage 4)

Check first: does the repo already have tokens, a theme, or a component library (Tailwind config, MUI/Chakra/shadcn, CSS variables)? If yes, document and extend it; do not replace it.

## What `DESIGN_SYSTEM.md` must define (concise, as tables)
1. **Color tokens** (semantic, not raw): background, surface, border, text-primary/secondary/disabled, primary, primary-hover, danger, warning, success, info, focus-ring. One neutral scale, one brand color, four status colors. Light theme required; dark only if requested. Every text/background pair listed with its contrast ratio: body text at least 4.5:1, large text and UI boundaries at least 3:1.
2. **Typography:** one family (system UI stack by default), a scale such as 12/14/16/20/24/32 px, weights 400/600, line heights (1.4 to 1.6 for body), numeric columns use tabular numerals.
3. **Spacing scale:** 4 px base: 4, 8, 12, 16, 24, 32, 48. Page gutters, section gaps and component padding use only scale values.
4. **Sizing:** control height 32 (dense) or 40 px (default); icon 16/20 px; sidebar 240 px; max content width; table row 40 to 48 px.
5. **Radius and shadow:** two radii (for example 4 and 8 px), two shadows (raised, overlay). No decorative gradients.
6. **Components with all states** (default, hover, focus-visible, active, disabled, loading, error where relevant): button (primary/secondary/ghost/danger), input, select, checkbox/radio, textarea, table (sortable header, row hover, selection, pagination, empty/loading rows), card, dialog (title, body, actions, focus trap), navigation (sidebar/top bar, active item), toast/alert/banner, badge/status chip, tabs, form layout.
7. **Breakpoints:** 640, 768, 1024, 1280 px, with the layout rule at each.
8. **Interaction:** feedback timings, loading patterns, confirmation patterns for destructive actions, keyboard behavior for composite widgets.
9. **Motion:** only functional transitions (100 to 200 ms), disabled under `prefers-reduced-motion`.

## Principles
Consistency over novelty. Hierarchy through size, weight and spacing, not decoration. One primary action per view. Information density by audience: admin and data-heavy apps use dense rows, clear column alignment (text left, numbers right), sticky headers, visible filters, status chips with text (not only color), and saved/sticky sort and filter state. Consumer apps use more whitespace and larger targets.
No animations, gradients, glassmorphism or illustrations unless they carry meaning.

## Implementation requirement
Tokens exist in code (CSS variables or theme file) and components consume tokens only. Raw hex values and pixel literals outside the token file are defects found in Stage 7/9.

## Hackathon profile
Tokens + the six core components (button, input, table, card, dialog, toast) + status chip. Pick an existing library (for example the one already in the repo, or a lightweight headless-plus-Tailwind setup) rather than hand-building everything.
