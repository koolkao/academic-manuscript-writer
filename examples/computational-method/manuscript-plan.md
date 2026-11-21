# Manuscript Plan — Computational Method Example (Synthetic Worked Example)

> Note: All dataset counts, sites, and performance metrics in this worked example are synthetic,
> created solely to illustrate the skill on a Markdown biomedical-AI methods manuscript ready for
> `.docx` (`wordcraft-cli`) + Zotero assembly. `draft-manuscript.md` is a compact ~1,400-word
> demonstration rather than a full-length submission.

- **Working title options:**
  1. Calibration-Preserving Structured Attention Pruning for a Cross-Site 12-Lead ECG Transformer
  2. Preventing Cross-Site Probability Drift During Attention-Head Pruning of a 12-Layer ECG Transformer
- **Field family & study type:** Computational & Machine Learning (Medical AI) — Retrospective multi-site external validation
- **Applicable reporting guideline:** TRIPOD+AI
- **Target venue & house style:** *npj Digital Medicine* — *Nature*-family style (unstructured summary abstract ≤ 150 words, declarative Results subheadings, separate lock-safe Data Availability and Code Availability headings, full submission main text ≤ 3,500 words, ≤ 5 main figures/tables).
- **Source depth inspected:** Illustrative synthetic benchmark tables embedded in this worked example (no external CSV files bundled in repo).

## Candidate Story Spines

### Spine A — Speedup / compression benchmark ("1.4x faster ECG transformer")
- **Tension:** ECG transformers have high CPU inference latency on edge devices.
- **Turn:** Prune 75% of attention heads for 1.4-fold CPU latency reduction (FFN blocks untouched) at similar AUROC.
- **One-sentence thesis:** Structured attention-head pruning reduces ECG transformer CPU latency 1.4-fold.
- **Evidence fit & primary risk:** Incremental compression benchmark; clinical-AI reviewers immediately challenge calibration and external-site risk reliability.

### Spine B — Preventing hidden cross-site calibration collapse under pruning (Selected)
- **Tension:** Standard magnitude and Taylor attention-head pruning preserve in-distribution and external AUROC in a 12-layer 12-lead ECG transformer while inflating external macro expected calibration error (ECE) threefold across hospitals, degrading thresholded risk estimates.
- **Turn:** Introduce a Brier calibration-sensitivity penalty (CalPrune) during structured head pruning using disjoint selection and temperature-scaling splits, and evaluate discrimination, macro 15-bin ECE, calibration slope/intercept, per-site performance, and ARM CPU latency across three external hospitals (n = 14,820 recordings from 11,240 patients).
- **One-sentence thesis:** Adding a Brier calibration-sensitivity penalty to structured attention-head pruning in a 12-layer ECG transformer retained external AUROC (0.931 vs. 0.934 dense) while reducing 75%-pruned external macro ECE from 0.054 to 0.019 (calibration slope 0.97 vs. 0.71) across three held-out hospitals (14,820 recordings) at the same 1.4-fold CPU latency reduction shared by 75%-pruned baselines.
- **Evidence fit & primary risk:** Grounded in internal-test, pooled external, and per-site tables plus matched disjoint-split temperature scaling; strictly scoped to retrospective archives and a 12-layer encoder transformer (`C04` is a `gap`).

## Selected Framing

- **Selected spine:** Spine B
- **One-sentence contribution:** Adding a Brier calibration-sensitivity penalty to structured attention-head pruning in a 12-layer ECG transformer retained external AUROC (0.931 vs. 0.934 dense) while reducing 75%-pruned external macro ECE from 0.054 to 0.019 (calibration slope 0.97 vs. 0.71) across three held-out hospitals (14,820 recordings) at the same 1.4-fold CPU latency reduction shared by 75%-pruned baselines.
- **Why this framing wins:** Elevates the paper from generic pruning to a clinically consequential failure mode verified on pooled and per-site external hospital metrics without exaggerating head-only latency speedups.

## Claims-Evidence Ledger

| ID | Claim (calibrated wording) | Evidence source | Exact values | Status | Target section |
| --- | --- | --- | --- | --- | --- |
| C01 | At 75% head sparsity, magnitude pruning kept single-model external AUROC near dense (0.928 vs. 0.934) while tripling external macro ECE (0.054 vs. 0.018) and flattening calibration slope (0.71 vs. 0.98) | Table 1 | Dense AUROC 0.934, ECE 0.018 (0.015–0.021), slope 0.98; MagPrune AUROC 0.928, ECE 0.054 (0.049–0.059), slope 0.71 | verified | Abstract, Results |
| C02 | CalPrune reduced 75%-pruned single-model external macro ECE to 0.019 (slope 0.97) while maintaining AUROC 0.931 across 14,820 recordings (11,240 patients) and all three individual external hospitals | Tables 1–2 | Pooled ECE 0.019 (0.016–0.022), AUROC 0.931 (0.925–0.937), slope 0.97; Site A ECE 0.018, Site B 0.021, Site C 0.019 | verified | Abstract, Results |
| C03 | Structured 75% attention-head pruning lowered single-model ARM Cortex-A76 CPU latency 1.4-fold (34.2–34.3 ms vs. 48.6 ms dense, FFN layers intact) across magnitude, Taylor, and CalPrune | Table 1 | 34.2–34.3 ms vs. 48.6 ms (1.4x) | verified | Abstract, Results |
| C04 | CalPrune reduces bedside emergency-department triage mortality or false-alarm workload in live clinical deployment | None — retrospective multi-site archives only | — | gap | Discussion — Scope and Limitations |

## Section Architecture

| Section | Core job | Key claims | Budget (words) | Main figures / tables |
| --- | --- | --- | --- | --- |
| Abstract | Unstructured *Nature*-style summary | C01, C02, C03 | 150 | — |
| Introduction | Edge ECG deployment need → masked calibration collapse → CalPrune summary | C01, C02 | 450 | Fig. 1 |
| Methods | Patient-disjoint splits, disjoint calibration split, CalPrune objective, multi-label ECE & slope definitions | — | 700 | — |
| Results | Internal test → external pooled collapse → CalPrune per-site stability & CPU latency | C01, C02, C03 | 900 | Figs. 1–2, Tables 1–2 |
| Discussion | Practical meaning → reliability-bin interpretation → proportionate scope → deployment next steps | C01–C03 | 600 | — |
