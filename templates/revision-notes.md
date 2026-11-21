# Revision Notes

<!-- If the project already maintains STATUS.md, update STATUS.md instead of creating a parallel file. -->

- **Original file:** <Path (unchanged)>
- **Draft / structural output:** <Path (`<name>.draft.<ext>`, `<name>.structural.<ext>`, or `<name>.keys.md` with `.pre-*.md` backup)>
- **Scope of pass:** <Plan / Draft / Structural revision / Adversarial revision / Rebuttal>

## Substantive Changes Applied

1. <Change + rationale + affected headings>
2. <Change + rationale + affected headings>

## Unresolved Decisions & `pending-author-data` Items

- <Item requiring author computation, data, confirmation, or `[user-verify]` literature check>

## Field-Calibrated Limitations Rationale

- **Included in published manuscript:** <Caveats required by field/reporting guideline or materially bounding central claims>
- **Kept internal (not inflated in prose):** <Secondary omissions tracked here without bloating Discussion>

## Integrated Consistency Check

- **Automated check:** `python3 <skill-dir>/scripts/check_manuscript.py <target> --stage <draft|submission> [--bib <refs>]` → <exact PASS/FAIL/WARN counts; note any `--accept` rules + rationale>
- **Structural preservation check** *(if restructuring an existing draft)*: `preservation_check.py <orig> <structural>` → <PASS / Not applicable (new draft) / Tool not installed locally>
- **Semantic sweep verified:** Title ↔ Abstract / Summary ↔ Key Points ↔ Intro ↔ Results ↔ Figures/Tables/Captions ↔ Discussion ↔ Declarations ↔ Response Letter (`<Complete / Partial — list gaps>`)

## Prioritized Next Actions

1. **Essential:** <...>
2. **High-value improvement:** <...>
3. **Optional polish:** <...>

## Handoff to academic-humanizer

- **Input file for humanizer:** `<path/to/paper.draft.md>` (or `<paper.keys.md>`)
- **Workflow mode:** `<standalone (.revised.md + .changes.md; promote to .keys.md after approval) | in-place with .pre-humanizer-<date>.md backup>`
- **Protect file:** `protect-terms.txt` (or `protect.txt`; one term per line)
- **Recommended mode:** `edit` (or `voice` with author prior paper: `<sample_path>`)
- **Target venue & house style:** `<venue; e.g., JAMA Network Open — AMA style>`
- **Locked one-sentence thesis:** `<exact sentence>`
- **Protected claim boundaries:**
  - `<boundary 1>`
- **Locked declaration headings (do not edit):** `Ethics Approval, Data Availability, Code Availability, Funding, Conflicts of Interest, AI-Use Disclosure`
- **Open items for author (do not guess in prose pass):** `<items or None>`
