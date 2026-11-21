# Adversarial review protocol

Adversarial review catches desk-rejection triggers, methodological flaws, visual-empirical blurs,
and overclaimed inferences *before* submission — and maps each real vulnerability to the
lowest-effort defensible fix.

## 1. Fresh-context isolation and subagent brief

When reviewing a manuscript you helped plan or draft:

- **Run in a fresh subagent whenever the host supports subagents.**
- **Explicit file boundary:** Pass the manuscript file(s), supplied data/tables/figures, target
  venue, this protocol (`references/adversarial-review.md`), and the applicable reporting guideline
  note (`references/field-and-reporting.md`). **Explicitly exclude** `manuscript-plan.md` and
  `revision-notes.md` so the reviewer never inherits drafting rationalizations or sunk-cost framing.
- **Record an honest isolation manifest** at the top of `adversarial-review.md`: state
  `Fresh subagent`, `Same session (explicit adversarial pass)`, or `Illustrative worked example`,
  and list **only files that actually exist and were actually passed**.
- **Fresh re-verification of `FATAL` fixes:** Marking a `FATAL` item `resolved` requires citing the
  exact edited passage/heading in the updated file — and, for pre-submission sign-off, a second
  fresh-context check confirming the fix closes the hole without introducing a new one.
- Agent review is pre-submission triage, not domain peer review or formal biostatistical sign-off.

### Subagent Isolation Brief (copy/fill when launching)

```text
Role: Independent adversarial pre-submission reviewer ("Handling Editor + Reviewer #2").
Files to inspect:
  - Manuscript: <exact path>
  - Supplied data / tables / figures: <exact paths or "None beyond manuscript">
  - Target venue & house style: <journal/conference + reporting guideline>
  - Review protocol: <skill-dir>/references/adversarial-review.md
Explicitly excluded: manuscript-plan.md, revision-notes.md (do not read or infer from them).

Task:
1. Read the full manuscript and supplied tables/figures before forming any judgment.
2. Apply the four adversarial lenses and the per-claim attack procedure in adversarial-review.md.
3. Verify every candidate critique against the full manuscript text before ranking it; drop any
   finding already addressed in Methods, Tables, or Supplement.
4. Anchor every finding by exact heading, paragraph/line, table, or figure (never by plan claim IDs).
5. Write adversarial-review.md using templates/adversarial-review.md. Store Status ONLY in the
   Impact × Effort Decision Matrix, and never assign `accepted-risk` (that is the author's decision).
```

## 2. Attack the *current* file, verify findings, avoid theatre

1. **Audit the current draft as submitted**, never a retrospective story about how earlier drafts
   improved.
2. **Forced rejection pre-mortem (required):** Open with a **3-sentence rejection letter** a
   skeptical editor would send *today* for the current file, plus the **Top-3 ranked rejection
   risks** (most lethal first).
3. **Findings verification step (required before ranking):** Before emitting any finding, re-check
   the full manuscript (Methods, Results, Tables, Captions, Supplement pointers) to confirm the
   issue is genuinely present and unaddressed. Never log a "verification passed" check as a finding,
   and never report a false positive as `MAJOR`.
4. **Residual objections (no filler quotas):** When the review reports **zero open `FATAL` or
   `MAJOR` findings**, include a `## Residual Objections` section listing **up to three genuine
   non-blocking objections** (or `None` if none remain), explaining why each is non-blocking. Do
   not pad generic caveats just to hit a count.
5. **Anti-wishlist discipline:** Do not invent `FATAL` flaws on a clean paper, and do not grade
   "single-center observational cohort — run a multicenter RCT" as `FATAL` unless the manuscript
   claims causal proof or universal generalizability beyond its design. Attack the **gap between
   the claim and the evidence**, not finite resources.

## 3. Four adversarial lenses

### Lens 1 — Handling Editor (Desk-Rejection Filter)
- Can a generalist editor retell the contribution in one sentence from Title, Abstract, and
  Figure 1 alone?
- Does the Introduction establish a consequential gap for *this* venue now?
- Do Title, Abstract, Key Points, and Conclusions promise more than Results establish?
- Do main figures and captions carry a coherent standalone story?

### Lens 2 — Skeptical Methodologist / Biostatistician ("Reviewer #2")

Apply this **general 7-step per-claim attack procedure** to every headline claim in the manuscript:

1. **Estimand & scope:** What exact quantity, target population, and endpoint are claimed in the
   Title/Abstract/Conclusions, and do they match what the analysis actually estimated?
2. **Comparator & counterfactual:** Is the comparator contemporary, clinically/technically strong,
   and treated identically (e.g., equal calibration, tuning budget, follow-up window, or standard of
   care)?
3. **Time zero, exposure, & data splits:** Where does follow-up or evaluation begin? Check for
   immortal time, post-treatment conditioning, patient/site/temporal leakage, or hyperparameter /
   threshold / calibration fitting on the evaluation split.
4. **Selection & missingness:** Do eligibility rules condition on post-baseline outcomes or
   follow-up completion? Do attrition handling, imputation statements, and table denominators agree?
5. **Measurement & metric definition:** Are metrics defined unambiguously and applied at the right
   level (e.g., individual responder MCID vs. group mean difference; ensemble metrics vs.
   single-model latency; macro vs. per-class multi-label calibration; null CIs crossing zero)?
6. **Modeling, multiplicity, & arithmetic recomputation:** Check prespecification/registration of
   subgroups, clustering/repeated measures, and model assumptions. **Recompute** counts, `n (%)`,
   ratios, sensitivity bounds (e.g., continuous E-values via VanderWeele & Ding:
   `RR ≈ exp(0.91 × d)`, `E = RR + sqrt(RR × (RR − 1))`), and stated speedups/latencies strictly
   for verification (never insert recomputed numbers directly into manuscript prose).
   - *Plausibility note on subgroup pooling:* Comparing `Σ n_i × est_i / N` against an overall
     estimate is only a **rough plausibility check** for simple unweighted linear means. It does
     **not** hold identically for weighted estimators (IPTW/IPW), non-collapsible effect measures
     (odds ratios, hazard ratios), or inverse-variance precision-weighted pooling — verify the
     estimator before flagging a discrepancy.
7. **Strongest alternative explanation:** What single unaddressed confounder, batch/site artifact,
   hardware/implementation quirk, or design bias could reproduce the headline result?

**Design-specific triggers (illustrative examples, not an exhaustive checklist):**
- *Observational cohorts:* time-varying confounding between index event and landmark, immortal-time
  reintroduction in continuous timing splines, outcome-conditioned eligibility, unmeasured
  confounding sensitivity.
- *Randomized trials:* allocation concealment, intention-to-treat vs. per-protocol drift, outcome
  switching vs. registration, informative censoring, subgroup multiplicity.
- *Diagnostic / clinical prediction / ML:* patient/site-disjoint splits, calibration slope/intercept
  and decision-curve net benefit beyond AUROC, single-model vs. ensemble compute parity, matched
  post-hoc calibration across baselines, hardware-plausible speedups.
- *Systematic reviews / meta-analyses:* search/screening reproducibility, risk-of-bias weighting,
  heterogeneity (`I²` / prediction interval), small-study bias, overlapping cohorts.
- *Bench / experimental studies:* biological vs. technical replicates, blinding/randomization, batch
  effects, positive/negative controls, normalization and outlier exclusion criteria.

### Lens 3 — Busy Field Reader / Practitioner
- Read only Figures + Captions in sequence: where does comprehension break?
- Do `[conceptual schematic]` elements ever masquerade as `[measured data]` or imply prospective
  clinical utility from retrospective/in silico data?
- Where do uncited background statistics, opaque acronyms, or lab chronology erode trust?
- Are limitations proportionate to the study design and field norms?

### Lens 4 — Reporting, Ethics & Novelty Gate
- Are required venue declarations present under lock-safe headings (`Ethics Approval`,
  `Data Availability`, `Code Availability`, `Funding`, `Conflicts of Interest`,
  `AI-Use Disclosure`)?
- Are core items of the applicable reporting guideline (STROBE, CONSORT, TRIPOD+AI, PRISMA,
  ARRIVE) satisfied, including protocol/trial registration when claims use `"prespecified"`?
- **Novelty & priority claims:** Offline agents cannot verify priority against the full literature.
  Flag every *"first"*, *"novel"*, or *"no prior study"* claim as **`[user-verify]`**.

## 4. Severity rubric and mutually exclusive Submission Verdict

Every finding MUST cite an exact anchor in the manuscript (heading, paragraph/line, table, or
figure — never plan claim IDs) and quote or pinpoint the exact text/number.

- **`FATAL`** — Likely desk-reject or reject unless resolved (broken central claim, bias/leakage
  invalidating headline result, numerical contradiction in primary endpoint, ungrounded claim).
- **`MAJOR`** — Likely major revision (unaddressed alternative explanation, missing key metric or
  matched baseline, unsupported `"prespecified"` claim, unreadable central figure, overclaiming
  Abstract/Conclusion, missing core declarations).
- **`MINOR`** — Minor revision / polish (local clarity, notation/house-style drift, caption polish).

**Submission Verdict (four mutually exclusive, exhaustive tiers — evaluate in order):**
1. **`Hold — FATAL flaw unresolved (KILL / PIVOT)`** — One or more `FATAL` findings are `open` or
   `pending-author-data` (regardless of rung). State both the **Pivot path** (narrower honest claim
   supported today) and **Acquire path** (single decisive analysis/dataset).
2. **`Revise before submission (author reanalysis required)`** — Zero open `FATAL` findings, and
   one or more `MAJOR` findings are `pending-author-data` on Rung 5 or Rung 6.
3. **`Revise before submission (manuscript edits only)`** — Zero open `FATAL` findings, zero Rung
   5–6 `MAJOR` findings, and one or more `MAJOR` findings are `open` on Rungs 1–4.
4. **`Ready after minor fixes`** — Zero open `FATAL` and zero open `MAJOR` findings (include
   `## Residual Objections` with up to three genuine non-blocking objections, or `None`).

## 5. The 6-rung minimum-defensible-fix ladder & single-source status

Pair every `FATAL` and `MAJOR` item with the lowest-effort rung that resolves it:

| Rung | Fix type | Effort | Can the skill execute directly? |
|---|---|---|---|
| **1** | Clarify wording / report existing detail | Very low | Yes (from supplied materials) |
| **2** | Reorganize / signpost | Low | Yes |
| **3** | Redesign figure / table / caption | Low–Med | Yes (layout brief & caption) |
| **4** | Narrow or recalibrate the claim | Low | Propose; confirm with author for central claims |
| **5** | Analyze existing data | Medium | **No** — specify exact analysis and mark `pending-author-data` |
| **6** | Run new experiment / collect new data | High | **No** — mark `pending-author-data` (or pivot to Rung 4) |

**Single-source status rule:** Store each finding's status **ONLY in the `## Impact × Effort
Decision Matrix`** (do not duplicate `Status:` inline on narrative bullets).

**Unified status vocabulary** (shared with `rebuttal-plan.md` and enforced by `check_manuscript.py`):
- `open` — unaddressed (blocks submission if `FATAL`).
- `pending-author-data` — awaits author-computed Rung 5/6 output (blocks submission if `FATAL`;
  never fabricate results).
- `resolved (<locator>)` — fixed in the current manuscript, citing the exact heading/table/figure
  (required by `check_manuscript.py` for any resolved `FATAL`).
- `narrowed (<locator>)` — claim recalibrated to match existing evidence, citing the updated text.
- `accepted-risk` — **author-only decision** to submit with the boundary explicitly disclosed; a
  reviewer must never assign `accepted-risk` unilaterally.
