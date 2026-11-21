# Section craft, house style, and Markdown → DOCX + Zotero workflow

Draft clean, publishable scientific prose on the first pass — avoiding structural AI-draft tells so
an optional final `academic-humanizer` pass has minimal churn. Leave detailed sentence-level
cliché catalogs and voice matching to `academic-humanizer`.

## 1. Macro-architecture: every section has one clear job

| Section | Core job | Common failure to avoid |
|---|---|---|
| **Title** | Make contribution and design/scope identifiable in one scannable phrase. Offer 2–3 options when framing a new paper. | Clever pun with no information; universal claim from one cohort or architecture. |
| **Abstract** *(or *Nature* **Summary**)* | Compress context → gap → approach → key quantitative results (exact `n`, uncertainty, comparator) → bounded meaning. Every number matches Results/Tables verbatim. | Vague promises; stale numbers after table edits; exceeding journal word limit. |
| **Key Points / Highlights** *(when venue requires)* | JAMA-style **Question / Findings / Meaning** (≤ 100 words) or 3–5 bullet Highlights (≤ 85 chars each) stating concrete, bounded takeaways. | Copying Abstract verbatim; overstating group means or subgroup findings. |
| **Introduction** | Consequential problem → specific unresolved gap → what this study did and contributes → stakes (typically 3–5 tight paragraphs). | Textbook lit-review dump; uncited background statistics; hiding contribution until paragraph 7. |
| **Methods** | Explain *what* was done and *why* key design choices protect validity (design/cohort/splits → exposures or method → outcomes/metrics → statistical/validation plan → sensitivity checks). | Missing time-zero/eligibility flow; outcome-conditioned eligibility; unstated metric definitions. |
| **Results** | Answer questions in logical reader order. State finding first, point to Figure/Table, give effect sizes + uncertainty + `n`, and bridge cleanly. | Lab chronology; reciting every table cell; sneaking unsupported mechanism speculation into Results. |
| **Discussion** | Paragraph 1: main advance and meaning first. Next: reconcile with prior literature, bound mechanism honestly, field-calibrated limitations (e.g., STROBE item 19 for clinical cohorts ~20–35%; concise bounded caveats for computational papers ~10–25%), concrete implications. | Opening with Intro recap; treating null CI as "no effect"; either under-disclosing clinical biases or writing defensive filler. |
| **Declarations** | Required venue blocks under **separate, lock-safe headings**: **Ethics Approval**, **Trial/Protocol Registration** (if applicable), **Data Availability**, **Code Availability**, **Funding**, **Conflicts of Interest**, **AI-Use Disclosure** (ICMJE). | Merging `Data and Code Availability` or omitting declarations (breaks `academic-humanizer` section locking). |
| **Cover Letter** *(when requested)* | 3–4 crisp paragraphs: (1) title, type, one-sentence advance; (2) why it fits *this* journal's readership now; (3) rigor highlights; (4) confirmations (exclusivity, ethics, COI, author approval). | Pasting the Abstract verbatim; overselling impact. |

## 2. Venue house style (explicit step in `draft` mode)

When a target venue is named, apply its house conventions from the start and record them in
`manuscript-plan.md` (or `PLAN.md`) and the humanizer handoff:

| House style | Representative venues | Key formatting conventions |
|---|---|---|
| **AMA** | *JAMA*, *JAMA Network Open*, *Anesthesiology*, US clinical journals | Structured abstract (≤ 350 words) + **Key Points**; uppercase `P` without leading zero (`P < .001`, `P = .004`); Unicode symbols (`≥`, `≤`, `−`, `×`); numeric refs; `%` repeated in ranges (`13.8%–25.6%`); absolute differences between proportions as **percentage points** (`19.7 percentage points`, not `+19.7%`). |
| **Vancouver / ICMJE** | *NEJM*, *Lancet*, *BMJ*, *Annals of Internal Medicine* | Structured abstract (250–300 words); exact 95% CIs + absolute and relative effects; explicit EQUATOR compliance and trial/protocol registration. |
| ***Nature*-family** | *Nature Medicine*, *npj Digital Medicine*, *Nature Biomedical Engineering* | Unstructured `## Summary` / Abstract (~150–200 words: broad context → specific gap → "Here we show…" → 2–3 quantitative results → wider implication); declarative Results subheadings; mandatory separate `Data Availability` and `Code Availability`. |
| **ML / Computational** | NeurIPS, ICML, ICLR, MLHC, *JAMIA* | Compact 150–250 word abstract; explicit problem setup, patient/site-disjoint splits, matched baselines, calibration + uncertainty across seeds, exact compute/latency hardware named. |

## 3. Paragraph and sentence architecture

- **Context → Content → Conclusion (C-C-C):** Sentence 1 anchors the question/link; middle
  sentences deliver evidence; final sentence states what the evidence establishes and sets up the
  next paragraph.
- **Topic & stress positions:** Put familiar context at the opening of the sentence and the new
  finding or quantitative punchline at the end. Keep grammatical subject and verb close.
- **Declarative headings & grounded wording:**
  - Replace subjective praise (*comprehensive, minimal, optimal, seamless, novel*) with mechanism
    descriptions or measured observations.
  - Use declarative headings (*"Calibration drift under standard pruning"*), never rhetorical
    questions (*"Why does AUROC fail?"*) or opaque labels (*"Stage 1"*).
- **Structural-not-prose mirroring (self-plagiarism guard):** Mirror section organization and
  paragraph jobs from reference papers — never reuse phrasing or literature-review prose verbatim.
- **Cite every factual background claim:** Never write uncited background statistics ("roughly one
  in four patients", "prior studies reported mixed results") without a verified citekey from the
  project's reference library — if missing, flag it in `revision-notes.md` (or with the project's
  `[PENDING: ...]` convention) rather than fabricating a citekey.

## 4. Four structural AI-draft tells to eliminate while drafting

1. **No reading instructions** (*"should be interpreted with caution"*, *"readers should bear in
   mind"*). State the concrete boundary as a scientific fact.
2. **No counted prefaces** (*"There are three key limitations"*). State the points directly.
3. **No self-ranking your own results** (*"Our most informative finding is…"*). Let placement and
   effect size carry weight.
4. **Length follows importance, not defensiveness.** Minor caveats get 1–2 sentences.

Keep field-appropriate **organizational signposting** (*"We next tested…", "To assess
immortal-time bias, we…"*) and natural **first-person plural ("we")**.

## 5. Optional: Markdown → `.docx` + Zotero assembly workflow (no Pandoc)

If your project authors manuscripts in keyed Markdown and assembles `.docx` files with live Zotero
citations using external project-local build scripts and a Word CLI (such as `wordcraft-cli`, not
bundled with this skill):

1. **Know which file is the master copy vs. generated output:**
   - **Master copy (edit this):** keyed Markdown (`<name>.keys.md`) using bracketed citekeys
     (`[@key]`, `[@key, p. 3; @key2]`) paired with the project's checked refs JSON
     (`manuscript-refs.json` `{key: {text, doi, src}}`, referenced by `zotero.json`'s `"refs"`
     field) or a Zotero `.bib`. Note that `.keys.md` is a **source format**, not a draft stage.
   - **Generated output (never hand-edit):** numbered Markdown (`<name>.md` produced by
     `number-refs.py`) and built `.docx` files. Always edit `<name>.keys.md` and regenerate
     downstream outputs.
   - **Reference authority:** When `zotero.json` and `sync-refs.mjs` are present, `sync-refs.mjs`
     is the authoritative citation-key check for the build; `check_manuscript.py` provides a quick
     local preflight (with `--stage draft` when `[PENDING: ...]` markers are still open, or
     `--stage submission` before final assembly).
2. **Keep figures and tables modular for assembly:**
   - Store rendered figures as standalone high-DPI PNG/SVG/PDF files paired with finding-first
     captions (`**Figure 1.** …` or `### Figure 1. …`).
   - Keep Markdown tables cleanly structured (`**Table 1.** …` or `### Table 1. …`) with group `n`
     in column headers so `check_manuscript.py` can audit count/percentage arithmetic.
3. **Downstream `.docx` + live Zotero assembly (project build step, outside this skill):**
   - `sync-refs.mjs` syncs checked refs into Zotero and builds the field plan (`ADDIN ZOTERO_ITEM
     CSL_CITATION {...}` + `ADDIN ZOTERO_BIBL`).
   - Project `build-docx.py` drives `wordcraft-cli run` (`insert.field {instr, result}`), sets
     Zotero citation style (e.g., AMA), and runs `wordcraft-cli zotero refresh`.
   - Project `docx_checks.py` verifies rendered fields and bibliography metadata.
4. **Post-assembly audit rules:**
   - Never raw-edit XML or strip live Zotero fields inside an assembled `.docx`.
   - Run `scripts/check_manuscript.py <assembled.docx>` read-only: it **FAILs** if any unconverted
     literal `[@key]`, `{Citation}`, or `[Citation error]` survived into the `.docx`.
   - Use `wordcraft-cli render <assembled.docx> <page.png>` for a multimodal visual audit of the
     laid-out pages and figures.
