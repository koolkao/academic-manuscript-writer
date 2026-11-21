# Manuscript Plan — Clinical Cohort Example (Synthetic Worked Example)

> Note: All cohort counts and statistics in this worked example are synthetic, created solely to
> illustrate the skill's structure, AMA house style, mathematical consistency, and verification
> workflow. `draft-manuscript.md` is a compact ~1,350-word demonstration rather than a full
> 3,000-word journal submission.

- **Working title options:**
  1. Early Multidisciplinary Rehabilitation and 12-Month Physical Function After Lumbar Surgery: A Two-Center Landmark Cohort Study
  2. Postoperative Multidisciplinary Rehabilitation Timing and 12-Month Functional Recovery by Neuropathic Pain Phenotype
- **Field family & study type:** Clinical / Epidemiological — Retrospective observational cohort (6-week landmark design)
- **Applicable reporting guideline:** STROBE
- **Target venue & house style:** *JAMA Network Open* — AMA style (`P < .001`, percentage points for risk differences, Unicode `≥`, `−`, structured abstract ≤ 250–350 words, Key Points ≤ 100 words, full submission main text ≤ 3,000 words, ≤ 5 main figures/tables).
- **Source depth inspected:** Illustrative synthetic cohort summary tables embedded in this worked example (no external CSV files bundled in repo).

## Candidate Story Spines

### Spine A — Broad timing effect ("earlier rehab helps everyone")
- **Tension:** Postoperative rehabilitation referral timing after lumbar decompression varies without consensus.
- **Turn:** Compare initiation within 6 weeks against delayed initiation.
- **One-sentence thesis:** Early rehabilitation within 6 weeks improves 12-month physical function after lumbar surgery.
- **Evidence fit & primary risk:** Overstates causality ("improves") and misses the effect modification by baseline neuropathic pain phenotype.

### Spine B — Phenotype-stratified early landmark window (Selected)
- **Tension:** Multidisciplinary postoperative rehabilitation is resource-constrained, and prior trials did not stratify referral timing by baseline neuropathic pain phenotype.
- **Turn:** Anchor cohort eligibility at a fixed 6-week landmark (n = 1,420; multiple imputation for missing 12-month outcomes) and test the interaction between early (≤6-week) initiation and preoperative Douleur Neuropathique 4 (DN4) phenotype.
- **One-sentence thesis:** Across 1,420 adults reoperation-free at 6 weeks after lumbar decompression, initiating multidisciplinary rehabilitation within 6 weeks was associated with a 4.1-point greater 12-month PROMIS Physical Function gain (95% CI, 2.3 to 5.9; P < .001), with larger mean and responder-level gains concentrated among patients with baseline neuropathic pain features (interaction P = .004).
- **Evidence fit & primary risk:** Grounded in landmark primary model (weighted plausibility check `(584×7.2 + 836×1.9)/1,420 = 4.08 ≈ 4.1`), responder MCID analysis, pre-landmark initiation-week spline (weeks 1–6 only: +8.4 [5.7 to 11.1] at week 4 vs +5.1 [2.2 to 8.0] at week 1), and exact VanderWeele & Ding E-value sensitivity (`d = 0.59 → RR = 1.71 → E = 2.81`, lower CI `2.04`); remaining vulnerabilities are comparator pooling, surgery-to-landmark time-varying confounding (`pending-author-data`), and missing registration ID for `"prespecified"`.

### Spine C — Health-system cost savings
- **Tension:** Delayed referrals increase downstream 24-month surgical episode spending.
- **Turn:** Model 24-month cost savings from faster rehabilitation pathways.
- **One-sentence thesis:** Early multidisciplinary rehabilitation reduces 24-month surgical episode costs.
- **Evidence fit & primary risk:** Fails evidence check — 24-month claims cost data were not collected (`C05` is a `gap`).

## Selected Framing (Author Gate Confirmed)

- **Selected spine:** Spine B
- **One-sentence contribution:** Across 1,420 adults reoperation-free at 6 weeks after lumbar decompression, initiating multidisciplinary rehabilitation within 6 weeks was associated with a 4.1-point greater 12-month PROMIS Physical Function gain (95% CI, 2.3 to 5.9; P < .001), with larger mean and responder-level gains concentrated among patients with baseline neuropathic pain features (interaction P = .004).
- **Why this framing wins:** Captures the strongest verified signal (neuropathic phenotype modification), pairs mean differences with individual responder proportions, and keeps claims strictly observational.

## Claims-Evidence Ledger

| ID | Claim (calibrated wording) | Evidence source | Exact values | Status | Target section |
| --- | --- | --- | --- | --- | --- |
| C01 | Early rehabilitation (≤6 weeks) was associated with a 4.1-point greater 12-month PROMIS Physical Function gain in IPTW landmark analysis | Table 2 | +4.1 points (95% CI, 2.3 to 5.9; P < .001; n = 1,420) | verified | Abstract, Results |
| C02 | Baseline neuropathic phenotype (DN4 ≥ 4) modified the association on both mean score and individual MCID responder rate | Fig. 1C, Table 2 | DN4 ≥ 4 (n = 584): +7.2 points (95% CI, 4.9 to 9.5), MCID responder 64.2% vs. 44.5% (+19.7 percentage points, 95% CI, 11.7 to 27.7); DN4 < 4 (n = 836): +1.9 points (95% CI, −0.4 to 4.2); interaction P = .004 | verified | Abstract, Results |
| C03 | Within the pre-landmark early window (weeks 1–6, n = 512), estimated within-group 12-month gain from baseline peaked for initiation between weeks 3 and 5 in the neuropathic subgroup | Fig. 1B | +8.4 points from baseline (95% CI, 5.7 to 11.1) at week 4 vs +5.1 points from baseline (95% CI, 2.2 to 8.0) at week 1 (n = 512) | verified | Results, Fig. 1 |
| C04 | Association persisted in complete-case (n = 1,292), 8-week landmark (+3.6; 95% CI, 1.7 to 5.5), and E-value sensitivity checks | Table 2, Fig. 2 | Complete-case n = 1,292 (+3.9; 95% CI, 2.0 to 5.8); 8-week landmark +3.6 (95% CI, 1.7 to 5.5); SMD d = 0.59, E-value = 2.81 (lower CI, 2.04) | verified | Results, Table 2 |
| C05 | Early multidisciplinary referral reduces 24-month downstream medical costs | None — claims cost data not collected | — | gap | Excluded from manuscript |

## Section Architecture (Full-Submission Budgets)

| Section | Core job | Key claims | Budget (words) | Main figures / tables |
| --- | --- | --- | --- | --- |
| Abstract | Structured AMA summary | C01, C02, C04 | 250–300 | — |
| Introduction | Clinical gap → prior literature limits → objective | C01, C02 | 450 | — |
| Methods | Landmark design, imputation, interaction, E-value conversion | — | 700 | Table 1, Fig. S1 |
| Results | Cohort balance → primary + phenotype interaction + responder MCID → pre-landmark timing & sensitivity | C01–C04 | 850 | Figs. 1–2, Tables 1–2 |
| Discussion | Main meaning → literature reconciliation → STROBE item 19 limitations → bounded implications | C01–C04 | 750 | — |
