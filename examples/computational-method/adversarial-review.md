# Adversarial Review — Computational Method Example

- **Manuscript inspected:** `examples/computational-method/draft-manuscript.md`
- **Isolation manifest:** Illustrative worked example (modeled on fresh-subagent isolation) — Files inspected: `examples/computational-method/draft-manuscript.md`, `examples/computational-method/references.bib`. Excluded: `manuscript-plan.md`, `revision-notes.md`.
- **Target venue & house style:** *npj Digital Medicine* (*Nature*-family style)
- **Scope note:** Agent adversarial review is pre-submission triage, not formal peer review.

## Forced Rejection Pre-Mortem

**Simulated 3-sentence rejection letter (for the current draft as written):**
> While CalPrune improves expected calibration error and calibration slope over magnitude and Taylor head pruning across three external ECG datasets, all baselines use single-scalar temperature scaling rather than per-class Platt or vector scaling for this six-class multi-label task. In addition, the clinical consequence of lowering ECE from 0.054 to 0.019 is not quantified through decision-curve net benefit or demographic subgroup fairness required under TRIPOD+AI. Without a stronger multi-label post-hoc recalibration comparator and clinical utility / subgroup reporting, the editorial board views the methodological advance as incomplete.

**Top-3 ranked rejection risks:**
1. Missing stronger multi-label post-hoc calibration comparator (per-class temperature / vector scaling) (`Methods — Calibration-Sensitive Head Pruning and Metrics`).
2. Absence of decision-curve net benefit and TRIPOD+AI demographic subgroup/fairness reporting (`Results` & `Methods`).
3. Single 12-layer encoder transformer architecture limits breadth (`Discussion — Scope and Limitations`).

## Submission Verdict

- **Verdict:** Revise before submission (author reanalysis required) — zero open `FATAL` findings, but one `MAJOR` item (`M01`) requires Rung 5 author reanalysis (`pending-author-data`) before final submission lock.

## Four-Lens Critique

*(Status is tracked ONLY in the Impact × Effort Decision Matrix below. All findings below were verified against the full manuscript text.)*

### Lens 1 — Handling Editor (Desk-Rejection Filter)
- **[MINOR] E01 — Clinical consequence of ECE gap (0.054 vs 0.019) could be made concrete** (`Results`): Adding a decision-curve net benefit plot across plausible clinical screening thresholds (5%–20%) translates ECE directly into false-alert savings. *Minimum fix:* Rung 5 (Analyze existing data) — add decision-curve net benefit curve to Supplement (`Fig. S3`) using saved external predictions.

### Lens 2 — Skeptical Methodologist / Biostatistician ("Reviewer #2")
- **[MAJOR] M01 — Post-hoc baseline uses single-scalar temperature scaling rather than per-class Platt/vector scaling** (`Methods — Calibration-Sensitive Head Pruning and Metrics`): For a six-class multi-label ECG classifier, a single shared temperature scalar may under-serve magnitude pruning compared with per-class temperature scaling. *Risk:* Reviewers may argue per-class post-hoc calibration closes the ECE gap without changing head pruning. *Minimum fix:* Rung 5 (Analyze existing data) — evaluate per-class calibration-split temperature scaling on saved magnitude-pruned logits and report in Supplementary Table S1.

### Lens 3 — Busy Field Reader / Practitioner
- **[MINOR] R01 — List the six arrhythmia rhythm labels explicitly in Methods** (`Methods — Calibration-Sensitive Head Pruning and Metrics`): Text references `"six rhythm classes"` without naming them. *Minimum fix:* Rung 1 (Clarify wording) — list the six rhythm classes inline once confirmed from dataset metadata.

### Lens 4 — Reporting, Ethics & Novelty Gate
- **[MINOR] G01 — Partial TRIPOD+AI gaps remaining** (`Methods` & `Results`): Core items (patient-disjoint splits, internal test, per-site external validation, separate lock-safe Declarations) are present, but demographic subgroup/fairness metrics, sample-size justification, and missing-lead handling should be added to the Supplement to complete TRIPOD+AI reporting. *Minimum fix:* Rung 1 / Rung 5.
- **[INFO] G02 — Novelty / literature check `[user-verify]`:** Author to verify whether any 2025–2026 ECG pruning paper combined Brier sensitivity with structured head pruning prior to submission.

## Impact × Effort Decision Matrix

| ID | Severity | Rung (1–6) | Priority tier | Minimum defensible fix | Status |
| --- | --- | --- | --- | --- | --- |
| M01 | MAJOR | 5 (Analyze existing data) | Essential before submission | Run per-class temperature scaling on saved magnitude-pruned logits and report in Table S1 | pending-author-data |
| E01 | MINOR | 5 (Analyze existing data) | High-value improvement | Add decision-curve net-benefit plot (Fig. S3) from saved external predictions | pending-author-data |
| G01 | MINOR | 5 (Analyze existing data) | High-value improvement | Add demographic subgroup fairness, sample-size note, and missing-lead handling for TRIPOD+AI completeness | pending-author-data |
| R01 | MINOR | 1 (Clarify wording) | Useful improvement | List the six ECG rhythm classes explicitly in Methods | open |
