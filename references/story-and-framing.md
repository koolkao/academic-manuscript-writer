# Story and framing

A scientific story is not marketing gloss or manufactured drama. It is the logical path a reader
needs to travel from an unresolved problem to a bounded, evidenced change in what the field knows,
measures, predicts, or does.

## 1. Source depth before diagnosis

Before proposing a storyline or diagnosing a weak draft, inspect the deepest available source:
methods, full results, tables, figure captions, and supplementary analyses.

- Never lock a story from a title, abstract, or bullet summary alone.
- If full methods or results are not supplied, list exactly what you inspected, mark the framing as
  **provisional (source-depth limited)**, and name the files or numbers needed to lock it.
- Separate **established findings** (directly measured in supplied outputs) from
  **interpretations** (inferences about mechanism or implication) and **gaps** (missing controls,
  untested groups, unmeasured confounders).

## 2. The Audience Contract

Every strong framing satisfies three readers at once:

| Reader | Core question | What loses them |
|---|---|---|
| **Handling editor** | Why does this matter to *this* journal's readership now? | Incremental positioning, buried contribution, mismatch between title and findings. |
| **Skeptical reviewer** | Is every central claim backed by the design, controls, and statistics shown? | Overclaimed causality, unacknowledged alternative explanations, cherry-picked baselines. |
| **Busy field reader** | What is the one thing I can now think, measure, or do differently? | Lab-chronology dumps, five competing sub-messages, opaque jargon. |

Do not optimize only for editor excitement (creates overclaiming) or only for reviewer safety
(creates an unreadable catalog).

## 3. Generate 2–4 candidate story spines

Whenever a study has multiple results or possible angles, draft **2–4 genuinely distinct candidate
framings** before selecting one. Each framing represents a different contribution type:

- **Empirical / clinical discovery:** an unexpected pattern, dose–response, risk stratification, or
  null/negative result that changes clinical or scientific belief.
- **Mechanistic insight:** *why* an observed effect occurs, identifying the mediating pathway,
  failure mode, or structural bottleneck.
- **Method / technical capability:** a cleaner, faster, better-calibrated, or more generalizable
  algorithm, assay, or analytical workflow — framed by the scientific obstacle it overcomes, not
  merely a leaderboard bump.
- **Resource / benchmark / synthesis:** a validated cohort, dataset, atlas, reporting standard, or
  conceptual reconciliation that unlocks downstream work.

For each candidate spine, write four crisp lines:
1. **Tension:** current belief or practice → specific consequential gap or bottleneck.
2. **Turn:** the decisive analysis, design, or method that resolves the gap.
3. **One-sentence thesis:** *"In [population/setting/system], [approach/observation] shows/is
   associated with [primary supported finding], establishing/suggesting [bounded advance]."*
4. **Evidence fit & risk:** which supplied results directly prove it, and what Reviewer #2 would
   attack first.

Recommend the strongest framing **supported by existing evidence**, explain why the alternatives
are weaker or require unavailable data, and **confirm the chosen spine with the author** before
drafting the full manuscript. Never force an honest exploratory or descriptive study into a fake
"existing methods fail dramatically" conflict.

## 4. The one-sentence contribution test

If you cannot state the paper's central contribution in one concrete, falsifiable sentence without
stacking three unrelated clauses, **stop drafting and fix the framing**.

- Weak: *"We analyze multimodal cohort data with deep learning and find several interesting
  associations with post-surgical recovery."*
- Strong: *"Across 1,420 adults followed after lumbar surgery, initiating multidisciplinary
  rehabilitation within 6 weeks was associated with a 4.1-point greater 12-month PROMIS physical
  function gain after immortal-time and propensity adjustment, with benefit concentrated in
  patients presenting with baseline neuropathic pain features."*

## 5. Reader logic beats laboratory chronology

Laboratory order ("First we tried A, it failed, then we collected B, then we ran 14 sensitivity
models") obscures the argument. Order sections and results by **what the reader must believe first**:

1. Establish the primary phenomenon or clinical/technical problem cleanly.
2. Present the main result answering the central question.
3. Test the decisive alternative explanations (confounders, ablations, negative controls).
4. Clarify mechanism, subgroups, or boundary conditions (where the effect holds and where it stops).
5. Move dead-end explorations, routine preprocessing checks, and secondary tables to the
   Supplement.

## 6. The Claims-Evidence Ledger (`C01`, `C02`, …)

For any full manuscript plan (`manuscript-plan.md` or existing project `PLAN.md`), build a compact
Claims-Evidence Ledger:

| ID | Claim (exact calibrated wording) | Evidence source (file / table / figure) | Exact values | Status | Target section |
|---|---|---|---|---|---|
| C01 | … | `results/table2.csv`, Fig. 2 | … | `verified` | Results — Primary Endpoint |

Status definitions:
- **`verified`**: directly confirmed in the supplied files or user-provided values.
- **`unverified`**: asserted in draft notes, not yet checked against source data — flag for author.
- **`gap`**: required to support a desired claim, but absent from current data. A `gap` claim must
  **never** be stated as an established finding in the manuscript; either narrow the claim or record
  the missing evidence in `revision-notes.md`.
