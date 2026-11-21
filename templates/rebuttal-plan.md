# Rebuttal Plan

- **Manuscript:** <Revised file path>
- **Decision / venue:** <e.g., Major Revision — Journal Name>
- **Summary strategy:** <2–3 sentences describing the main thrust of the revision>

## Atomic Reviewer Critiques

*(Status MUST use the unified vocabulary enforced by `check_manuscript.py`: `open | pending-author-data | resolved | narrowed | accepted-risk`. Use real unnumbered headings from the manuscript, never invented section numbers.)*

| ID | Reviewer & point | Type | Rung (1–6) / Pushback | Evidence anchor | Target manuscript location | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R1.1 | <Concise paraphrase of atomic critique> | Methodological challenge | Rung 5 (Reanalyze existing data) | <Table S2 / new sensitivity output> | Methods — Sensitivity Analyses; Results — Robustness | resolved |
| R1.2 | <...> | Claim/scope disagreement | Rung 4 (Narrow claim) | <Primary cohort scope> | Abstract; Discussion — Limitations | narrowed |
| R2.1 | <...> | Out-of-scope wishlist | Polite evidence-backed pushback | <Study design / primary aim> | Response letter only (no bloat added) | resolved |

## Promise-to-Edit Verification

- [ ] Every quantitative figure or new analysis mentioned in `response-letter.md` exists in the revised manuscript or Supplement with identical numbers.
- [ ] Every quoted passage in `response-letter.md` verified verbatim by `check_manuscript.py` (`REB-02`).
- [ ] All `pending-author-data` items resolved (zero fabricated results).
- [ ] `python3 <skill-dir>/scripts/check_manuscript.py <target>` re-run cleanly after all rebuttal edits.
