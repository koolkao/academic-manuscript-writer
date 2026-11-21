# Figure Plan — Computational Method Example

- **Manuscript:** Calibration-Preserving Structured Attention Pruning for a Cross-Site 12-Lead ECG Transformer
- **Visual grammar (shared across all figures):**
  - *Palette (colorblind-safe):* CalPrune (proposed) = Okabe–Ito blue (`#0072B2`), Magnitude pruning = Okabe–Ito vermilion (`#D55E00`), Taylor pruning = Okabe–Ito reddish purple (`#CC79A7`), Dense baseline = charcoal (`#222222`, non-Okabe–Ito neutral).
  - *Dual encoding:* Filled circles + solid line (CalPrune), open triangles + dashed line (Magnitude), open squares + dotted line (Taylor), horizontal reference line (Dense).
  - *Typography & export:* Double-column print width (175 mm), ≥ 8 pt post-scaling, vector SVG/PDF or 600-dpi PNG for `.docx` assembly via `wordcraft-cli`.

## Central Synthesis Figure

- **Planned placement:** Figure 1 (anchoring Introduction-to-Methods)

### Concept 1 — Integrated Scientific Illustration
- **Core takeaway:** CalPrune couples ECG attention-head pruning with a Brier calibration-sensitivity term so pruned 12-layer transformers preserve single-model risk probabilities across external hospitals.
- **Panel layout & focal anchor:** Left-to-right three-stage strip: (a) 12-lead ECG input and multi-head attention waveform map; (b) pruning gate comparing magnitude-only vs. calibration-sensitive head scoring; (c) external three-hospital reliability curve inset showing aligned vs. drifted predicted probabilities.
- **Empirical boundary:** Stages (a) and (b) are `[conceptual schematic]`; stage (c) reliability curves (ECE 0.054 vs. 0.019) are `[measured data]` (synthetic Table 1 summary). Explicitly **no** emergency-room monitor or clinical outcome icons.
- **Key annotations & draft finding-first caption:** "Retained calibration-sensitive heads", "External sites A–C (n = 14,820)", "ECE 0.019 vs. 0.054". *Caption:* Figure 1. Calibration-sensitive structured head pruning prevents cross-site probability drift in a 75%-pruned 12-layer 12-lead ECG transformer.
- **Effort & tradeoff:** Medium effort; intuitive for broad clinical-AI readers while strictly separating schematic architecture from measured external calibration.

### Concept 2 — Comparative / Explanatory Layout
- **Core takeaway:** Standard pruning looks safe on an AUROC plot while failing sharply on a calibration plot across the exact same external ECG recordings.
- **Panel layout & focal anchor:** Side-by-side paired diagnostic panels on identical 0–85% pruning sparsity x-axes: Panel A shows nearly flat AUROC curves (0.934 → 0.928); Panel B shows sharply diverging external ECE curves (0.018 → 0.054 for magnitude pruning vs. 0.019 for CalPrune).
- **Empirical boundary:** Both panels are 100% `[measured data]` (synthetic sparsity-curve summary).
- **Key annotations & draft finding-first caption:** "AUROC gap 0.006 (masked failure)", "3x ECE inflation under magnitude pruning", "75% sparsity operating point (34.2–34.3 ms CPU)". *Caption:* Figure 1. Standard pruning hides a threefold external calibration collapse behind nearly unchanged AUROC, whereas CalPrune preserves both discrimination and calibration across sparsity levels.
- **Effort & tradeoff:** Low effort (purely data-driven); delivers an instant visual contrast.

### Concept 3 — Data-Led / Novel Relationship Visual
- **Core takeaway:** CalPrune occupies the strict Pareto frontier across single-model CPU latency (ms), external AUROC, and external calibration error simultaneously across all three held-out hospitals.
- **Panel layout & focal anchor:** Single wide frontier chart mapping ARM CPU latency (x-axis, 48.6 ms down to 31.0 ms, FFN layers untouched) against external ECE (y-axis), with connected trajectories tracing 0% → 50% → 75% → 85% sparsity for each pruning family and per-site ECE inset.
- **Empirical boundary:** 100% `[measured data]` (synthetic latency and calibration summary).
- **Key annotations & draft finding-first caption:** "1.4x single-model CPU speedup at 75% head sparsity (34.2–34.3 ms, ECE 0.019)". *Caption:* Figure 1. At 75% attention-head sparsity (1.4-fold CPU latency reduction, 34.2–34.3 ms vs. 48.6 ms), CalPrune keeps external ECE within 0.001 of the dense transformer across three held-out hospitals.
- **Effort & tradeoff:** Low–medium effort; dense with quantitative information, though three metrics on one plane are harder to scan than paired panels.

### Selected Concept (Author Gate Confirmed)
- **Choice:** Concept 1 for Figure 1 (overview + external reliability contrast) paired with Concept 2's sparsity-curve diagnostic as Figure 2.
- **Rationale:** Splitting the mechanism schematic (Fig. 1a–b) + external reliability contrast (Fig. 1c) from full sparsity-vs-ECE/AUROC curves (Fig. 2) keeps every panel uncluttered and maintains a crisp boundary between `[conceptual schematic]` and `[measured data]`.

## Main Figure and Table Sequence

| Item | Question answered | Empirical boundary | Source data | Draft finding-first caption sentence |
| --- | --- | --- | --- | --- |
| Figure 1 | How does CalPrune work and what does external calibration look like at 75% sparsity? | Panels a–b `[conceptual schematic]`; Panel c `[measured data]` | Synthetic external reliability summary | Calibration-sensitive structured head pruning prevents cross-site probability drift in a 75%-pruned 12-layer ECG transformer. |
| Figure 2 | Does AUROC hide calibration degradation across sparsity levels, and does CalPrune prevent it? | `[measured data]` | Synthetic sparsity-frontier summary | Standard pruning triples external expected calibration error while leaving AUROC nearly flat, whereas CalPrune holds external calibration error near the dense model through 75% sparsity. |
| Table 1 | How do pruning baselines and CalPrune compare on pooled external single-model discrimination, calibration (ECE, slope, intercept), and ARM CPU latency? | `[measured data]` | Synthetic pooled external + latency summary | Pooled external cross-site single-model discrimination, calibration error, slope/intercept, and single-record ARM Cortex-A76 latency at 75% attention-head sparsity (n = 14,820 recordings). |
| Table 2 | Does CalPrune hold calibration across every individual external hospital despite differing prevalences? | `[measured data]` | Synthetic per-site external summary | Per-site external validation single-model performance across three independent hospitals at 75% attention-head sparsity (n = 14,820 recordings; 11,240 unique patients). |

## Standalone Sequence Test

Read Figure 1 → Figure 2 → Table 1 → Table 2 in order:
- **Does the sequence carry the full argument without Results prose?** Yes: Fig. 1 introduces the pruning penalty and 75% external reliability contrast; Fig. 2 exposes AUROC-vs-ECE divergence across sparsity; Table 1 summarizes pooled metrics and shared 1.4x head-pruning latency gains; Table 2 proves per-site stability across Hospitals A, B, and C.
- **Moved to Supplement (aligned verbatim with manuscript):** Internal test metrics and across-seed standard deviations (Table S1), and hyperparameter sensitivity on $\lambda$ (Figure S2).

## Accessibility and Visual Audit Checklist

- [x] Okabe–Ito palette (+ neutral charcoal baseline) with distinct marker shapes and line styles
- [x] Zero clinical-monitor or patient-outcome graphics (prevents visual overclaiming from retrospective data)
- [x] Single-model metrics matched to single-model latency with 95% patient-level bootstrap CIs (`n = 14,820`)
- [ ] Vector export and ≥ 8 pt labels at 175 mm verified on rendered plots `[user-verify — text-only brief]`
