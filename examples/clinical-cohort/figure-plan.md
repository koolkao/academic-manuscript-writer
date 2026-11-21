# Figure Plan — Clinical Cohort Example

- **Manuscript:** Early Multidisciplinary Rehabilitation After Lumbar Surgery
- **Visual grammar (shared across all figures):**
  - *Palette (colorblind-safe):* Neuropathic phenotype (DN4 ≥ 4) = Okabe–Ito blue (`#0072B2`), Nociceptive-predominant phenotype (DN4 < 4) = Okabe–Ito orange (`#E69F00`), Delayed/usual comparator = neutral gray (`#7F8C8D`, non-Okabe–Ito), Landmark boundary = charcoal dashed (`#333333`).
  - *Dual encoding:* Solid lines + filled circles (neuropathic); dashed lines + open squares (nociceptive); direct labels.
  - *Typography & export:* Double-column width (175 mm), ≥ 8 pt post-scaling, vector SVG/PDF or 600-dpi PNG for `.docx` assembly via `wordcraft-cli`.

## Central Synthesis Figure (Optional — included here to clarify the 6-week landmark design)

- **Planned placement:** Figure 1 (anchoring Methods-to-Results transition)

### Concept 1 — Integrated Scientific Illustration
- **Core takeaway:** A fixed 6-week landmark aligns exposure classification before outcome accrual and links neuropathic phenotype to higher 12-month functional responder rates.
- **Panel layout & focal anchor:** Two-tier horizontal figure: top strip depicts the surgical-to-landmark timeline (`Surgery → Weeks 1–6 exposure classification → Week 6 landmark time zero → Month 12 PROMIS outcome`); bottom strip shows side-by-side responder proportions (individual MCID ≥ 3.0 points: 64.2% vs. 44.5% in DN4 ≥ 4).
- **Empirical boundary:** Top clinical timeline is `[conceptual schematic]`; bottom responder bars and 95% CIs are `[measured data]` (synthetic Table 2 outputs).
- **Key annotations & draft finding-first caption:** "Landmark time zero (Week 6; excludes early reoperations)", "Individual MCID responder (≥3.0 pts): 64.2% vs. 44.5%". *Caption:* Figure 1. Early multidisciplinary rehabilitation within 6 weeks after lumbar decompression is associated with higher 12-month physical function responder rates predominantly in patients with baseline neuropathic pain features.
- **Effort & tradeoff:** Medium effort; clean for generalist readers, though omits timing variation within weeks 1–6.

### Concept 2 — Comparative / Explanatory Layout
- **Core takeaway:** Naive post-surgery exposure classification introduces immortal time, whereas the 6-week landmark cleanly separates early-window initiation from downstream outcome follow-up.
- **Panel layout & focal anchor:** Split two-panel figure: Panel A contrasts naive exposure windows against the 6-week landmark design; Panel B shows IPTW-adjusted 12-month PROMIS score distributions for early vs. delayed groups across both phenotypes.
- **Empirical boundary:** Panel A is `[conceptual schematic]`; Panel B interval plots are `[measured data]` (synthetic Table 2 outputs).
- **Key annotations & draft finding-first caption:** "Landmark time zero eliminates immortal-time bias", "Interaction P = .004". *Caption:* Figure 1. Six-week landmark alignment prevents immortal-time bias and isolates phenotype-stratified 12-month functional gains.
- **Effort & tradeoff:** Low–medium effort; preempts methodological objections, though foregrounds epidemiologic bias over clinical responder magnitude.

### Concept 3 — Data-Led / Novel Relationship Visual
- **Core takeaway:** Among patients initiating rehabilitation before the 6-week landmark, estimated 12-month functional gains peak during weeks 3–5 (+8.4 points at week 4 vs +5.1 points at week 1) and translate into a 19.7-percentage-point higher individual MCID responder rate in patients with neuropathic pain.
- **Panel layout & focal anchor:** Three-panel double-column figure: Panel A (top strip, schematic) shows the 6-week landmark time zero; Panel B (bottom left, 55% width) plots IPTW-adjusted restricted cubic splines strictly within pre-landmark initiation weeks 1–6 (n = 512) stratified by DN4 phenotype; Panel C (bottom right, 45% width) shows 12-month individual MCID responder proportions (≥3.0-point gain, 95% CIs) by phenotype.
- **Empirical boundary:** Panel A is `[conceptual schematic]`; Panels B and C are `[measured data]` (synthetic primary and spline outputs).
- **Key annotations & draft finding-first caption:** "Pre-landmark initiation window only (Weeks 1–6)", "Peak week 4: +8.4 pts from baseline (5.7–11.1)", "Responder RD +19.7 pp (11.7–27.7 pp)". *Caption:* Figure 1. Early multidisciplinary rehabilitation within the 6-week landmark window is associated with higher 12-month PROMIS Physical Function mean and responder gains predominantly among patients with baseline neuropathic pain features (n = 1,420).
- **Effort & tradeoff:** Medium effort; resolves immortal-time concerns visually while presenting both continuous early-window timing and individual-level clinical responder rates.

### Selected Concept
- **Choice:** Concept 3 (Data-Led / Novel Relationship Visual)
- **Rationale:** Restricting the spline strictly to pre-landmark initiation weeks 1–6 prevents immortal-time reintroduction, while pairing it with Panel C separates individual MCID responder rates from group mean differences.

## Main Figure and Table Sequence

| Item | Question answered | Empirical boundary | Source data | Draft finding-first caption sentence |
| --- | --- | --- | --- | --- |
| Table 1 | Are early and delayed landmark groups balanced after IPTW? | `[measured data]` | Synthetic cohort baseline summary | Baseline characteristics of 1,420 lumbar decompression patients at the 6-week landmark with post-IPTW standardized mean differences. |
| Figure 1 | How is time zero defined, and how do early-window timing and individual MCID responder rates differ by phenotype? | Panel A `[conceptual schematic]`; Panels B–C `[measured data]` | Synthetic landmark + spline summary | Early multidisciplinary rehabilitation within the 6-week landmark window is associated with higher 12-month PROMIS Physical Function mean and responder gains predominantly among patients with baseline neuropathic pain features. |
| Figure 2 | Does the phenotype-specific pattern persist across subgroups and sensitivity analyses? | `[measured data]` | Synthetic subgroup + sensitivity summary | The 12-month physical function association for early rehabilitation persists across exploratory surgical subgroups, 8-week landmark alignment, and complete-case sensitivity analyses. |
| Table 2 | What are the exact adjusted mean, responder, interaction, and sensitivity estimates? | `[measured data]` | Synthetic landmark + E-value summary | Primary landmark, prespecified phenotype-interaction, responder, and sensitivity estimates for 12-month PROMIS Physical Function. |

## Standalone Sequence Test

Read Table 1 → Figure 1 → Figure 2 → Table 2 in order:
- **Does the sequence carry the full argument without Results prose?** Yes: Table 1 establishes covariate balance; Figure 1 shows landmark alignment, pre-landmark initiation timing, and individual responder divergence by DN4 phenotype; Figure 2 demonstrates stability across subgroups and sensitivity models; Table 2 supplies exact effect sizes, CIs, and E-values.
- **Moved to Supplement:** Screening and follow-up flow (Figure S1), full 24-covariate Love table (Table S1), multiple-imputation diagnostics (Table S2).

## Accessibility and Visual Audit Checklist

- [x] Colorblind-safe palette (Okabe–Ito blue/orange + neutral gray comparator) with solid/dashed dual encoding
- [x] Individual MCID responder proportions separated cleanly from group mean differences
- [x] Conceptual schematic (Fig. 1A) visibly separated from measured plots (Figs. 1B–C)
- [ ] Vector export and ≥ 8 pt post-scaling legibility verified on rendered graphics `[user-verify — text-only brief]`
