# Revision Notes — Clinical Cohort Example

- **Original file:** None (new synthetic worked demonstration)
- **Draft / structural output:** `examples/clinical-cohort/draft-manuscript.md` (compact ~1,375-word demonstration)
- **Scope of pass:** Full blueprint + AMA-styled Markdown draft + illustrative adversarial red-team + integrated sweep

## Substantive Changes Applied

1. **Eliminated immortal-time risk and verified all derived arithmetic:** Anchored eligibility at the 6-week landmark without conditioning on 12-month survey completion (n = 1,420; 1,292 [91.0%] observed; m = 20 multiple imputation), restricted the timing spline strictly to pre-landmark weeks 1–6 (n = 512) with explicit within-group baseline-change estimates (`+8.4` [95% CI, 5.7 to 11.1] at week 4 vs `+5.1` [95% CI, 2.2 to 8.0] at week 1), and recomputed the exact VanderWeele & Ding continuous E-value for `d = 0.59` (`RR ≈ exp(0.91 × 0.59) = 1.71 → E = 2.81`; lower CI `d = 0.33 → E = 2.04`).
2. **Removed group-level MCID and null-result overclaims:** Replaced `"clinically meaningful"` on the 4.1-point group mean with exact score gains + individual MCID responder rates (`≥3.0`-point gain: 64.2% vs 44.5%; +19.7 percentage points, 95% CI, 11.7 to 27.7 percentage points), replaced `"selectively"` in Figure 1 caption with `"predominantly"` (respecting the nociceptive CI upper bound of 4.2), and kept AMA `P < .001`, `No. (%)`, and Unicode `≥`/`−`.
3. **Aligned STROBE item 19 limitations and lock-safe Declarations:** Expanded `### Limitations` to address confounding, comparator pooling, missingness, and academic-center generalizability honestly (~28% of Discussion, comfortably within the 20–35% clinical STROBE range); kept separate `### Data Availability` and `### Code Availability` headings so every declaration is FAIL-locked by `academic-humanizer`.

## Unresolved Decisions & `pending-author-data` Items

- **`M01` (`pending-author-data` — Essential):** Run Rung 5 sensitivity analysis restricting comparator strictly to delayed (>6 wk) multidisciplinary recipients, and report median (IQR) delayed initiation week (`R01`).
- **`M02` (`pending-author-data` — Essential):** Add available early postoperative (weeks 0–2) recovery covariates to IPTW or verify sensitivity to time-varying pre-landmark confounding.
- **`G01` (`open` — Essential):** Cite timestamped SAP/protocol registration ID supporting `"prespecified"` DN4 interaction, or remove `"prespecified"`.
- **`E01` (`open`) & `G02` (`[user-verify]`):** Author decides whether to add neuropathic phenotype to Title and confirms Introduction literature-gap claim against live PubMed/Cochrane search.

## Field-Calibrated Limitations Rationale

- **Included in published manuscript (1 STROBE item 19 paragraph, ~28% of Discussion):** Unmeasured confounding & surgery-to-landmark time-varying selection (bounded by E-value = 2.81), comparator pooling of delayed multidisciplinary vs. usual single-modality care, missing 12-month follow-up (9.0%), and absence of therapist clustering IDs / two-center academic generalizability.
- **Kept internal (not inflated in prose):** Absence of 24-month cost claims (`C05` gap) and wearable step-count logs.

## Integrated Consistency Check

- **Automated check:** `python3 scripts/check_manuscript.py examples/clinical-cohort` → 0 FAIL; 3 expected `REV-05` WARNs (`open MAJOR M01`, `M02`, `G01`).
- **Structural preservation check:** Not applicable (new synthetic draft, not restructured from an existing manuscript).
- **Semantic sweep verified:** Title ↔ Key Points ↔ Abstract ↔ Intro ↔ Methods ↔ Results ↔ Tables 1–2 ↔ Figures 1–2 ↔ Discussion ↔ Declarations aligned; all `[@citekey]` occurrences verified in `references.bib`; Table 1 `No. (%)` arithmetic verified cleanly.

## Prioritized Next Actions

1. **Essential:** Run Rung 5 sensitivity checks (`M01`, `M02`) and resolve SAP registration citation (`G01`).
2. **High-value improvement:** Render Figures 1 and 2 at 175 mm double-column width and run a multimodal visual audit.
3. **Optional polish:** Run `academic-humanizer` (`voice` mode) using `protect-terms.txt`, then assemble `.docx` via your project's Zotero build scripts.

## Handoff to academic-humanizer

- **Input file for humanizer:** `examples/clinical-cohort/draft-manuscript.md` (after author resolves `M01`/`M02`/`G01`)
- **Workflow mode:** standalone (`draft-manuscript.revised.md` + `draft-manuscript.changes.md`; promote to `.keys.md` after approval)
- **Protect file:** `examples/clinical-cohort/protect-terms.txt` (pass via `--protect`)
- **Recommended mode:** `edit` (or `voice` with author's prior clinical cohort manuscript)
- **Target venue & house style:** *JAMA Network Open* — AMA style (`P < .001`, percentage points, `≥`, `−`)
- **Locked one-sentence thesis:** Across 1,420 adults reoperation-free at 6 weeks after lumbar decompression, initiating multidisciplinary rehabilitation within 6 weeks was associated with a 4.1-point greater 12-month PROMIS Physical Function gain (95% CI, 2.3 to 5.9; P < .001), with larger mean and responder-level gains concentrated among patients with baseline neuropathic pain features (interaction P = .004).
- **Protected claim boundaries:**
  - Retrospective observational cohort: keep "associated with"; never upgrade to causal verbs ("improves", "reduces", "yielded").
  - Nociceptive subgroup CI (−0.4 to 4.2) crosses null: never rewrite as "no effect", "recovered similarly", or "selectively".
  - Do not apply individual 3.0-point MCID as a label for a group mean difference, and do not claim cost reduction.
- **Locked declaration headings (do not edit):** `Ethics Approval, Data Availability, Code Availability, Funding, Conflicts of Interest, AI-Use Disclosure`
- **Open items for author (do not guess in prose pass):** `M01`, `M02`, `G01`, `E01`, `G02`.
