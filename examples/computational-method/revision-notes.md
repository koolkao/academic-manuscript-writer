# Revision Notes — Computational Method Example

- **Original file:** None (new synthetic worked demonstration)
- **Draft / structural output:** `examples/computational-method/draft-manuscript.md` (compact ~1,350-word demonstration)
- **Scope of pass:** Full blueprint + *Nature*-style Markdown draft + illustrative adversarial red-team + post-review rebuttal + integrated sweep

## Substantive Changes Applied

1. **Aligned single-model metrics with single-model deployment latency:** Replaced five-seed ensemble probability averaging with five-seed mean single-model metrics (95% patient-level bootstrap CIs pooled across the five single-model checkpoints, across-seed SD in Table S1) so reported calibration and 34.2–34.3 ms ARM Cortex-A76 latency measure the exact same single-model artifact.
2. **Corrected latency attribution and Table 1 parity:** Stated `34.2–34.3 ms` across magnitude (`34.3 ms`), Taylor (`34.2 ms`), and CalPrune (`34.2 ms`) equally (1.4-fold speedup with FFN layers intact), matching Table 1 verbatim.
3. **Scoped Title, Abstract, and Conclusion strictly to a 12-layer ECG transformer and balanced Discussion:** Expanded main Discussion interpretation so `### Scope and Limitations` accounts for ~21% of Discussion (honestly within the ≤ 25% computational bound).
4. **Separated lock-safe declaration headings and verified verbatim rebuttal quotes:** Split `Data Availability` and `Code Availability` into distinct headings (`DEC-01`/`DEC-02`) and verified all `response-letter.md` quoted passages verbatim against `draft-manuscript.md` (`REB-02`).

## Unresolved Decisions & `pending-author-data` Items

- **`M01` (`pending-author-data` — Essential):** Run per-class calibration-split temperature scaling on saved magnitude-pruned logits and add to Supplementary Table S1.
- **`E01` / `G01` (`pending-author-data` — High-value):** Add decision-curve net-benefit plot (`Fig. S3`) plus demographic subgroup fairness, sample-size note, and missing-lead handling for full TRIPOD+AI reporting.
- **`R01` (`open`) & `G02` (`[user-verify]`):** Name the six ECG rhythm classes inline in Methods and verify 2025–2026 literature novelty before submission.

## Field-Calibrated Limitations Rationale

- **Included in published manuscript (1 concise paragraph, ~21% of Discussion):** Retrospective archive scope (no live alert-fatigue or outcome testing) and single 12-layer encoder-transformer architecture (intact FFN layers, unquantized).
- **Kept internal:** Alternative edge SoCs beyond ARM Cortex-A76.

## Integrated Consistency Check

- **Automated check:** `python3 scripts/check_manuscript.py examples/computational-method` → 0 FAIL; 1 expected `REV-05` WARN (`open MAJOR M01`, `pending-author-data`); `REB-02` verified all 3 quoted passages in `response-letter.md` verbatim.
- **Structural preservation check:** Not applicable (new synthetic draft); lock-safe declaration headings verified via `academic-humanizer/scripts/preservation_check.py` live mutation test (`Ethics Approval`, `Data Availability`, `Code Availability`, `Funding`, `Conflicts of Interest`, `AI-Use Disclosure`).

## Prioritized Next Actions

1. **Essential:** Run `M01` per-class temperature scaling check and add the six rhythm class names (`R01`).
2. **High-value improvement:** Add decision-curve net benefit (`E01`) and TRIPOD+AI subgroup/missing-lead details (`G01`).
3. **Optional polish:** Run `academic-humanizer` (`edit` or `voice` mode) using `protect-terms.txt`, then assemble `.docx` via `sync-refs.mjs` + `build-docx.py` (`wordcraft-cli run` + `wordcraft-cli zotero refresh`).

## Handoff to academic-humanizer

- **Input file for humanizer:** `examples/computational-method/draft-manuscript.md` (after `M01` / `R01`)
- **Workflow mode:** standalone (`draft-manuscript.revised.md` + `draft-manuscript.changes.md`; promote to `.keys.md` after approval)
- **Protect file:** `examples/computational-method/protect-terms.txt` (pass via `--protect`)
- **Recommended mode:** `edit` (or `voice` with author's prior computational paper)
- **Target venue & house style:** *npj Digital Medicine* (*Nature*-family style)
- **Locked one-sentence thesis:** Adding a Brier calibration-sensitivity penalty to structured attention-head pruning in a 12-layer ECG transformer retained single-model external AUROC (0.931 vs. 0.934 dense) while reducing 75%-pruned external macro ECE from 0.054 to 0.019 (calibration slope 0.97 vs. 0.71) across three held-out hospitals (14,820 recordings) at the same 1.4-fold single-model CPU latency reduction shared by 75%-pruned baselines.
- **Protected claim boundaries:**
  - Retrospective multi-site validation only: never claim prospective bedside clinical efficacy or alert-fatigue reduction.
  - Scope claims to single-model evaluation of the 12-layer encoder transformer with intact FFN blocks.
  - Attribute the 1.4-fold latency speedup (34.2–34.3 ms vs. 48.6 ms) to 75% structured attention-head pruning across all pruned methods, not CalPrune uniquely.
- **Locked declaration headings (do not edit):** `Ethics Approval, Data Availability, Code Availability, Funding, Conflicts of Interest, AI-Use Disclosure`
- **Open items for author (do not guess in prose pass):** `M01`, `E01`, `G01`, `R01`, `G02`.
