# Changelog

## 0.3.0 (2026-11-21) — First public release

Initial public release of `academic-manuscript-writer` under the MIT License.

- **Core skill & 5 modes (`SKILL.md`):** `plan` (default for raw notes/results), `figure`, `draft`
  (default for existing manuscripts, including consistency sweep), `review` (default for critique),
  and `respond` (point-by-point rebuttal + response letter), with explicit Author Decision Gates
  and a "project conventions first" contract (`PLAN.md`, `STATUS.md`, `protect.txt`,
  `[PENDING: ...]`, keyed `.keys.md` vs. generated numbered `.md`).
- **References & templates (`references/`, `templates/`):**
  - Story framing, candidate spines, one-sentence contribution test, and Claims-Evidence Ledger.
  - Standalone figure sequencing, `[measured data]` vs. `[conceptual schematic]` boundary,
    multimodal visual audit, and optional 3-concept central synthesis figures.
  - Field-calibrated drafting craft, venue house style (AMA, Vancouver/ICMJE, *Nature*-family,
    ML/computational), reporting pointers (STROBE, CONSORT, TRIPOD+AI, PRISMA, ARRIVE), and
    optional keyed-Markdown + Zotero/`.docx` workflow notes.
  - Isolated four-lens adversarial review with Subagent Isolation Brief, general 7-step per-claim
    attack procedure, Findings Verification Step, four mutually exclusive verdict tiers, 6-rung
    minimum-defensible-fix ladder, `pending-author-data` honesty, and single-source matrix status.
  - Peer-review rebuttal workflow (`rebuttal-plan.md` + `response-letter.md`) and clean handoff
    contract with [`koolkao/academic-humanizer`](https://github.com/koolkao/academic-humanizer)
    (v0.2.0) including exact `DECLARATION_HEAD`-safe declaration headings and structural
    `preservation_check.py` verification.
- **Zero-dependency consistency checker (`scripts/check_manuscript.py`, Python 3.9+):**
  - Supports Markdown (`.md`, `.qmd`, `.Rmd`), Word (`.docx`), and LaTeX (`.tex`) plus companion
    artifacts and bibliography files (`.bib`, checked refs JSON, `zotero.json` `"refs"` pointers,
    CSL-JSON).
  - Deny-by-default fail-closed `FATAL` review gate, `--stage draft|submission`, authoritative
    `--list-rules` catalog, safe `--accept` / `--accept-substring` / `--accept-file` suppression,
    unclosed code-fence/HTML-comment detection (`IO-04`), exact `academic-humanizer` lock-safe
    declaration checks (`DEC-01`/`DEC-02`), sign-aware Abstract↔Body number drift (`NUM-01`),
    paragraph-joined Figure/Table reference auditing (`REF-01`–`REF-06`), precision-aware table
    arithmetic (`TAB-01`), submission rebuttal enforcement (`REB-01`), mechanical response-letter
    quote verification (`REB-02`–`REB-04`), and opt-in `--style` checks.
- **Worked demonstrations, evaluation specs & CI (`examples/`, `evals/`, `tests/`, `.github/`):**
  - Compact synthetic clinical cohort (AMA/STROBE) and computational medical-AI (*Nature*/TRIPOD+AI)
    demonstrations with Zotero `.bib`, lock-safe declarations, and `protect-terms.txt`.
  - 19 fixture-backed evaluation cases (including observational and held-out RCT/diagnostic
    false-negative controls and a clean false-positive control).
  - Table-driven unit, regression, CLI, rule-catalog sync, and golden tests run on Python 3.9 and
    3.13 via GitHub Actions.
