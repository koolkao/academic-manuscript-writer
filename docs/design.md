# Design: academic-manuscript-writer

Date: 2026-11-21 (v0.3.0).

## Why

Researchers using AI for manuscripts hit two opposite failure modes: unguided LLMs produce
chronology-ordered prose padded with AI tells, defensive caveats, and subtle methodological errors;
heavy multi-agent pipelines bury straightforward papers in compliance paperwork and ML-conference
templates.

Meanwhile, the companion skill ([`koolkao/academic-humanizer`](https://github.com/koolkao/academic-humanizer),
v0.2.0) already solves sentence-level AI-tell removal, author-voice matching, and token-level
preservation checking — but refuses to frame a story, design figures, draft new sections,
restructure arguments, stress-test claims adversarially, or sweep cross-section consistency.

`academic-manuscript-writer` owns that structural, visual, drafting, adversarial-review, and
peer-review-response role across Markdown, Word (`.docx`), and LaTeX workflows, while fitting
existing project conventions (`PLAN.md`, `STATUS.md`, `protect.txt`, `[PENDING: ...]`,
`<name>.keys.md` vs. generated numbered `<name>.md`, and in-place `.pre-humanizer*.md` backups).

## Goals

- Turn raw results, tables, notes, or rough drafts into a coherent argument organized for readers,
  with explicit Author Decision Gates before full drafting or central claim narrowing.
- Make the figure sequence carry the paper with `[measured data]` vs. `[conceptual schematic]`
  separation and standalone captions (keeping 3-concept synthesis graphics opt-in for clinical
  reports under tight display caps).
- Catch fatal framing, methodological, and numerical flaws *before* submission through an isolated
  four-lens adversarial review built on a general 7-step per-claim attack procedure, mandatory
  finding verification before ranking, and single-source-of-truth matrix status.
- Enforce cross-section consistency with a zero-dependency stdlib checker
  (`scripts/check_manuscript.py`) supporting `--stage draft|submission`, exact Rule IDs +
  `--accept` / `--accept-substring` suppression, opt-in `--style`, numbered headings, heading-style
  captions, lock-safe declaration enforcement, and automated `response-letter.md` quote verification.
- Hand off cleanly to `koolkao/academic-humanizer` (both standalone `.revised.md` + promotion and
  in-place `.pre-humanizer*.md` backup workflows).

## Non-goals

- Rendering publication graphics, running statistical analyses on raw data (verification arithmetic
  is reported in review notes only; Rung 5–6 analyses are marked `pending-author-data`), or
  bundling project-specific `.docx`/Zotero assembly scripts.
- Sentence-level AI-tell humanization or author-voice cloning (owned by `academic-humanizer`).
- Forcing one discipline's conventions onto clinical, biomedical, computational, or review work.

## Key decisions

| Topic | Decision |
|---|---|
| Companion skill | [`koolkao/academic-humanizer`](https://github.com/koolkao/academic-humanizer) v0.2.0 (`53777ba`). `academic-manuscript-writer` writes `<name>.draft.<ext>`, `<name>.structural.<ext>`, or updates `<name>.keys.md` (with `.pre-*` backup) plus `protect-terms.txt` (or `protect.txt`); `academic-humanizer` writes `<input-stem>.revised.<ext>` and `<input-stem>.changes.md` (or runs in-place with `.pre-humanizer*.md` backup). Restructuring runs `preservation_check.py <original> <structural>` when installed. |
| Skill name & modes | `academic-manuscript-writer`. Five modes with explicit defaults: `plan` (default for raw notes/results; quick framing or full plan), `figure`, `draft` (default for restructuring/expanding drafts; includes sweep), `review` (default for critique), `respond` (rebuttal plan + quote-verified response letter). |
| Real project fit | "Project conventions first": adopt existing `PLAN.md`, `STATUS.md`, `protect.txt`, `[PENDING: ...]` markers, and `zotero.json` → `manuscript-refs.json`; edit `<name>.keys.md` and never hand-edit generated numbered `<name>.md`. |
| Adversarial review | Fresh-subagent Isolation Brief (passing manuscript, data/tables/figures, venue, `references/adversarial-review.md`, reporting guideline; excluding `manuscript-plan.md` and `revision-notes.md`), general 7-step per-claim attack procedure, Findings Verification Step before ranking, four mutually exclusive exhaustive verdict tiers, single-source status in the Decision Matrix, and no filler quotas. |
| Python checker | Stdlib-only `scripts/check_manuscript.py` (Python 3.9+; `.md`, `.docx`, `.tex`): deny-by-default fail-closed `FATAL` gate, unified `normalize_heading()`, `--stage draft|submission`, `--list-rules`, safe `--accept` / `--accept-substring`, opt-in `--style`, exact humanizer `DECLARATION_HEAD` enforcement (`DEC-01`/`DEC-02`), submission rebuttal status enforcement (`REB-01`), and mechanical `response-letter.md` verbatim quote check (`REB-02`–`REB-04`). |
| Licensing | 100% original text and code under MIT; upstream sources reviewed and pinned in `docs/source-review.md`. |

## Key architecture notes

- **Cross-skill alignment:** Meaning locks point to `academic-humanizer/SKILL.md`; lock-safe
  declaration headings match `preservation_check.py`'s exact `DECLARATION_HEAD` regex (verified by
  test); Claims-Evidence Ledger IDs (`C01`… with `verified | unverified | gap`) align with
  `koolkao/academic-video-scriptwriter`.
- **Worked examples:** Both [`examples/clinical-cohort/`](../examples/clinical-cohort/) and
  [`examples/computational-method/`](../examples/computational-method/) are compact (~1,350–1,400
  word) synthetic demonstrations in Markdown + Zotero `.bib`, regression-tested by golden tests in
  `tests/test_check_manuscript.py`.
