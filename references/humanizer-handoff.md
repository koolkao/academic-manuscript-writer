# Handoff contract with `academic-humanizer`

Grounded in `koolkao/academic-humanizer` v0.2.0 (commit `53777babda5b`, 2026-11-16).

## 1. Division of labor and filename workflows

Run **`academic-manuscript-writer` first** to lock story, structure, claims, declarations, and
figures; run **`academic-humanizer` once** at the end for sentence-level AI-tell cleanup and voice
matching.

Two supported filename workflows (adopt whichever the project already uses):

1. **Standalone / non-destructive workflow:**
   - Original author file: `<name>.md` (untouched).
   - `academic-manuscript-writer` writes `<name>.draft.md` or `<name>.structural.md`, plus
     `revision-notes.md` and `protect-terms.txt`.
   - `academic-humanizer` writes `<input-stem>.revised.<ext>` and `<input-stem>.changes.md` beside
     the file passed to it (e.g., `paper.draft.md` → `paper.draft.revised.md` +
     `paper.draft.changes.md`).
   - In Zotero/`sync-refs` projects, once the author approves `<name>.keys.revised.md`, promote it
     to the build master (after saving `<name>.keys.pre-humanizer-<YYYY-MM-DD>.md`) or update
     `zotero.json`'s `"keys"` field. `check_manuscript.py` prefers `.revised.` over a stale
     `zotero.json` `"keys"` target so post-humanizer checks audit the latest file.
2. **In-place project workflow (standard in `sync-refs` repositories):**
   - Save a dated backup `<name>.keys.pre-humanizer-<YYYY-MM-DD>.md`, run the humanizer pass on
     `<name>.keys.md` (with `protect.txt`), then regenerate the numbered `<name>.md` and `.docx`
     via the project build scripts.
   - `check_manuscript.py` automatically ignores `*.changes.md` and `*.pre-humanizer*.md`.

| Responsibility | `academic-manuscript-writer` | `academic-humanizer` |
|---|---|---|
| Story spine, section order, figure sequence, central graphic | Owns | Preserves |
| Drafting new sections, Key Points, cover letter, declarations, rebuttals | Owns | Does not draft new content |
| Pre-submission adversarial review & cross-section consistency (`check_manuscript.py`) | Owns | Single-file token preservation (`preservation_check.py`) |
| Structural revision preservation check | Runs `preservation_check.py <orig> <structural>` when available | Owns script |
| Sentence-level AI-tell scrubbing & personal voice matching | Avoids structural tells while drafting | **Owns** (`edit` / `voice` mode) |
| Locked declaration sections | Emits under lock-safe headings | Locks as FAIL-protected spans |

## 2. Structural revision preservation check

Whenever `draft` mode restructures an author's existing manuscript into `<name>.structural.md`, run
`academic-humanizer`'s preservation checker (when installed) to ensure reordering did not silently
drop numbers, units, or citekeys:

```bash
python3 <humanizer-dir>/scripts/preservation_check.py <original.md> <name>.structural.md \
  [--protect protect-terms.txt]
```

Record the result (or note clearly if `academic-humanizer` is not installed locally) in
`revision-notes.md`.

## 3. Lock-safe declaration headings (verified against `preservation_check.py`)

`academic-humanizer/scripts/preservation_check.py` locks declarations using its `DECLARATION_HEAD`
regex. Use **separate, lock-safe heading prefixes** so every declaration is FAIL-protected:

- `### Ethics Approval` (or `### Ethics`) — **locked**
- `### Data Availability` — **locked** *(never merge into `Data and Code Availability` or rename to
  `Data Sharing Statement`, which `DECLARATION_HEAD` does not lock)*
- `### Code Availability` — **locked** *(separate heading whenever code availability is reported)*
- `### Funding` — **locked**
- `### Conflicts of Interest` (or `### Competing Interests`) — **locked**
- `### AI-Use Disclosure` (or `### Declaration of Generative AI`) — **locked**
- `### Author Contributions` / `### Acknowledgments` — **locked**

`check_manuscript.py` enforces this exact contract (`DEC-01` / `DEC-02`) and warns on non-lock-safe
variants (`Data and Code Availability`, `Data Sharing`, `IRB Statement`, `Financial Support`).

## 4. Meaning locks (pointer + high-frequency drafting reminders)

Follow all meaning locks defined in `academic-humanizer/SKILL.md` (causal vs. associational
language, certainty, null-result discipline, planned vs. completed work, modality, dropped
conditions, scope widening, precision, effect direction, and formal theorem/estimator assumptions)
alongside `preservation_check.py`'s token/declaration locks. Three restated here because they
matter most while drafting:

1. **Association vs. causation:** Never turn observational association (`associated with`,
   `linked to`) into causal verbs (`causes`, `drives`, `improves`, `reduces`, `yields`).
2. **Null-result discipline:** Never turn a confidence interval crossing null or `no evidence of
   difference` into `no effect`, `recovered similarly`, or `trended toward benefit`.
3. **Planned vs. completed work:** Never turn future/proposed analyses (`will`, `plan to`) into
   completed claims (`we tested`, `we added`).

## 5. Handoff artifacts

1. **`protect-terms.txt`** (or project `protect.txt`): plain text, one protected term per line,
   passed to `preservation_check.py --protect`.
2. **Handoff block in `revision-notes.md` (or `STATUS.md`):**

```markdown
## Handoff to academic-humanizer

- **Input file for humanizer:** `<path/to/paper.draft.md>` (or `<paper.keys.md>`)
- **Workflow mode:** `<standalone (.revised.md + .changes.md) | in-place with .pre-humanizer backup>`
- **Protect file:** `protect-terms.txt` (or `protect.txt`)
- **Recommended mode:** `edit` (or `voice` with author prior paper: `<sample_path>`)
- **Target venue & house style:** `<e.g., JAMA Network Open — AMA style (P < .001, percentage points, ≥, −)>`
- **Locked one-sentence thesis:** `<exact contribution sentence>`
- **Protected claim boundaries:**
  - `<e.g., Observational cohort: preserve "associated with"; never upgrade to causal verbs>`
  - `<e.g., Null subgroup CI crosses zero: never rewrite as "no effect" or "recovered similarly">`
- **Locked declaration headings (do not edit):** `Ethics Approval, Data Availability, Code Availability, Funding, Conflicts of Interest, AI-Use Disclosure`
- **Open items for author (do not guess in prose pass):** `<pending-author-data / [user-verify] items or None>`
```

## 6. Return signals from `academic-humanizer`

If `<input-stem>.changes.md` raises items under **Unresolved issues** or **Substantive proposals**,
return those items to the author or back to `academic-manuscript-writer` (`review` or `draft` mode)
rather than letting a prose pass rewrite claims. Re-run `scripts/check_manuscript.py` after any
structural edit.
