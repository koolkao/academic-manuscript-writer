# Field calibration and reporting standards

Do not force one discipline's conventions onto another. Identify the field family from the supplied
materials (ask only when genuinely ambiguous and venue-altering) and calibrate structure, voice,
visuals, and reporting expectations accordingly.

## 1. Field-family calibration

| Field family | Typical structure & abstract | Voice & tense norms | Primary visual idioms | What reviewers attack first |
|---|---|---|---|---|
| **Clinical & epidemiological** | Structured abstract (250–350 words); strict IMRaD; clear primary vs. secondary endpoints; Table 1 baseline demographics. | Moderate "we" (common in Intro/Discussion, concise past passive acceptable in Methods); past tense for cohort/results; absolute + relative risk with 95% CIs. | Cohort/CONSORT flow diagram, Kaplan–Meier or longitudinal trajectory plots, forest plots (subgroups/sensitivity), clinical timeline/pathway synthesis. | Immortal-time bias, confounding by indication, selection/missing-data bias, multiplicity, causal language on observational data, clinical vs. statistical significance. |
| **Biomedical & life sciences** | Unstructured or *Nature*-style summary; IMRaD or Intro → Results → Discussion → Methods; finding-declarative subheadings in Results. | Active "we" throughout Results/Discussion; present tense for established biology and figure descriptions, past tense for experiments performed. | Multi-panel mechanistic + quantitative figures, microscopy/imaging with scale bars, volcano/enrichment/spatial plots, integrated biological pathway synthesis. | Biological vs. technical replicates (`n` vs. `N`), negative/positive controls, batch effects, orthogonal validation, extrapolating in vitro/animal findings to humans. |
| **Computational & machine learning** | Unstructured 150–250 word abstract; Intro → Related Work → Method → Experiments → Discussion/Conclusion; clear problem formulation. | High active "we" and explicit signposting ("Section 3 defines…"); present tense for method/model and established properties, past tense for experiments. | Architecture/mechanism schematic (clearly non-empirical), Pareto/tradeoff frontiers, calibration & shift curves, ablation heatmaps, qualitative error analysis. | Data leakage across splits/sites, weak or untuned baselines, missing external validation or uncertainty intervals across seeds, metric gaming, conflating benchmark gain with clinical utility. |
| **Methods, biostatistics & theory** | Compact abstract; Motivation/Problem → Formal Setup/Assumptions → Method/Theory → Simulation Study → Real-Data Application → Discussion. | High active "we"; exact modal and assumption language ("under Assumption 1…", "asymptotically unbiased"); prove/establish reserved for theorems. | Bias–variance/coverage grids across regimes, sample-size scaling curves, real-data diagnostic plots, DAGs/identifiability schematics. | Unstated or unrealistic assumptions, simulation scenarios cherry-picked to favor the method, missing competitor methods, finite-sample failure modes. |
| **Reviews & evidence syntheses** | Structured abstract (systematic) or thematic synthesis; explicit search/selection criteria (systematic) or organizing conceptual lens (narrative). | Authoritative, balanced synthesis; present tense for current state of evidence, past tense for search execution and individual study results. | PRISMA flow diagram, evidence-gap matrix, conceptual taxonomy/framework diagram, forest/harvest plots. | Non-systematic cherry-picking, risk-of-bias omission, conflating heterogeneity with consensus, outdated search cutoff. |

## 2. Light-touch reporting-guideline pointers (EQUATOR)

Use the applicable guideline as a **targeted validity check**, never as a bloated 40-item form
dumped into the user's lap. Surface only the **missing core items** that would trigger reviewer or
editor pushback:

| Study design | Guideline | High-leverage items to verify early |
|---|---|---|
| Randomized trial | **CONSORT** | Allocation/randomization & blinding details, participant flow (`n` screened → randomized → analyzed), pre-specified primary endpoint, intention-to-treat handling, trial registration ID, harms. |
| Observational cohort / case-control / cross-sectional | **STROBE** | Clear eligibility & index date (`time zero`), exposure/outcome definitions, handling of missing data and loss to follow-up, confounder selection rationale, sensitivity analyses for unmeasured confounding/bias. |
| Clinical prediction / medical AI model | **TRIPOD+AI / CLAIM** | Cohort provenance & site split (internal vs. external validation), leakage prevention, calibration (not just AUROC), subgroup/fairness performance, handling of missing predictors, clinical decision threshold / net benefit. |
| Systematic review / meta-analysis | **PRISMA 2020** | Databases & search date, screening counts & exclusion reasons, risk-of-bias tool, heterogeneity metrics ($I^2$, prediction intervals), protocol registration (PROSPERO/OSF). |
| Animal / preclinical study | **ARRIVE 2.0** | Experimental unit (`n`), randomization, blinding, sample-size justification, exclusions, housing/welfare & ethics statement. |
| Clinical case report | **CARE** | De-identified timeline, diagnostic reasoning & differentials, intervention details, follow-up outcome, patient perspective/consent statement. |

## 3. Venue-constraint check

Before finalizing a plan or draft, capture concrete target-venue limits when known (or note
assumptions if venue is undecided):
- Abstract word limit and structured vs. unstructured format
- Main-text word or page limit (note whether references and tables count toward page limit)
- Main figure + table cap (and whether a graphical abstract or highlights box is required)
- Required declarations (ethics/IRB, data/code availability, funding, conflicts, AI-use disclosure
  — keep declaration sections locked once authored)
