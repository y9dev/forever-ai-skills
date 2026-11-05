# UX methodology (Stages 3 and 9)

## Task-first design
1. List user goals from the PRD, then the tasks behind each goal. Rank tasks by **frequency x importance**. Frequent tasks get the fewest steps and the most prominent entry points.
2. Derive screens from tasks. A page the user listed that supports no task is questioned; a task with no screen is a gap.
3. Information architecture: sitemap (max 2 navigation levels for MVP), primary navigation (5 to 7 items), per-role visibility, object model (entities and their relations as users see them), naming consistent with user vocabulary.
4. Screen structure for each important screen: purpose, primary action, content blocks in priority order, secondary actions, data shown (with default sort/filter), the four states below.

## State matrix (mandatory per screen/data view)
- **Loading:** skeleton or spinner within 100 ms; no layout shift on arrival.
- **Empty:** says why it is empty and offers the next action.
- **Success:** visible confirmation of what happened (toast, inline, redirect with message).
- **Error:** says what failed in plain words, keeps user input, offers retry or alternative; field errors next to fields; network failure distinct from validation failure.
Also: partial data, permission denied (403 view), not found (404 view), session expired.

## Journey specification (6 fields, per critical journey; see `templates/user-journey.md`)
Starting point; user action; system response; expected result; possible errors; recovery path. Write each step as a row. Include step count and the expected time for the happy path.

## Nielsen's 10 heuristics: check questions
1. Visibility of system status: does every action give feedback within 1 s; are long operations shown with progress?
2. Match with real world: labels in user language, not internal field names?
3. User control and freedom: undo, cancel, back, close; destructive actions reversible or confirmed?
4. Consistency and standards: same action looks and behaves the same everywhere; platform conventions followed?
5. Error prevention: constraints, defaults, disabled-with-reason states, confirmation for destructive acts, inline validation?
6. Recognition over recall: options visible, recent items, labeled icons, filters showing their current value?
7. Flexibility and efficiency: shortcuts, bulk actions, saved filters, sensible defaults for frequent users?
8. Aesthetic and minimalist design: nothing on screen that does not support the task?
9. Help users recover from errors: plain-language messages, specific cause, specific next step?
10. Help and documentation: only where needed; contextual hints, empty-state guidance.

## Cognitive load rules
Max about 7 items per navigation group; one primary action per screen; progressive disclosure for advanced options; group related fields; default values; avoid modal chains; tables show the 5 to 8 columns users actually scan with the rest on a detail view.

## Accessibility baseline (WCAG 2.2 AA targets)
Semantic landmarks and headings in order; every input with a visible label; all functions keyboard operable in logical tab order; visible focus indicator (at least 2 px or equivalent contrast); text contrast at least 4.5:1 (3:1 for large text and UI components); not color alone to convey state; touch targets at least 24x24 CSS px (44 preferred on mobile); dialogs trap and restore focus, Esc closes; live regions for async status; alt text for meaningful images; respects `prefers-reduced-motion`; page zoom to 200% without loss.

## Responsive baseline
Breakpoints per design system. Verify at 360, 768, 1280 px widths at minimum. Tables: horizontal scroll with sticky first column, or card layout on narrow screens. No horizontal page scroll. Navigation collapses accessibly.

## Audit conduct (Stage 9)
- Auditors execute the journeys as a first-time user would, with the actual app, noting steps, time, confusion, dead ends. They also try failure paths: invalid input, empty data, double submit, back button, refresh mid-flow, offline (if testable), forbidden pages.
- Evidence per finding: steps to reproduce, screenshot path or exact DOM/console/network observation.
- Severity: **Critical** = a primary journey cannot be completed or data loss; **High** = journey completable only with significant confusion or workaround, or an a11y barrier blocking a user group; **Medium** = noticeable friction or inconsistency; **Low** = polish.
- Preference is not a defect: a finding must name a heuristic, a measurable property (contrast ratio, target size, step count), or an observed user failure.
- Use `templates/ux-audit.md` for the output.
