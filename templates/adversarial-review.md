# Adversarial Review

- **Manuscript inspected:** <Exact file path>
- **Isolation manifest:** <Fresh subagent | Same session (explicit adversarial pass) | Illustrative worked example> — Files passed: `<list exact existing manuscript + data/table/figure files>`. Excluded: `manuscript-plan.md`, `revision-notes.md`.
- **Target venue & house style:** <Journal / conference; e.g., JAMA Network Open (AMA)>
- **Scope note:** Agent adversarial review is pre-submission triage, not domain peer review or formal biostatistical sign-off.

## Forced Rejection Pre-Mortem

**Simulated 3-sentence rejection letter (for the current draft as written):**
> <Sentence 1: editorial framing/fit or headline flaw.> <Sentence 2: decisive methodological or evidentiary gap.> <Sentence 3: why the journal cannot send it out or accept it as written.>

**Top-3 ranked rejection risks:**
1. <Most lethal risk + exact heading/table/figure anchor>
2. <Second risk + exact anchor>
3. <Third risk + exact anchor>

## Submission Verdict

- **Verdict:** <Hold — FATAL flaw unresolved (KILL / PIVOT) | Revise before submission (author reanalysis required) | Revise before submission (manuscript edits only) | Ready after minor fixes>

## Four-Lens Critique

*(Status is tracked ONLY in the Impact × Effort Decision Matrix below. Every finding below must have been verified against the full manuscript text before ranking.)*

### Lens 1 — Handling Editor (Desk-Rejection Filter)
- **[MAJOR] E01 — <Short title>** (`<Exact heading / line / figure>`): <Quote or observation>. *Risk:* <Why editor rejects>. *Minimum fix:* Rung <1–6> — <Concrete action>.

### Lens 2 — Skeptical Methodologist / Biostatistician ("Reviewer #2")
- **[FATAL] M01 — <Short title>** (`<Exact heading / line / table / figure>`): <Quote or numerical/design issue>. *Risk:* <Why inference breaks>. *Minimum fix:* Rung <1–6> — <Concrete action>.

### Lens 3 — Busy Field Reader / Practitioner
- **[MINOR] R01 — <Short title>** (`<Exact heading / figure>`): <...>. *Minimum fix:* Rung <1–6> — <...>.

### Lens 4 — Reporting, Ethics & Novelty Gate
- **[MAJOR] G01 — <Declarations / reporting item>** (`<Exact heading>`): <Missing lock-safe declaration, registration, or EQUATOR item>. *Minimum fix:* Rung 1 — <Concrete action>.
- **[INFO] G02 — Novelty / priority claims requiring author verification `[user-verify]`:** <Quote any "first", "novel", or "no prior study" claims for author literature check, or state `None`>.

## Impact × Effort Decision Matrix

*(Single source of truth for finding status. Reviewer must never assign `accepted-risk` — that is an author-only decision. Any `resolved` FATAL must include an exact locator.)*

| ID | Severity | Rung (1–6) | Priority tier | Minimum defensible fix | Status |
| --- | --- | --- | --- | --- | --- |
| M01 | FATAL | 5 (Analyze existing data) | Essential before submission | <Concrete fix> | pending-author-data |
| E01 | MAJOR | 2 (Reorganize / signpost) | Essential before submission | <Concrete fix> | open |
| R01 | MINOR | 1 (Clarify wording) | Useful improvement | <Concrete fix> | open |

## Residual Objections (Include when zero FATAL/MAJOR items remain open; list up to 3 genuine objections or `None`)

1. **<Objection 1>** (`<Exact heading / table / figure>`): <What a tough Reviewer #2 could still argue, and why it is non-blocking>.

## Kill-Switch / Pivot Analysis (Include if any FATAL item is `open` or `pending-author-data`)

- **Pivot path (existing data):** <Narrower honest claim supported today>
- **Acquire path (new analysis/data):** <Single decisive analysis/experiment required>
