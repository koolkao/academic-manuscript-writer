# Early Multidisciplinary Rehabilitation and 12-Month Physical Function After Lumbar Surgery: A Two-Center Landmark Cohort Study

> Compact synthetic worked demonstration (~1,350 words; not a full 3,000-word journal submission)
> illustrating AMA house style, Markdown + Zotero `references.bib`, lock-safe Declarations, and
> verification workflow. All cohort counts and estimates are illustrative fixtures.

## Key Points

**Question:** Is initiating multidisciplinary rehabilitation within 6 weeks after lumbar
decompression associated with greater 12-month physical function, and does baseline neuropathic
pain phenotype modify this association?

**Findings:** In this two-center 6-week landmark cohort of 1,420 adults, early rehabilitation was
associated with a 4.1-point greater 12-month PROMIS Physical Function gain (P < .001). Gains were
concentrated in patients with baseline neuropathic pain features (+7.2 points; responder difference
19.7 percentage points; prespecified interaction P = .004).

**Meaning:** Baseline neuropathic pain screening may help stratify early multidisciplinary referral
windows pending prospective randomized evaluation.

## Abstract

**Importance:** Optimal timing and patient selection for multidisciplinary rehabilitation after
lumbar decompression remain uncertain.

**Objective:** To evaluate whether initiating multidisciplinary rehabilitation within 6 weeks is
associated with greater 12-month physical function and whether baseline neuropathic pain modifies
this association.

**Design, Setting, and Participants:** Two-center retrospective landmark cohort of 1,420 adults
undergoing elective lumbar decompression (2019–2024) alive and reoperation-free at week 6. Missing
12-month scores (9.0%) were multiply imputed.

**Exposure:** Multidisciplinary rehabilitation intake within 6 weeks (n = 512) vs delayed/usual
care (n = 908).

**Main Outcomes and Measures:** Twelve-month PROMIS Physical Function T-score change and individual
responder rate (≥3.0-point gain), estimated via inverse probability of treatment weighting (IPTW).

**Results:** Among 1,420 patients (mean age 58.4 years; 52.1% female), early rehabilitation was
associated with +4.1 PROMIS points (95% CI, 2.3 to 5.9; P < .001). Baseline neuropathic pain
(DN4 ≥ 4; n = 584) modified this association (interaction P = .004): early care was associated with
+7.2 points (95% CI, 4.9 to 9.5) and a 64.2% vs 44.5% responder rate (+19.7 percentage points;
95% CI, 11.7 to 27.7 percentage points) vs +1.9 points (95% CI, −0.4 to 4.2) in
nociceptive-predominant patients (n = 836). Complete-case (n = 1,292; +3.9), 8-week landmark
(+3.6), and E-value (2.81; lower CI, 2.04) checks agreed.

**Conclusions and Relevance:** Early multidisciplinary rehabilitation (≤6 weeks) was associated
with larger 12-month physical function score gains and higher individual MCID responder rates
concentrated among patients with baseline neuropathic pain, motivating prospective evaluation of
phenotype-stratified referral.

## Introduction

Lumbar decompression relieves neural compression in symptomatic spinal stenosis and disc
herniation, yet persistent postoperative disability remains common in long-term surgical cohorts
[@weinstein2008sport]. Postoperative rehabilitation programs can support functional recovery,
although systematic reviews report heterogeneous effect sizes across timing windows and program
intensities [@ostelo2008rehab; @mcgregor2014rehab].

Because multidisciplinary clinics combining physical therapy, pain psychology, and graded activity
have limited intake capacity, referral delays vary widely in routine practice. Existing trials
and observational cohorts have rarely stratified postoperative rehabilitation timing by baseline
pain mechanism [@mcgregor2014rehab], and unaligned observational timing analyses are vulnerable
to immortal-time bias when patients must remain event-free until clinic intake.

Patients presenting with preoperative neuropathic pain features often experience persistent
sensitization and movement avoidance during early surgical recovery [@bouhassira2005dn4]. We
conducted a two-center 6-week landmark cohort study of 1,420 adults to test whether initiating
multidisciplinary rehabilitation within 6 weeks after lumbar decompression is associated with
greater 12-month PROMIS Physical Function gains and whether a prespecified baseline neuropathic
pain phenotype modifies this association.

## Methods

### Study Design, Landmark Alignment, and Eligibility

We conducted a retrospective observational cohort study across two academic spine centers reported
according to STROBE guidelines [@vonelm2007strobe]. Eligible adults aged 18 to 80 years underwent
primary elective lumbar decompression between January 2019 and December 2024 and completed
preoperative baseline assessments (Table 1; screening and follow-up flow in Supplementary Figure S1).

To prevent immortal-time bias, time zero was fixed at postoperative week 6 (Figure 1). Patients
who underwent reoperation, died, or withdrew before week 6 were excluded prior to landmark
assignment. All remaining patients alive and reoperation-free at week 6 were included regardless
of 12-month survey completion (n = 1,420). Patients who completed at least one multidisciplinary
rehabilitation intake visit on or before week 6 formed the early-rehabilitation group (n = 512),
and all other landmark-eligible patients formed the comparator group (n = 908).

Baseline pain phenotype was defined preoperatively using the validated Douleur Neuropathique 4
(DN4) questionnaire [@bouhassira2005dn4], dichotomized at the standard threshold of 4 or greater
(n = 584 neuropathic; n = 836 nociceptive-predominant). The primary outcome was 12-month change in
PROMIS Physical Function T-score [@cella2010promis]. Because the 3.0-point minimal clinically
important difference (MCID) reflects an individual-level change threshold, we evaluated both
between-group mean differences and the proportion of patients achieving an individual gain of at
least 3.0 points.

### Statistical Analysis

We balanced 24 preoperative demographic, surgical, comorbidity, and pain severity covariates using
stabilized inverse probability of treatment weighting (IPTW), targeting post-weighting
standardized mean differences below 0.10 (Table 1 and Supplementary Table S1). Missing 12-month
PROMIS scores (128 of 1,420 patients [9.0%]) were addressed with chained-equations multiple
imputation (m = 20 imputations; diagnostics in Supplementary Table S2).

Primary and prespecified DN4-interaction models used IPTW weighted linear regression for mean
change and weighted binomial regression for individual MCID responder risk differences, with
robust sandwich standard errors. Secondary subgroup analyses by age, surgical levels, and center
were labeled exploratory. To examine timing variation without reintroducing post-landmark immortal
time, we fit a restricted cubic spline strictly within pre-landmark initiation weeks 1 through 6
among early initiators (n = 512), evaluating 12-month outcomes strictly after week 6 (Figure 1).
Prespecified sensitivity analyses included complete-case estimation (n = 1,292), an 8-week
landmark, and E-value estimation from the primary standardized mean difference (d = 0.59, SD = 7.0;
lower CI d = 0.33) via the VanderWeele and Ding conversion [@vanderweele2017evalue].

## Results

### Cohort Balance and Primary Landmark Association

Of 1,685 screened adults, 1,420 remained alive and reoperation-free at the 6-week landmark (mean
age 58.4 years; 52.1% female), comprising 512 early-rehabilitation patients and 908 comparator
patients; 1,292 patients (91.0%) completed 12-month PROMIS follow-up (Table 1). After IPTW, all
24 baseline covariates achieved standardized mean differences of 0.08 or less.

In the primary multiply imputed IPTW landmark model, early rehabilitation was associated with a
4.1-point greater 12-month PROMIS Physical Function gain (95% CI, 2.3 to 5.9; P < .001; Table 2).
In the prespecified phenotype-interaction analysis (interaction P = .004), early rehabilitation
was associated with a 7.2-point greater gain (95% CI, 4.9 to 9.5) and a 64.2% vs 44.5% individual
MCID responder rate (risk difference +19.7 percentage points; 95% CI, 11.7 to 27.7 percentage
points) among patients with baseline neuropathic pain features (n = 584). Among patients with
nociceptive-predominant pain (n = 836), the between-group difference did not reach statistical
significance (+1.9 points; 95% CI, −0.4 to 4.2; responder difference +5.1 percentage points,
95% CI, −1.4 to 11.6 percentage points), though the upper confidence bound includes modest benefit
(Figure 1 and Table 2).

### Pre-Landmark Timing, Subgroups, and Sensitivity Analyses

Within early-window initiators (weeks 1–6; n = 512), restricted cubic spline modeling indicated
that estimated within-group 12-month gains from baseline in the neuropathic subgroup peaked for
intake between weeks 3 and 5 (+8.4 points from baseline [95% CI, 5.7 to 11.1] at week 4 vs +5.1
points from baseline [95% CI, 2.2 to 8.0] at week 1; Figure 1). Exploratory subgroup estimates
remained consistent across age strata, single-level vs multilevel decompression, and both centers
(Figure 2).

Results were stable in complete-case analysis restricted to the 1,292 patients with observed
12-month scores (+3.9 points; 95% CI, 2.0 to 5.8; P < .001) and when shifting the landmark to
postoperative week 8 (+3.6 points; 95% CI, 1.7 to 5.5; P < .001; Table 2). From the primary
standardized mean difference (d = 0.59; approximate risk ratio 1.71), an unmeasured confounder
would need a risk-ratio association of at least 2.81 with both early referral and functional
recovery (2.04 for the lower confidence bound) to explain away the observed association (Table 2).

**Table 1.** Baseline characteristics of 1,420 lumbar decompression patients at the 6-week landmark
with post-IPTW standardized mean differences.

| Characteristic | Early Rehab (n = 512) | Delayed / Usual Care (n = 908) | Post-IPTW SMD |
| --- | --- | --- | --- |
| Age, mean (SD), y | 57.9 (11.2) | 58.7 (11.6) | 0.03 |
| Female, No. (%) | 274 (53.5) | 466 (51.3) | 0.02 |
| Baseline PROMIS Physical Function, mean (SD) | 35.8 (6.4) | 36.4 (6.7) | 0.04 |
| Baseline DN4 ≥ 4 (neuropathic), No. (%) | 246 (48.0) | 338 (37.2) | 0.05 |
| Observed 12-month PROMIS follow-up, No. (%) | 468 (91.4) | 824 (90.7) | 0.02 |

**Figure 1.** Early multidisciplinary rehabilitation within the 6-week landmark window is
associated with higher 12-month PROMIS Physical Function mean and responder gains predominantly
among patients with baseline neuropathic pain features (n = 1,420). Panel A illustrates the 6-week
landmark design (schematic). Panel B shows IPTW-adjusted 12-month PROMIS gains by initiation week
restricted strictly to pre-landmark initiators (weeks 1–6; n = 512). Panel C displays proportions
achieving the individual minimal clinically important difference (≥3.0 points) by baseline DN4
phenotype with 95% confidence intervals.

**Figure 2.** The 12-month physical function association for early rehabilitation persists across
exploratory surgical subgroups, 8-week landmark alignment, and complete-case sensitivity analyses.
Points represent IPTW-adjusted 12-month PROMIS differences with 95% confidence intervals.

**Table 2.** Primary landmark, prespecified phenotype-interaction, responder, and sensitivity
estimates for 12-month PROMIS Physical Function.

| Analysis | Adjusted Estimate (95% CI) | P Value / Metric |
| --- | --- | --- |
| Primary 6-week landmark, MI (n = 1,420) | +4.1 points (2.3 to 5.9) | P < .001 |
| Neuropathic phenotype, DN4 ≥ 4 (n = 584) | +7.2 points (4.9 to 9.5) | Interaction P = .004 |
| Neuropathic individual MCID responder (≥3.0 pts) | 64.2% vs 44.5% (+19.7 pp, 11.7 to 27.7 pp) | P < .001 |
| Nociceptive phenotype, DN4 < 4 (n = 836) | +1.9 points (−0.4 to 4.2) | Interaction P = .004 |
| Complete-case sensitivity (n = 1,292) | +3.9 points (2.0 to 5.8) | P < .001 |
| 8-week landmark sensitivity | +3.6 points (1.7 to 5.5) | P < .001 |
| Unmeasured confounding bound (d = 0.59) | — | E-value = 2.81 (lower CI, 2.04) |

## Discussion

In this two-center 6-week landmark cohort, initiating multidisciplinary rehabilitation within 6
weeks after lumbar decompression was associated with a 4.1-point greater 12-month PROMIS Physical
Function gain, with larger mean and individual responder gains concentrated in patients with
baseline neuropathic pain features. Stratifying early multidisciplinary intake by preoperative DN4
screening represents a concrete hypothesis for prospective clinical pathway trials where clinic
capacity is constrained.

Prior postoperative spine rehabilitation trials reported inconsistent timing effects in
unstratified surgical populations [@ostelo2008rehab; @mcgregor2014rehab]. Stratifying by baseline
DN4 phenotype provides a plausible explanation for that heterogeneity: patients with neuropathic
pain features showed substantial divergence in both mean recovery and individual MCID responder
rates under early multidisciplinary care, whereas the confidence interval in
nociceptive-predominant patients crossed the null while remaining compatible with modest benefit.
Early combined physical and behavioral rehabilitation during weeks 3 through 5 (+8.4 points at week
4 vs +5.1 points at week 1) may interrupt postoperative movement avoidance before chronic
deconditioning consolidates, although mechanistic mediators were not directly measured here.

### Limitations

Because referral occurred in routine care rather than randomized allocation, residual confounding
by surgeon preference, patient motivation, or early postoperative pain flares before week 6 cannot
be excluded (E-value 2.81; lower CI, 2.04). The comparator also pools delayed multidisciplinary
intake (>6 weeks) with usual care, preventing separation of timing from program intensity without
a delayed-multidisciplinary sensitivity check. Missing 12-month scores (9.0%) were multiply
imputed, yet non-random attrition remains possible. Finally, two-center academic data lacked
therapist identifiers, warranting prospective multicenter evaluation.

### Conclusions

Early multidisciplinary rehabilitation initiated within 6 weeks after lumbar decompression was
associated with larger 12-month physical function gains and higher individual MCID responder rates
concentrated among patients with baseline neuropathic pain features. These observational findings
motivate prospective randomized evaluation of phenotype-stratified postoperative referral pathways.

## Declarations

### Ethics Approval
The institutional review boards at both participating academic spine centers approved this
retrospective cohort study with a waiver of informed consent for de-identified electronic health
record analysis (synthetic worked-example declaration).

### Data Availability
De-identified aggregate summary tables supporting this worked example are available upon reasonable
request subject to institutional data-use agreements.

### Code Availability
Analytic scripts supporting this worked example are available in the companion repository.

### Funding
No external funding supported this synthetic worked example.

### Conflicts of Interest
The authors report no competing financial or nonfinancial interests.

### AI-Use Disclosure
AI-assisted drafting and structural consistency checks were used during manuscript preparation;
all scientific claims, statistical interpretations, and final text were reviewed and approved by
the authors in accordance with ICMJE guidance.
