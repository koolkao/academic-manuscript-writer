# Rebuttal Plan — Computational Method Example (Simulated Post-Review Round)

- **Manuscript:** `examples/computational-method/draft-manuscript.md`
- **Decision / venue:** Major Revision — *npj Digital Medicine* (simulated post-submission peer review; distinct from pre-submission adversarial red-team items)
- **Summary strategy:** Address Reviewer 1's per-site reporting and calibration-slope requests directly in Table 1 and Table 2, clarify disjoint validation splits in Methods, and provide concise evidence-backed pushback to Reviewer 2's out-of-scope prospective clinical deployment trial request.

## Atomic Reviewer Critiques

| ID | Reviewer & point | Type | Rung (1–6) / Pushback | Evidence anchor | Target manuscript location | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R1.1 | Reviewer 1: Report calibration slope and intercept alongside ECE, and break down performance separately for each external hospital rather than pooled only | Missing analysis | Rung 5 (Reanalyze existing data — completed by author) | Table 1 (slopes 0.97 vs. 0.71) and Table 2 (per-site ECEs 0.018, 0.021, 0.019) | Results — Standard Pruning Preserves AUROC / CalPrune Maintains Pooled and Per-Site Calibration; Table 1; Table 2 | resolved |
| R1.2 | Reviewer 1: Confirm that hyperparameter selection ($\lambda$) and post-hoc temperature scaling were not fit on the same validation subset | Clarity / presentation | Rung 1 (Clarify wording) | 70% train / 10% pruning-selection / 10% calibration / 10% internal test, patient-disjoint | Methods — Multi-Site Cohorts and Disjoint Validation Splits | resolved |
| R2.1 | Reviewer 2: Conduct a 12-month prospective randomized clinical deployment trial measuring emergency-department alert fatigue and patient outcomes | Out-of-scope wishlist | Polite evidence-backed pushback + Rung 4 (Narrow claim) | Retrospective TRIPOD+AI external validation scope; live clinical deployment requires separate prospective trial protocol and IRB | Discussion — Scope and Limitations; `response-letter.md` | narrowed |

## Promise-to-Edit Verification

- [x] Every quantitative token cited in `response-letter.md` (`0.054`, `0.019`, `0.97`, `0.71`, `0.018`, `0.021`, `5,420`, `4,980`, `4,420`, `42,600`, `4,260`) appears verbatim in both `response-letter.md` and `draft-manuscript.md` / Tables 1–2.
- [x] Every quoted passage in `response-letter.md` verified verbatim by `check_manuscript.py` (`REB-02`).
- [x] Every manuscript locator in `response-letter.md` matches the exact Markdown headings in `draft-manuscript.md`.
- [x] `python3 scripts/check_manuscript.py examples/computational-method` passes with 0 FAIL.
