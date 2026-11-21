# Point-by-Point Response to Reviewers — Computational Method Example

**Manuscript:** Calibration-Preserving Structured Attention Pruning for a Cross-Site 12-Lead ECG Transformer
**Target Journal / Decision:** *npj Digital Medicine* — Major Revision (simulated worked example)
**Revised File:** `examples/computational-method/draft-manuscript.md`

Dear Editor and Reviewers,

We have revised the manuscript to address every point raised in review. Specifically, we added
logistic calibration slope and intercept to Table 1, added a full per-site external validation
breakdown across Hospitals A, B, and C in Table 2, clarified our disjoint pruning-selection and
calibration validation splits in Methods, and kept our prospective clinical scope explicitly
bounded in Discussion.

---

## Reviewer 1

### Comment R1.1
> "Expected calibration error alone can obscure systematic under- or over-estimation across risk
> strata, and pooled external numbers may hide poor performance at one hospital. Please report
> calibration slope and intercept and provide per-site external validation results."

**Response:** We now report logistic calibration slope and calibration intercept for every method
in Table 1 and present per-site external AUROC, macro 15-bin ECE, arrhythmia prevalence, and
calibration slope separately for Hospitals A (n = 5,420), B (n = 4,980), and C (n = 4,420) in a
new Table 2. On pooled external validation, CalPrune held macro ECE at 0.019 (calibration slope
0.97) compared with magnitude pruning at ECE 0.054 (calibration slope 0.71). Per site, CalPrune
maintained ECE between 0.018 and 0.021 (0.018 at Hospital A, 0.021 at Hospital B, and 0.019 at
Hospital C; slopes 0.95 to 0.98), whereas magnitude pruning exceeded 0.049 ECE at every
institution (slopes 0.68 to 0.73).

**Manuscript revision (`Results — CalPrune Maintains Pooled and Per-Site Calibration at Matched Head-Pruning Speed` and `Table 2`):**
> "Per-site evaluation confirmed consistent calibration across all three external hospitals despite
> differing arrhythmia prevalences (18.4% at Hospital A, 24.1% at Hospital B, and 15.2% at Hospital
> C; Table 2). CalPrune held site-level ECE between 0.018 and 0.021 (slopes 0.95 to 0.98), whereas
> magnitude pruning exceeded 0.049 ECE at every institution (Table 2)."

### Comment R1.2
> "Please clarify whether the pruning penalty weight $\lambda$ and post-hoc temperature scaling
> were tuned on the same validation split, which could introduce optimism bias."

**Response:** They were fit on strictly disjoint patient-level splits. We expanded `Methods —
Multi-Site Cohorts and Disjoint Validation Splits` to specify the 70/10/10/10 patient-disjoint
partition of the 42,600 development recordings separating pruning-selection validation (10%) from
post-hoc temperature-scaling calibration validation (10%) and internal testing (10%, n = 4,260
recordings).

**Manuscript revision (`Methods — Multi-Site Cohorts and Disjoint Validation Splits`):**
> "Model development used 42,600 12-lead ECG recordings from 31,400 unique patients at one academic
> medical center, partitioned at the patient level into training (70%), pruning-selection
> validation (10%), post-hoc calibration validation (10%), and internal test (10%; 4,260
> recordings). Separating the pruning-selection split from the calibration split prevented
> temperature-scaling optimism on the same validation records."

---

## Reviewer 2

### Comment R2.1
> "To establish clinical value, the authors should conduct a 12-month prospective randomized
> deployment study evaluating emergency-department alert fatigue and patient outcomes."

**Response:** We agree that prospective clinical evaluation is essential before bedside adoption,
and we explicitly state this boundary in the manuscript. A 12-month prospective interventional
trial requires separate multi-site institutional review board approval, EHR alert integration, and
prospective safety monitoring that lie outside the scope of this retrospective TRIPOD+AI
methodological validation study. To ensure readers do not infer live clinical efficacy, we keep
every claim in the Abstract, Figure 1, Discussion, and Conclusion strictly scoped to retrospective
multi-site evaluation.

**Manuscript revision (`Discussion — Scope and Limitations`):**
> "Evaluation relied on retrospective multi-site ECG archives rather than prospective bedside
> deployment, so effects on clinician alert fatigue and patient outcomes remain unmeasured."
