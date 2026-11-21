# Fixture: Clean, Sound Observational Draft (False-Positive Adversarial Control)

## Abstract

**Objective:** To evaluate whether preoperative anemia screening within 30 days of elective hip
arthroplasty is associated with lower perioperative red blood cell transfusion rates.

**Design, Setting, and Participants:** Retrospective cohort of 1,120 consecutive adults undergoing
primary elective total hip arthroplasty at one academic center (2020–2024), all with complete
inpatient transfusion records.

**Exposure:** Documented hemoglobin screening 14 to 30 days before surgery (n = 680) vs no
preoperative screening within 30 days (n = 440).

**Results:** After inverse probability of treatment weighting across 18 preoperative covariates
(all post-weighting SMDs ≤ 0.06), preoperative screening was associated with lower 7-day
transfusion incidence (6.2% vs 11.4%; adjusted risk difference −5.2 percentage points; 95% CI,
−8.4 to −2.0 percentage points; P = .001; crude risk ratio 1.84; E-value = 3.08, lower CI 1.72).
Propensity-matched checks were consistent (−4.9 percentage points; 95% CI, −8.2 to −1.6 percentage
points).

**Conclusions:** Preoperative anemia screening 14 to 30 days before elective hip arthroplasty was
associated with lower perioperative transfusion rates in this single-center cohort, supporting
prospective multicenter evaluation of standardized screening pathways.

## Methods

We conducted a single-center retrospective cohort study reported under STROBE guidelines
[@vonelm2007strobe]. Time zero was the date of primary elective hip arthroplasty; exposure
(hemoglobin screening 14 to 30 days preoperatively) was measured strictly before time zero,
avoiding immortal-time bias. Inpatient transfusion within 7 postoperative days was captured for all
1,120 patients (0% outcome missingness). Stabilized IPTW balanced 18 demographic, comorbidity, and
anticoagulation covariates to standardized mean differences ≤ 0.06 (Table 1).

## Results

Among 1,120 patients (mean age 66.2 years; 56.1% female), 680 underwent preoperative screening and
440 did not (Table 1). Seven-day transfusion occurred in 42 of 680 screened patients (6.2%) vs 50
of 440 unscreened patients (11.4%; crude risk ratio 1.84), yielding an IPTW-adjusted risk
difference of −5.2 percentage points (95% CI, −8.4 to −2.0 percentage points; P = .001; Figure 1).
Propensity-score matching estimated −4.9 percentage points (95% CI, −8.2 to −1.6 percentage
points), and an unmeasured confounder would need a risk-ratio association of at least 3.08 (1.72
for the lower CI bound) with both screening and transfusion to explain away the association.

**Table 1.** Baseline cohort characteristics (n = 1,120).

| Characteristic | Screened (n = 680) | Unscreened (n = 440) | Post-IPTW SMD |
| --- | --- | --- | --- |
| Female, No. (%) | 382 (56.2) | 246 (55.9) | 0.01 |
| 7-day transfusion, No. (%) | 42 (6.2) | 50 (11.4) | — |

**Figure 1.** Preoperative anemia screening 14 to 30 days before hip arthroplasty is associated
with lower 7-day red blood cell transfusion incidence across IPTW and propensity-matched models.

## Discussion

Preoperative anemia screening 14 to 30 days before elective hip arthroplasty was associated with a
5.2-percentage-point lower perioperative transfusion rate. Because screening was non-randomized at
one academic hospital, residual confounding by surgeon pathway adherence and transportability to
community hospitals warrant prospective multicenter testing.

## Declarations

### Ethics Approval
Approved by the institutional review board with a waiver of informed consent for de-identified
chart review.

### Data Availability
Aggregate summary tables are available upon reasonable request.

### Code Availability
Analytic scripts are available in the companion repository.

### Funding
Institutional department support only.

### Conflicts of Interest
The authors report no conflicts of interest.

### AI-Use Disclosure
No generative AI was used to analyze data; AI-assisted editorial checks were author-reviewed.
