# Calibration-Preserving Structured Attention Pruning for a Cross-Site 12-Lead ECG Transformer

> Compact synthetic worked demonstration (~1,400 words; not a full-length journal submission)
> illustrating *Nature*-family style, Markdown + Zotero `references.bib`, lock-safe Declarations,
> and post-review rebuttal alignment. All dataset counts and performance metrics are illustrative
> fixtures.

## Abstract

Structured attention-head pruning lowers inference latency for 12-lead electrocardiogram (ECG)
transformers, yet its cross-site calibration impact remains underexamined. Across three external
hospitals (14,820 recordings; 11,240 patients), 75% magnitude head pruning of a 12-layer ECG
transformer preserved external AUROC (0.928 vs. 0.934 dense) while tripling macro expected
calibration error (ECE; 0.054 vs. 0.018) and lowering calibration slope (0.71 vs. 0.98). We
introduce CalPrune, combining cross-entropy sensitivity with a Brier calibration-sensitivity
penalty. At 75% sparsity, CalPrune retained single-model AUROC (0.931; 95% CI, 0.925–0.937) and
external ECE (0.019; 95% CI, 0.016–0.022; slope 0.97; site ECEs 0.018, 0.021, 0.019), matching
the 1.4-fold ARM CPU latency reduction of 75%-pruned baselines (34.2–34.3 ms vs. 48.6 ms dense,
feed-forward blocks intact). Calibration-aware pruning prevents silent probability distortion in
compressed ECG transformers.

## Introduction

Deploying transformer-based 12-lead ECG arrhythmia screening models on point-of-care devices
requires substantial reductions in compute and memory footprint. Structured attention-head pruning
delivers predictable wall-clock speedups on commodity processors without custom sparse kernels
[@michel2019heads], and prior medical-signal compression studies have evaluated pruned models
primarily using area under the receiver operating characteristic curve (AUROC).

Discrimination alone is insufficient for clinical risk stratification [@guo2017calibration]. When
screening workflows act on predicted arrhythmia probabilities, calibration determines whether fixed
decision thresholds maintain intended sensitivity and false-alert rates across institutions.
Evaluating standard magnitude and Taylor pruning of a 12-layer ECG transformer on external hospital
archives reveals a masked failure mode: at 75% head sparsity, external AUROC drops by 0.006, yet
macro-averaged ECE triples and calibration slope falls from 0.98 to 0.71 (Figure 1).

We introduce CalPrune, a structured attention-head pruning criterion that augments task-loss
sensitivity with a first-order Brier calibration-sensitivity penalty [@brier1950verification]
(Figure 1). We evaluate CalPrune on an internal test split and three external hospital ECG cohorts
comprising 14,820 recordings from 11,240 unique patients under patient-disjoint validation aligned
with TRIPOD+AI reporting recommendations [@collins2024tripodai].

## Methods

### Multi-Site Cohorts and Disjoint Validation Splits

Model development used 42,600 12-lead ECG recordings from 31,400 unique patients at one academic
medical center, partitioned at the patient level into training (70%), pruning-selection validation
(10%), post-hoc calibration validation (10%), and internal test (10%; 4,260 recordings). Separating
the pruning-selection split from the calibration split prevented temperature-scaling optimism on
the same validation records. External validation used 14,820 recordings from 11,240 unique patients
across three independent hospitals (Hospitals A, B, and C) acquired with distinct ECG hardware
vendors; external recordings were never accessed during training, pruning, hyperparameter
selection, or temperature scaling.

### Calibration-Sensitive Head Pruning and Metrics

Let $L_{\text{CE}}$ denote six-class multi-label binary cross-entropy and $L_{\text{Brier}}$ denote
macro-averaged empirical Brier score [@brier1950verification] on the pruning-selection validation
split. For each attention head $h$ with gating scalar $\alpha_h = 1$, CalPrune scores head
importance as:

$$s_h = \left|\frac{\partial L_{\text{CE}}}{\partial \alpha_h}\right| + \lambda \left|\frac{\partial L_{\text{Brier}}}{\partial \alpha_h}\right|$$

The weighting factor $\lambda$ was tuned once on the pruning-selection split (sensitivity in
Supplementary Figure S2). Heads with lowest $s_h$ were pruned in 15% increments (leaving
feed-forward network [FFN] blocks intact) followed by brief fine-tuning and post-hoc temperature
scaling [@guo2017calibration] fit exclusively on the disjoint calibration split. Dense, L1
magnitude-pruned, first-order Taylor-pruned, and CalPrune models all received identical
calibration-split temperature scaling.

To match single-model deployment latency, we evaluated individual single-model checkpoints trained
across five random initialization seeds rather than a five-model ensemble: Tables 1–2 report the
five-seed mean single-model metric with 95% patient-level stratified bootstrap confidence intervals
(1,000 resamples) pooled across the five single-model checkpoints, and across-seed standard
deviations are reported in Supplementary Table S1. Calibration was quantified via multi-label
macro-averaged 15-equal-width-bin ECE across all six rhythm classes together with logistic
calibration slope and calibration intercept.

## Results

### Standard Pruning Preserves AUROC While Degrading External Calibration

On the internal test split (n = 4,260 recordings), all 75%-pruned methods maintained single-model
AUROC within 0.004 of the dense model (0.946 dense vs. 0.942 magnitude, 0.943 Taylor, and 0.945
CalPrune), with modest internal ECE differences (0.014 dense vs. 0.024 magnitude and 0.015
CalPrune; Supplementary Table S1). Under cross-site shift across the 14,820 external recordings,
however, calibration diverged sharply (Table 1 and Figure 2).

The dense 12-layer ECG transformer achieved pooled external AUROC 0.934 (95% CI, 0.928–0.940),
macro ECE 0.018 (95% CI, 0.015–0.021), and calibration slope 0.98 (intercept −0.03). At 75% head
sparsity, magnitude pruning retained external AUROC 0.928 (95% CI, 0.922–0.934) while inflating
macro ECE threefold to 0.054 (95% CI, 0.049–0.059) and depressing calibration slope to 0.71
(intercept −0.24), indicating systematic overconfidence in high-probability bins (Figure 1 and
Figure 2). First-order Taylor pruning showed the same degradation (AUROC 0.930, ECE 0.046, slope
0.76) despite matched calibration-split temperature scaling (Table 1).

### CalPrune Maintains Pooled and Per-Site Calibration at Matched Head-Pruning Speed

Incorporating Brier calibration sensitivity preserved calibration from 30% through 75% sparsity
(Figure 2). At 75% sparsity, CalPrune achieved pooled external AUROC 0.931 (95% CI, 0.925–0.937),
macro ECE 0.019 (95% CI, 0.016–0.022), and calibration slope 0.97 (intercept −0.04; Table 1).

Per-site evaluation confirmed consistent calibration across all three external hospitals despite
differing arrhythmia prevalences (18.4% at Hospital A, 24.1% at Hospital B, and 15.2% at Hospital
C; Table 2). CalPrune held site-level ECE between 0.018 and 0.021 (slopes 0.95 to 0.98), whereas
magnitude pruning exceeded 0.049 ECE at every institution (Table 2). On an ARM Cortex-A76 CPU,
removing 75% of attention heads while leaving FFN layers intact reduced single-model, single-record
latency 1.4-fold from 48.6 ms (dense) to 34.2–34.3 ms across magnitude (34.3 ms), Taylor (34.2 ms),
and CalPrune (34.2 ms) equally without custom sparse kernels (Table 1).

**Figure 1.** Calibration-sensitive structured head pruning prevents cross-site probability drift
in a 75%-pruned 12-layer 12-lead ECG transformer. (a–b) Conceptual schematic of CalPrune head
scoring combining cross-entropy and Brier sensitivity. (c) Measured single-model external
reliability curves across three held-out hospitals (n = 14,820 recordings) showing high-confidence
bin overestimation under magnitude pruning (macro 15-bin ECE 0.054; slope 0.71) vs. preservation
under CalPrune (ECE 0.019; slope 0.97).

**Figure 2.** Standard pruning triples external expected calibration error while leaving AUROC
nearly flat, whereas CalPrune holds external calibration error near the dense model through 75%
sparsity. Curves show five-seed mean single-model estimates with 95% patient-level bootstrap
confidence intervals pooled across the five checkpoints over 14,820 external hospital recordings.

**Table 1.** Pooled external cross-site single-model discrimination, calibration (macro 15-bin ECE,
slope, intercept), and single-record ARM Cortex-A76 CPU latency at 75% attention-head sparsity
(n = 14,820 recordings across three held-out hospitals; FFN blocks intact; all methods include
matched calibration-split temperature scaling).

| Method | External AUROC (95% CI) | External ECE (95% CI) | Cal. Slope / Intercept | CPU Latency (ms) |
| --- | --- | --- | --- | --- |
| Dense (unpruned) | 0.934 (0.928–0.940) | 0.018 (0.015–0.021) | 0.98 / −0.03 | 48.6 |
| Magnitude pruning (75%) | 0.928 (0.922–0.934) | 0.054 (0.049–0.059) | 0.71 / −0.24 | 34.3 |
| Taylor pruning (75%) | 0.930 (0.924–0.936) | 0.046 (0.041–0.051) | 0.76 / −0.19 | 34.2 |
| CalPrune (75%, ours) | 0.931 (0.925–0.937) | 0.019 (0.016–0.022) | 0.97 / −0.04 | 34.2 |

**Table 2.** Per-site external validation single-model performance across three independent
hospitals at 75% attention-head sparsity (n = 14,820 recordings; 11,240 unique patients).

| Hospital (n recordings; prevalence) | Dense AUROC / ECE | MagPrune AUROC / ECE (Slope) | CalPrune AUROC / ECE (Slope) |
| --- | --- | --- | --- |
| Hospital A (n = 5,420; 18.4%) | 0.938 / 0.017 | 0.931 / 0.051 (0.73) | 0.935 / 0.018 (0.98) |
| Hospital B (n = 4,980; 24.1%) | 0.929 / 0.020 | 0.923 / 0.059 (0.68) | 0.927 / 0.021 (0.95) |
| Hospital C (n = 4,420; 15.2%) | 0.934 / 0.018 | 0.929 / 0.052 (0.72) | 0.931 / 0.019 (0.97) |

## Discussion

Compressing a 12-layer clinical ECG transformer with standard loss-based head pruning produces a
deceptive deployment risk: rank-order AUROC remains nearly unchanged while predicted probabilities
become systematically overconfident on external hospitals (calibration slope 0.71 vs. 0.98 dense).
Adding a Brier calibration-sensitivity penalty during head selection retains single-model external
macro ECE within 0.001 of the dense network across all three external hospitals while preserving
the 1.4-fold ARM CPU latency reduction shared by structured 75% attention-head pruning.

Rank-order metrics such as AUROC are invariant to monotonic logit stretching, so standard pruning
benchmarks overlook overconfidence in upper predicted-probability bins [@guo2017calibration].
External reliability curves showed extreme-bin overestimation under magnitude and Taylor pruning
even after matched calibration-split temperature scaling, indicating that scalar post-hoc rescaling
alone cannot fully recover distortion introduced when calibration-sensitive attention heads are
removed. Because clinical screening pathways frequently trigger downstream review at fixed
probability thresholds, reporting calibration slope, intercept, and per-site external ECE alongside
AUROC is necessary whenever compressed models are benchmarked for multi-site use
[@collins2024tripodai].

Evaluating individual single-model checkpoints rather than multi-seed ensembles also aligns
calibration metrics directly with the 34.2–34.3 ms single-model edge latency budget. Ensemble
averaging can mask single-model overconfidence while multiplying inference cost by the ensemble
size, so reporting single-model calibration and latency on the same deployment artifact provides a
direct basis for hardware-constrained model selection [@michel2019heads].

### Scope and Limitations

Evaluation relied on retrospective multi-site ECG archives rather than prospective bedside
deployment, so effects on clinician alert fatigue and patient outcomes remain unmeasured. Results
also apply to structured attention-head pruning in a 12-layer encoder transformer with intact FFN
blocks; extension to joint FFN pruning, convolutional backbones, quantized int8 weights, and
site-specific clinical net-benefit thresholds requires direct benchmarking prior to clinical
integration.

## Conclusion

In a 12-layer 12-lead ECG transformer evaluated retrospectively across 14,820 recordings from three
external hospitals, CalPrune preserved single-model cross-site probability calibration (macro ECE
0.019 vs. 0.054 under magnitude pruning; calibration slope 0.97 vs. 0.71) and discrimination
(AUROC 0.931) while maintaining the 1.4-fold ARM CPU latency reduction (34.2–34.3 ms vs. 48.6 ms)
of 75% structured attention-head pruning.

## Declarations

### Ethics Approval
Retrospective analysis of de-identified 12-lead ECG archives was approved with a waiver of informed
consent by the institutional review boards of the development and external validation centers
(synthetic worked-example declaration).

### Data Availability
Synthetic fixture summary tables supporting this worked example are included in the companion
repository; clinical ECG waveforms are governed by institutional data-use agreements.

### Code Availability
Pruning code and calibration evaluation scripts supporting this worked example are available in the
companion repository.

### Funding
No external funding supported this synthetic worked example.

### Conflicts of Interest
The authors declare no competing financial or nonfinancial interests.

### AI-Use Disclosure
AI-assisted drafting and consistency checking were used during manuscript preparation; all
technical claims, equations, and interpretations were verified by the authors.
