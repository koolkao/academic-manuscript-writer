# Revision, field-calibrated limitations, and peer-review responses (`respond` mode)

## 1. Field-calibrated proportional limitations

Present completed scientific work positively and accurately — neither apologetic nor evasive.

- **Keep internal diagnosis more exhaustive than published prose.** Capture every secondary caveat
  and future direction in `adversarial-review.md` or `revision-notes.md`.
- **Calibrate published limitations to field norms:**
  - *Clinical / epidemiological studies (STROBE item 19, CONSORT, TRIPOD+AI):* Include a full,
    direct limitations paragraph addressing sources of bias, imprecision, and direction/magnitude of
    potential confounding (~20–35% of Discussion; `check_manuscript.py` warns above 35%).
  - *Computational / ML / bench papers:* Keep limitations crisp and bounded (~10–25% of
    Discussion; `check_manuscript.py` warns above 25%) without defensive padding.
- **Include an omission in published prose when it:**
  1. materially changes how a reader should interpret a main finding;
  2. defines the legitimate boundary of a central claim (observational design, retrospective
     multi-site archive, single architecture family);
  3. is required by the applicable reporting guideline; or
  4. directly answers a specific reviewer critique.
- **Pair each limitation with what bounds or mitigates it** (sensitivity model, E-value, baseline
  comparability). Never imply an unperformed check was completed.

## 2. Responding to peer review (`respond` mode)

Responding to real reviewer reports is distinct from pre-submission red-teaming. Always produce
**two paired artifacts**: `rebuttal-plan.md` (strategy + verification ledger) AND
`response-letter.md` (point-by-point submission letter).

### Step 1 — Atomic decomposition (`rebuttal-plan.md`)
Split long reviewer paragraphs into numbered, single-issue critiques (`E1`, `R1.1`, `R1.2`,
`R2.1`, …) so no nested sub-question goes unanswered.

### Step 2 — Classify and choose the minimum defensible fix
For each atomic critique, assign:
- **Type:** `Factual error / bug` | `Methodological challenge` | `Missing analysis` | `Claim/scope
  disagreement` | `Clarity / presentation` | `Out-of-scope wishlist`
- **Fix-ladder rung (1–6) or polite pushback:** Clarify (1) → Reorganize (2) → Redesign figure (3)
  → Narrow claim (4) → Reanalyze existing data (5) → New experiment (6) — or **Polite,
  evidence-backed pushback** when a reviewer misread the text or requested an out-of-scope
  experiment.
- **Evidence anchor & unified status:** Use the exact same vocabulary as `adversarial-review.md`
  (`open | pending-author-data | resolved | narrowed | accepted-risk`, enforced by
  `check_manuscript.py` `REB-01`). Never invent extra statuses like `complete` or `wontfix`. If a
  Rung 5/6 analysis has not been run by the author, mark it **`pending-author-data`** — never
  fabricate numbers or placeholder "results were unchanged" prose.

### Step 3 — Draft the point-by-point response letter (`response-letter.md`)
Use `templates/response-letter.md`. For every critique:
1. Reproduce the reviewer's exact comment (or concise, faithful quote).
2. Lead with the **direct answer and action taken** in sentence 1 (skip repetitive "Thank you for
   this insightful comment" openers).
3. Supply concise scientific rationale and exact quantitative evidence.
4. Quote the **exact revised manuscript passage** using the **real heading/table/figure locator**
   present in the file (never invent section numbers like `§2.2` when the manuscript is unnumbered).

### Step 4 — Promise-to-edit verification (automated + manual)
Before finalizing `response-letter.md`:
- Run `check_manuscript.py`: rule **`REB-02`** mechanically verifies that every quoted revised
  passage (`> "..."`) in `response-letter.md` exists verbatim in the revised manuscript (normalized
  for whitespace/Markdown emphasis).
- Verify manually that every promised table, figure, or Supplement addition exists with identical
  numbers, and surface any remaining `pending-author-data` items as blocking submission.

## 3. The Integrated Consistency Sweep ("sweep, don't patch")

Whenever a sample size, metric, table, figure order, claim boundary, terminology choice, or
response-letter promise changes:

1. **Run `scripts/check_manuscript.py`** (path relative to the skill directory):
   ```bash
   python3 <skill-dir>/scripts/check_manuscript.py <manuscript-or-project-dir> \
     [--stage draft|submission] [--bib manuscript-refs.json|zotero.json|references.bib]
   ```
   - Use `--stage draft` on working drafts with deliberate `[PENDING: ...]` markers and
     `--stage submission` before final build/submission.
   - Resolve every `FAIL`, or suppress a verified false-positive rule with `--accept <RULE_ID>`
     and record why in `revision-notes.md`. Pass `--style` only if you also want optional
     prose/acronym/causal-verb lints.
2. **Manual semantic sweep across every coupled surface:**
   - Title ↔ Abstract / Summary ↔ Key Points / Highlights ↔ Cover Letter
   - Intro objective ↔ Results headline values ↔ Discussion ¶1 ↔ Conclusion
   - Every Figure & Table caption ↔ body text discussion ↔ Supplement pointers
   - Revised manuscript ↔ `response-letter.md` quotes and locators (if responding to reviews)
3. **Report honestly** in `revision-notes.md` (or `STATUS.md`) what was checked automatically, what
   was checked semantically, and what still awaits author action.
