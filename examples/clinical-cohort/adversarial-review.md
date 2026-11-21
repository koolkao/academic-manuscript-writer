# Adversarial Review — Clinical Cohort Example

- **Manuscript inspected:** `examples/clinical-cohort/draft-manuscript.md`
- **Isolation manifest:** Illustrative worked example (modeled on fresh-subagent isolation) — Files inspected: `examples/clinical-cohort/draft-manuscript.md`, `examples/clinical-cohort/references.bib`. Excluded: `manuscript-plan.md`, `revision-notes.md`.
- **Target venue & house style:** *JAMA Network Open* (AMA style)
- **Scope note:** Agent adversarial review is pre-submission triage, not domain peer review or formal biostatistical sign-off.

## Forced Rejection Pre-Mortem

**Simulated 3-sentence rejection letter (for the current draft as written):**
> Although the 6-week landmark alignment and neuropathic subgroup analysis address a practical postoperative question, the comparator group pools delayed multidisciplinary rehabilitation with single-modality usual care, preventing separation of referral timing from multidisciplinary program intensity. In addition, propensity weighting adjusts exclusively for preoperative covariates even though postoperative pain flares or early surgical recovery between weeks 1 and 6 likely drive referral prior to the landmark, and the draft calls the DN4 interaction "prespecified" without citing a registered statistical analysis plan. Without a delayed-multidisciplinary-only comparator check, time-varying postoperative adjustment, and verifiable prespecification documentation, the editorial board cannot recommend publication as written.

**Top-3 ranked rejection risks:**
1. Comparator conflates rehabilitation *timing* (>6 weeks) with *program intensity* (single-modality usual care) (`Methods — Study Design, Landmark Alignment, and Eligibility`).
2. Preoperative-only IPTW omits time-varying postoperative covariates accrued between surgery and the week-6 landmark (`Methods — Statistical Analysis`).
3. Key Points, Abstract, Introduction, Methods, and Results call the DN4 interaction `"prespecified"` with no protocol or statistical analysis plan registration ID (`Key Points`, `Methods — Statistical Analysis`).

## Submission Verdict

- **Verdict:** Revise before submission (author reanalysis required) — zero open `FATAL` findings; two `MAJOR` items (`M01`, `M02`) require Rung 5 author reanalysis (`pending-author-data`) and one `MAJOR` item (`G01`) requires protocol registration documentation or removal of `"prespecified"`.

## Four-Lens Critique

*(Status is tracked ONLY in the Impact × Effort Decision Matrix below. All findings below were verified against the full manuscript text.)*

### Lens 1 — Handling Editor (Desk-Rejection Filter)
- **[MINOR] E01 — Title omits the neuropathic phenotype modifier** (`Title`): The current title names only early rehabilitation, whereas the study's main clinical hook is the DN4 neuropathic effect modification. *Risk:* Generalist editors scanning titles may read the paper as a routine timing cohort. *Minimum fix:* Rung 1 (Clarify wording) — author to decide whether to include neuropathic pain phenotype in the Title.

### Lens 2 — Skeptical Methodologist / Biostatistician ("Reviewer #2")
- **[MAJOR] M01 — Comparator pools delayed multidisciplinary care with usual single-modality care** (`Methods — Study Design, Landmark Alignment, and Eligibility`): `"all other landmark-eligible patients formed the comparator group (n = 908)"`. *Risk:* Reviewers will ask whether the +7.2-point neuropathic difference reflects *receiving multidisciplinary care at all* rather than *initiating it within 6 weeks*. *Minimum fix:* Rung 5 (Analyze existing data) — run a sensitivity analysis restricting the comparator strictly to patients who initiated multidisciplinary rehabilitation after week 6.
- **[MAJOR] M02 — Preoperative-only IPTW omits post-surgery time-varying covariates up to week 6** (`Methods — Statistical Analysis`): `"We balanced 24 preoperative demographic, surgical, comorbidity, and pain severity covariates."` *Risk:* Early postoperative pain, wound complications, or mobility between week 0 and week 6 may drive week 1–6 referral prior to the landmark. *Minimum fix:* Rung 5 (Analyze existing data) — incorporate available 2-week postoperative pain/complication covariates into IPTW (or test sensitivity) if captured in EHR; if unavailable, document unavailability explicitly in Methods alongside Limitations.

### Lens 3 — Busy Field Reader / Practitioner
- **[MINOR] R01 — Report median (IQR) initiation week in delayed multidisciplinary comparator** (`Results — Cohort Balance and Primary Landmark Association`): Helps clinicians judge how late delayed referrals occurred once `M01` is extracted. *Minimum fix:* Rung 1 — add alongside `M01` output.

### Lens 4 — Reporting, Ethics & Novelty Gate
- **[MAJOR] G01 — Unsupported `"prespecified"` claim lacks protocol / SAP registration** (`Key Points`, `Introduction`, `Methods — Statistical Analysis`, `Results`): The draft repeatedly labels the DN4 interaction `"prespecified"` without citing a timestamped OSF/ClinicalTrials/institutional SAP registration ID. *Risk:* Under STROBE and *JAMA Network Open* standards, unverified `"prespecified"` subgroup claims invite methodological challenge. *Minimum fix:* Rung 1 / Rung 4 — cite the timestamped SAP/protocol registration ID, or remove `"prespecified"` and frame the subgroup interaction transparently.
- **[INFO] G02 — Novelty / literature check `[user-verify]`:** Verify `"Existing trials and observational cohorts have rarely stratified postoperative rehabilitation timing by baseline pain mechanism"` (`Introduction`) against a live PubMed/Cochrane search through 2026.

## Impact × Effort Decision Matrix

| ID | Severity | Rung (1–6) | Priority tier | Minimum defensible fix | Status |
| --- | --- | --- | --- | --- | --- |
| M01 | MAJOR | 5 (Analyze existing data) | Essential before submission | Restrict comparator to delayed (>6 wk) multidisciplinary recipients to separate timing from program intensity | pending-author-data |
| M02 | MAJOR | 5 (Analyze existing data) | Essential before submission | Add available early post-op (weeks 0–2) pain/recovery covariates to IPTW or test sensitivity | pending-author-data |
| G01 | MAJOR | 1 (Clarify) / 4 (Narrow) | Essential before submission | Cite timestamped SAP/protocol registration ID supporting `"prespecified"` DN4 interaction, or remove `"prespecified"` | open |
| R01 | MINOR | 1 (Clarify wording) | Useful improvement | Add median (IQR) initiation week for delayed multidisciplinary subgroup alongside `M01` | pending-author-data |
| E01 | MINOR | 1 (Clarify wording) | Author decision | Decide whether Title should explicitly name neuropathic pain phenotype | open |
