# academic-manuscript-writer

An agent skill for framing, planning, visually designing, drafting, adversarially stress-testing,
and revising scientific manuscripts across **Markdown**, **Word (`.docx`)**, and **LaTeX** —
calibrated for clinical, biomedical, and computational research.

Once structure, claims, declarations, and figures stabilize, it hands off cleanly to
[`koolkao/academic-humanizer`](https://github.com/koolkao/academic-humanizer) for final
sentence-level AI-tell scrubbing and author-voice matching.

## Use it

Paste this repo's URL into your agent (Claude Code, Codex, Cursor, or similar) and describe your
manuscript task:

```text
Use the skill at https://github.com/koolkao/academic-manuscript-writer to plan and red-team
draft-manuscript.md (target venue: JAMA Network Open, STROBE).
```

### Keep a local copy (optional)

Clone into your project's skills directory (Claude Code picks it up as `/academic-manuscript-writer`):

```bash
git clone https://github.com/koolkao/academic-manuscript-writer .claude/skills/academic-manuscript-writer
```

For unpublished manuscripts or sensitive clinical data, prefer a reviewed local copy over a live
URL and restrict network access in your agent settings.

## What it does

- **Story before prose, with Author Decision Gates.** Generates 2–4 supported candidate story
  spines, tests the contribution in one falsifiable sentence, tracks claims in a Claims-Evidence
  Ledger (`C01`, `C02`, …), and pauses for the author to confirm the spine before full drafting.
- **Standalone visual spine.** Strictly separates `[measured data]` from `[conceptual schematic]`,
  enforces the standalone caption test, supports multimodal visual audits of rendered figures, and
  offers three distinct synthesis-figure concepts when a synthesis graphic is warranted (opt-in for
  clinical reports under tight display caps).
- **Isolated four-lens adversarial review.** Runs in a fresh subagent using an explicit Isolation
  Brief (excluding `manuscript-plan.md` and `revision-notes.md`), applies a general 7-step
  per-claim attack procedure across study designs, verifies every finding against the full text
  before ranking, maps fixes on a 6-rung ladder, tracks unrun Rung 5–6 analyses honestly as
  `pending-author-data`, and stores status once in the Decision Matrix.
- **Submission deliverables & house style.** Applies venue house style (AMA `P < .001`,
  *Nature*-family, Vancouver/ICMJE, ML/computational) and drafts Key Points / Highlights,
  lock-safe Declarations (`Ethics Approval`, `Data Availability`, `Code Availability`, `Funding`,
  `Conflicts of Interest`, `AI-Use Disclosure`), Cover Letters, and quote-verified Response Letters.
- **Adapts to real projects.** Follows existing project conventions (`PLAN.md`, `STATUS.md`,
  `protect.txt`, `[PENDING: ...]`, `<name>.keys.md` vs. generated numbered `<name>.md`, `.bib` or
  checked refs JSON) rather than forcing parallel folders onto narrow tasks. Optionally integrates
  with external project-local keyed-Markdown → Zotero `.docx` build scripts (not bundled here).
- **Clean handoff to `academic-humanizer`.** Supports both standalone `.draft.md`/`.structural.md`
  → `.revised.md` and in-place `.pre-humanizer*.md` backup workflows, plus `preservation_check.py`
  verification when restructuring an existing draft.

## Modes

Five modes with explicit defaults; narrow requests get direct answers without multi-file folders:

| Mode | Use when… |
| --- | --- |
| `plan` *(default for raw notes)* | Finding the story (2–4 candidate spines + one-sentence thesis) or building `manuscript-plan.md` + `figure-plan.md` |
| `figure` | Designing figure sequences, rewriting captions, auditing rendered images, or comparing 3 synthesis-figure concepts |
| `draft` *(default for existing drafts)* | Drafting or restructuring sections, Key Points, Declarations, Cover Letter, and running the consistency sweep |
| `review` *(default for critique)* | Running an isolated four-lens pre-submission adversarial red-team (`adversarial-review.md`) |
| `respond` | Responding to real peer reviews (`rebuttal-plan.md` + quote-verified `response-letter.md`) |

## The checker (`scripts/check_manuscript.py`)

Requires **Python 3.9+** (standard library only; zero external dependencies).

```bash
python3 scripts/check_manuscript.py examples/computational-method
```

Sample output:

```text
# Manuscript Consistency Check

**Status:** PASS WITH WARNINGS (0 FAIL, 1 WARN)

## Summary
- Checked figure plan: figure-plan.md
- Checked manuscript plan: manuscript-plan.md
- Checked manuscript (md, stage=submission): draft-manuscript.md
- Word counts (draft-manuscript.md): total body=1363, abstract=150
- Checked bracketed citations against references.bib: 9 occurrence(s), 4 library key(s)
- Verified 3 quoted revision passage(s) in response-letter.md against manuscript
- Checked adversarial review: adversarial-review.md
- Checked rebuttal plan: rebuttal-plan.md

## FAIL
- None.

## WARN
- [WARN:REV-05] adversarial-review.md:43: open MAJOR finding M01 (Status: 'pending-author-data')
```

### Common flags

```bash
python3 scripts/check_manuscript.py path/to/manuscript-or-dir \
  [--stage draft|submission] \
  [--bib manuscript-refs.json|zotero.json|references.bib] \
  [--accept REF-04] [--accept-substring "specific phrase"] [--accept-file accepted.txt] \
  [--style] [--list-rules]
```

- **`--stage draft`** groups deliberate working markers (`[PENDING: ...]`, `TODO`, `TBD`,
  `pending-author-data`, `[user-verify]`, `[AUTHOR:...]`, `[OWNER:...]`) into one `WARN`
  (`PH-00`) so the checker is usable mid-draft; **`--stage submission`** (default) fails on them.
- **`--accept RULE_ID`** suppresses exact rule IDs; **`--accept-substring`** suppresses a specific
  message (≥ 8 chars). I/O errors (`IO-*`) are never suppressible, and FATAL review gates
  (`REV-00`, `REV-01`, `REV-02`, `REV-04`, `REV-06`) require explicit `--accept-fatal`.
- **`--style`** enables optional prose/style hints (`STY-01`–`STY-08`: reading instructions,
  counted prefaces, self-ranking, short subsections, acronym hygiene, observational causal verbs).
- **`--list-rules`** prints the full authoritative rule catalog directly from code.

### Key rules enforced (subset; run `--list-rules` for the complete table)

| Group | Rule IDs | Severity | What it checks |
| --- | --- | --- | --- |
| I/O & syntax | `IO-01`–`IO-05` | `FAIL` | Missing target/companion/`--accept-file`, malformed `.docx`, unclosed code fence or HTML comment (`IO-04`), invalid `--accept` |
| Placeholders | `PH-00`–`PH-11`, `PH-14`–`PH-15` | `FAIL` (`WARN` in draft) | Leftover `TODO`/`TBD`/`[PENDING]`/`pending-author-data`/`XX%`/`remove before submission`, broken Word refs, empty `[@]` / `{Citation}` (`PH-10`) |
| Citations | `CIT-01`, `CIT-02`, `CIT-04` | `FAIL` | Missing/unparseable `--bib` or `zotero.json` `"refs"` target (`CIT-01`), unknown citekey (`CIT-02`), unconverted literal `[@key]` in `.docx` (`CIT-04`) |
| References | `REF-01`, `REF-02` / `REF-04`–`REF-06` | `FAIL` / `WARN` | Dangling (`REF-01`) or orphaned (`REF-02`) main Figures/Tables (supports `### Table 1.`, `**Fig. 3 \| ...**`, wrapped lines); out-of-order first mentions (`REF-04`), figure-plan parity (`REF-05`), missing local image (`REF-06`) |
| Numbers & tables | `NUM-01`, `TAB-01` | `WARN` | Sign-aware Title/Key Points/Abstract/`## Summary`↔Body drift excluding References (`NUM-01`); precision-aware table `n (%)` / `n/N (%)` arithmetic & count > denominator (`TAB-01`) |
| Declarations & budgets | `DEC-01`, `DEC-02`, `BUD-01`–`BUD-03`, `LIM-01` | `WARN` | Exact `academic-humanizer` `DECLARATION_HEAD` lock-safe headings (`DEC-01`/`DEC-02`), word budgets (`BUD-*`), field-calibrated Discussion limitations share (`LIM-01`: >35% clinical / >25% computational) |
| Ledger | `LED-01`–`LED-04`, `LED-06` / `LED-05`, `LED-07` | `FAIL` / `WARN` | Missing/duplicate/invalid ledger IDs & statuses, verified claim without source (`LED-04`), gap targeting main section (`LED-06`); unverified claims (`LED-05`) & missing values (`LED-07`) |
| Adversarial review | `REV-00`, `REV-01`, `REV-02`, `REV-04`, `REV-06` / `REV-03`, `REV-05` | `FAIL` / `WARN` | Empty review (`REV-00`), deny-by-default unresolved `FATAL` (`REV-01`), inline-vs-matrix conflict (`REV-02`), unlocated resolved `FATAL` (`REV-04`), contradictory Verdict (`REV-06`), open `MAJOR` (`REV-05`) |
| Peer-review rebuttal | `REB-01`, `REB-02` / `REB-03`, `REB-04` | `FAIL` (`REB-01` `WARN` in draft) / `WARN` | Non-standard/unresolved rebuttal statuses (`REB-01`), verbatim quote mismatch in `response-letter.md` (`REB-02`), unverified letter (`REB-03`), rebuttal ID missing from letter (`REB-04`) |

## Examples

Both worked examples are **compact (~1,350–1,400 word) synthetic demonstrations** in Markdown +
Zotero `.bib` (labeled as illustrative fixtures):

- [`examples/clinical-cohort/`](examples/clinical-cohort/): STROBE-aligned clinical cohort
  demonstration (AMA style, Key Points, lock-safe Declarations, `protect-terms.txt`, pre-landmark
  spline, individual MCID responder rates, illustrative adversarial review with honest
  `pending-author-data` findings, and `academic-humanizer` handoff).
- [`examples/computational-method/`](examples/computational-method/): TRIPOD+AI-aligned medical-AI
  demonstration (*Nature*-family style, single-model evaluation matched to single-model latency,
  pooled + per-site external tables, lock-safe Declarations, `protect-terms.txt`). Includes both a
  pre-submission `adversarial-review.md` and a simulated post-decision `rebuttal-plan.md` +
  quote-verified `response-letter.md` to illustrate both workflow stages.

## Layout

```text
SKILL.md                  entry point for the agent
references/               story, figures, section craft, field/reporting, adversarial review, rebuttal, humanizer handoff
templates/                manuscript-plan, figure-plan, adversarial-review, revision-notes, rebuttal-plan, response-letter
scripts/                  check_manuscript.py (stdlib only; Python 3.9+; .md, .docx, .tex)
tests/                    unit, regression, rule-sync, CLI, and golden tests
examples/                 compact worked clinical cohort (AMA) and computational method (Nature style) demonstrations
evals/                    19 fixture-backed evaluation specs + fixtures/
docs/                     design notes and pinned source/license review
```

## Contributing & running tests

Run the full test suite (no third-party dependencies):

```bash
python3 -m unittest discover -s tests -v
```

Verify both worked examples:

```bash
python3 scripts/check_manuscript.py examples/clinical-cohort
python3 scripts/check_manuscript.py examples/computational-method
```

## Limits

- Agent adversarial review is pre-submission triage, not domain peer review or formal statistical
  sign-off.
- `scripts/check_manuscript.py` catches structural, citation-key, reference, arithmetic, quote, and
  numerical-drift defects heuristically; a clean run never proves scientific validity.
- This skill does not render plots, run statistical analyses on raw data, or bundle project-local
  `.docx`/Zotero build scripts.

## Credits and license

MIT License; see [`LICENSE`](LICENSE). All text and code are original. Conceptual influences and
pinned upstream revisions/licenses are documented in [`docs/source-review.md`](docs/source-review.md).
