---
name: hackathon-pitch-builder
description: Structures hackathon presentations and demo scripts for maximum judge impact. This skill should be used when preparing the final pitch, creating the presentation deck, writing the demo script, or organizing the Google Drive submission with all required materials.
argument-hint: "[minutes] [project description]"
---

# Hackathon Pitch Builder

Build winning hackathon presentations with optimal structure, compelling narratives, and demo scripts that create WOW moments.

## When to Use This Skill

- When preparing the final hackathon presentation
- When structuring your pitch for maximum impact in any length (default 3 minutes, set with the `minutes` argument)
- When creating demo scripts with wow moments
- When organizing Google Drive submission materials
- When rehearsing and refining your pitch

## Pitch Length (parameter)

The pitch length in minutes is an argument: `/hackathon-pitch-builder 5 <project description>`.

1. Take the first number in the arguments as `T` minutes. Accept forms like `5`, `5 min`, `5m`, `5 минут`, `2.5`. Ignore other numbers (team size, prizes) that are not next to a time word unless the first token is a bare number.
2. If no length is given, ask the user once for the length; if they do not answer or the context is non-interactive, use the default `T = 3`.
3. Clamp to a sensible range of 1 to 15 minutes. Outside it, confirm with the user.
4. Scale every duration in this skill from the 3-minute baseline: `new = baseline x T / 3`. Round to 5 seconds. Show the computed timeline to the user and use it in all later steps. The shares are: hook 1/12, problem 1/6, solution 1/6, demo 5/12, scale 1/12, ask 1/12.
5. Shape adjustments: under 2 minutes merge Scale into the Ask and keep one demo moment; from 6 minutes up the demo may show up to two flows, still never more, and the slide count may grow by one per extra 2 minutes.

## Pitch Structure (baseline 3 minutes; scale to `T`)

Timestamps below are for `T = 3`. Recompute them for the requested length.

```
[0:00 - 0:15]  HOOK — Start with a shocking statistic or story
[0:15 - 0:45]  PROBLEM — What's broken and who suffers
[0:45 - 1:15]  SOLUTION — What you built and how it works
[1:15 - 2:30]  DEMO — Show it working LIVE
[2:30 - 2:45]  SCALE — "Here's what happens at 1000x"
[2:45 - 3:00]  ASK — What you need next
```

## Instructions

When a user asks to build their hackathon pitch, first fix the pitch length `T` (see "Pitch Length"). All durations in the steps and the slide table below are 3-minute baselines; scale them by `T / 3`.

### Step 1: Craft the Hook (15 seconds)

Choose one hook type:

| Hook Type | Template | Example |
|-----------|----------|---------|
| **Shocking stat** | "Did you know [stat]?" | "India loses ₹5-15 Crore DAILY to wrong addresses" |
| **Story** | "Meet [persona]. They [pain point]." | "Meet Priya, a Tier-3 seller losing 25% of deliveries" |
| **Question** | "What if [inversion]?" | "What if every address had a credit score?" |
| **Demo-first** | Start with live demo, explain after | Show the heatmap, then explain what it is |

### Step 2: Frame the Problem (30 seconds)

Required elements:
```markdown
- WHO has this problem? [Specific user with numbers]
- HOW BAD is it? [Cost in ₹ or % or time wasted]
- WHY hasn't it been solved? [Current gap]
- WHY NOW? [Technology/regulation/market enabler]
```

### Step 3: Present the Solution (30 seconds)

Structure:
```markdown
- ONE sentence: "We built [product name] — [one-line description]"
- Show the architecture diagram (keep it simple, 4-5 boxes max)
- State the core insight: "Our key insight is [simplification cascade or collision result]"
```

### Step 4: Live Demo (75 seconds — MOST IMPORTANT)

```markdown
Demo Script Template:

1. [Show the starting state — "Here's a typical problem scenario"]
2. [Trigger the core feature — "Now watch what happens when..."]
3. [Show the WOW moment — "Notice how it automatically..."]
4. [Show the result — "This saved X% / ₹Y / Z hours"]
5. [Show scalability — "And at national scale, this means..."]
```

**Demo rules:**
- Pre-load data so nothing hangs
- Have a backup video recording in case live demo fails
- Show ONE flow beautifully, not five flows poorly
- End on a visual highlight (chart, map, animation)

### Step 5: Scale Story (15 seconds)

```markdown
"At [current scale], we [demonstrated result].
At [national scale], this means [impact in ₹ or lives].
Our architecture supports this because [one technical reason]."
```

### Step 6: The Ask (15 seconds)

```markdown
"We need [specific thing] to take this to production:
- [Data partnership / API access / pilot customer / funding amount]"
```

## Presentation Slide Template

| Slide | Content | Time (baseline 3 min, scale by T/3) |
|-------|---------|------|
| 1 | Title + Team + Hook stat | 15s |
| 2 | Problem (who, how bad, why unsolved) | 30s |
| 3 | Solution (one-liner + architecture) | 15s |
| 4 | LIVE DEMO (switch to app) | 75s |
| 5 | Impact + Scale | 15s |
| 6 | Business Model (revenue streams) | 10s |
| 7 | Ask / Next Steps | 10s |

## Google Drive Checklist

Things that must be in the Drive for submission:
- [ ] Final presentation (PPT/PDF)
- [ ] Demo video recording (backup)
- [ ] Source code link (GitHub)
- [ ] README.md with setup instructions
- [ ] Architecture diagram (PNG/SVG)
- [ ] Team photo/info

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Starting with "Hi, we are team X" | Start with the hook instead |
| Showing 5 features quickly | Show 1 feature beautifully |
| Reading slides | Talk to judges, slides are visual aids |
| Demo fails live | Always have backup video |
| Ending with "thank you" | End with the ASK — what you need next |
| Spending too long on the problem | Keep it to about 1/6 of the pitch — judges know the problem exists |

## Remember

- Judges remember the DEMO, not the slides
- One WOW moment > five okay moments
- Practice the demo 5 times before presenting
- Always have a backup video
- End with a clear, specific ask
