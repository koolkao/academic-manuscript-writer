"""Unit, regression, rule-catalog sync, CLI, and golden tests for scripts/check_manuscript.py."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_manuscript as cm  # noqa: E402


def _make_args(**overrides) -> argparse.Namespace:
    base = dict(
        stage="submission",
        accept=[],
        accept_substring=[],
        accept_file=None,
        accept_fatal=False,
        style=False,
        plan=None,
        figure_plan=None,
        review=None,
        rebuttal=None,
        response=None,
        bib=None,
        max_abstract=None,
        max_words=None,
        format="auto",
    )
    base.update(overrides)
    return argparse.Namespace(**base)


def _write_docx(path: Path, body_xml: str) -> None:
    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body_xml}</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", xml)


class TestCheckManuscript(unittest.TestCase):
    def test_fatal_gate_deny_by_default_matrix_and_inline_variants(self) -> None:
        """Every FATAL formatting/table/empty-review variant must fail closed unless located & resolved."""
        fail_cases = [
            ("unbracketed bold", "- **FATAL** F1 — no control arm. Status: open\n"),
            ("colon prose", "FATAL: outcome switched after unblinding.\n"),
            ("bold matrix cell", "## Impact\n| ID | Severity | Status |\n|---|---|---|\n| F1 | **FATAL** | open |\n"),
            ("annotated severity", "## Impact\n| ID | Severity | Status |\n|---|---|---|\n| F1 | FATAL (methods) | open |\n"),
            ("alt heading name", "## Decision Matrix\n| ID | Severity | Status |\n|---|---|---|\n| F1 | FATAL | open |\n"),
            ("h3 matrix heading", "### Matrix\n| ID | Severity | Status |\n|---|---|---|\n| F1 | FATAL | open |\n"),
            ("second table", "## Impact\n| A | B |\n|---|---|\n| 1 | 2 |\n\n| ID | Severity | Status |\n|---|---|---|\n| F1 | FATAL | open |\n"),
            ("finding column name", "## Matrix\n| Finding | Severity | Status |\n|---|---|---|\n| F1 | FATAL | open |\n"),
            ("empty review", "# Adversarial Review\n"),
            ("prose fatal claim", "# Review\nTwo FATAL findings remain open in Methods.\n"),
            ("tbd locator", "## Matrix\n| ID | Severity | Status |\n|---|---|---|\n| F1 | FATAL | resolved (TBD) |\n"),
            ("unlocated accepted-risk", "## Matrix\n| ID | Severity | Status |\n|---|---|---|\n| F1 | FATAL | accepted-risk |\n"),
            ("inline vs matrix conflict", "- [MAJOR] M01 — bad\n## Matrix\n| ID | Severity | Status |\n|---|---|---|\n| M01 | FATAL | open |\n"),
            ("contradictory verdict", "- **Verdict:** Ready after minor fixes\n## Matrix\n| ID | Severity | Status |\n|---|---|---|\n| F1 | FATAL | open |\n"),
        ]
        with tempfile.TemporaryDirectory() as td:
            for label, content in fail_cases:
                with self.subTest(case=label):
                    rev = Path(td) / "adversarial-review.md"
                    rev.write_text(content, encoding="utf-8")
                    rep = cm.run_checks(rev, _make_args())
                    self.assertTrue(rep.fails, f"Expected FAIL for {label}, got {rep}")

            # Resolved with concrete locator + fenced template example should PASS
            ok_rev = Path(td) / "adversarial-review.md"
            ok_rev.write_text(
                "# Adversarial Review\n"
                "```markdown\n- [FATAL] M99 — template quote inside fence\n```\n"
                "## Impact × Effort Decision Matrix\n"
                "| ID | Severity | Status |\n|---|---|---|\n"
                "| M01 | FATAL | Resolved (see Methods — Landmark Alignment) |\n",
                encoding="utf-8",
            )
            rep_ok = cm.run_checks(ok_rev, _make_args())
            self.assertEqual(rep_ok.fails, [])

    def test_accept_safety_non_suppressible_fatal_and_pre_grouping(self) -> None:
        """Empty/bad --accept fails; FATAL/IO require protection; PH-03 suppresses before PH-00 grouping."""
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            rev = d / "adversarial-review.md"
            rev.write_text("## Matrix\n| ID | Severity | Status |\n|---|---|---|\n| M01 | FATAL | open |\n")

            # Empty token rejected
            rep_empty = cm.run_checks(rev, _make_args(accept=[""]))
            self.assertIn("IO-05", [f.rule for f in rep_empty.fails])

            # Substring rejected on --accept; REV-01 cannot be suppressed without --accept-fatal
            rep_no_fatal = cm.run_checks(rev, _make_args(accept=["REV-01"]))
            self.assertIn("REV-01", [f.rule for f in rep_no_fatal.fails])

            rep_with_fatal = cm.run_checks(rev, _make_args(accept=["REV-01"], accept_fatal=True))
            self.assertEqual(rep_with_fatal.fails, [])
            self.assertIn("PASS WITH ACCEPTED", cm.format_report(rep_with_fatal))

            # Missing --accept-file fails cleanly
            rep_missing_af = cm.run_checks(rev, _make_args(accept_file=str(d / "no-such.txt")))
            self.assertIn("IO-01", [f.rule for f in rep_missing_af.fails])

            # 12 [PENDING] markers accepted via --accept PH-03 before grouping into PH-00
            ph_dir = d / "ph"
            ph_dir.mkdir()
            ms = ph_dir / "paper.draft.md"
            ms.write_text("# T\n\n## Intro\n" + "\n".join(f"[PENDING: item {i}]" for i in range(12)) + "\n")
            rep_ph = cm.run_checks(ms, _make_args(accept=["PH-03"]))
            self.assertEqual(rep_ph.fails, [])
            self.assertEqual(len(rep_ph.accepted), 12)

    def test_unclosed_code_fence_and_html_comment_fail(self) -> None:
        """Unclosed fences or HTML comments must emit IO-04 FAIL instead of hiding text."""
        with tempfile.TemporaryDirectory() as td:
            for name, txt in [
                ("fence.md", "# T\n\n## Methods\n```\ncode\nTODO hidden\n"),
                ("comment.md", "# T\n\n## Methods\n<!-- unclosed\nTODO hidden\n"),
            ]:
                with self.subTest(name=name):
                    p = Path(td) / name
                    p.write_text(txt, encoding="utf-8")
                    rep = cm.run_checks(p, _make_args())
                    self.assertIn("IO-04", [f.rule for f in rep.fails])

    def test_declaration_lock_safety_matches_humanizer_regex(self) -> None:
        """Numbered headings and bold run-ins must emit DEC-02 and NOT satisfy DEC-01."""
        with tempfile.TemporaryDirectory() as td:
            ms = Path(td) / "paper.draft.md"
            filler = " ".join(["word"] * 420)
            ms.write_text(
                f"# Title\n\n## 1. Introduction\n{filler}\n\n"
                "## Declarations\n"
                "### 6.1 Funding\nNone.\n"
                "**Data Availability.** Available.\n"
                "### Data and Code Availability\nCombined.\n"
                "### Ethics Approval\nApproved.\n",
                encoding="utf-8",
            )
            rep = cm.run_checks(ms, _make_args())
            dec2 = [w.msg for w in rep.warns if w.rule == "DEC-02"]
            dec1 = [w.msg for w in rep.warns if w.rule == "DEC-01"]
            self.assertTrue(any("6.1 Funding" in m for m in dec2))
            self.assertTrue(any("Data Availability" in m for m in dec2))
            self.assertTrue(any("Data and Code Availability" in m for m in dec2))
            # Funding and Data Availability were NOT bare headings, so DEC-01 flags them missing
            self.assertTrue(any("Funding" in m and "Data Availability" in m for m in dec1))

        # Cross-check HUMANIZER_DECLARATION_HEAD against canonical headings (and sibling repo if installed)
        for heading, expected in [
            ("### Ethics Approval", True),
            ("### Data Availability", True),
            ("### Code Availability", True),
            ("### Funding", True),
            ("### Conflicts of Interest", True),
            ("### AI-Use Disclosure", True),
            ("### 6.1 Funding", False),
            ("### Data and Code Availability", False),
            ("**Funding.** None.", False),
        ]:
            self.assertEqual(bool(cm.HUMANIZER_DECLARATION_HEAD.match(heading)), expected, heading)
        sibling = next((p for p in ROOT.parent.glob("academic-humanizer*/scripts/preservation_check.py")), None)
        if sibling is not None:
            src = sibling.read_text(encoding="utf-8")
            self.assertIn("DECLARATION_HEAD", src)

    def test_response_letter_quote_normalization_comments_and_missing_ids(self) -> None:
        """REB-02 handles emphasis/curly quotes/citations/ellipsis, ignores HTML comments, and flags silent letters/missing IDs."""
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            ms = d / "paper.draft.md"
            ms.write_text(
                "# Title\n\n## Methods\n"
                "We used *strict* patient-disjoint splits across three sites [@smith2020] with **zero** leakage.\n"
                "<!-- old hidden sentence that must not verify as live prose -->\n",
                encoding="utf-8",
            )
            reb = d / "rebuttal-plan.md"
            reb.write_text(
                "## Atomic Reviewer Critiques\n"
                "| ID | Reviewer | Target manuscript location | Status |\n|---|---|---|---|\n"
                "| R1.1 | Split | Methods | resolved |\n"
                "| R1.2 | Extra | Results | resolved |\n",
                encoding="utf-8",
            )
            letter = d / "response-letter.md"
            letter.write_text(
                "### Comment R1.1\n"
                "**Revised text:** “We used strict patient-disjoint splits... with zero leakage.”\n\n"
                "### Comment R1.1b\n"
                "**Manuscript revision:**\n"
                "> \"old hidden sentence that must not verify as live prose\"\n",
                encoding="utf-8",
            )
            rep = cm.run_checks(d, _make_args())
            # First quote (with dropped emphasis, curly quotes, stripped citation, ellipsis) PASSES;
            # second quote (only in HTML comment) FAILS REB-02; missing R1.2 WARNS REB-04
            reb2 = [f for f in rep.fails if f.rule == "REB-02"]
            self.assertEqual(len(reb2), 1)
            self.assertIn("old hidden sentence", reb2[0].msg)
            self.assertIn("REB-04", [w.rule for w in rep.warns])

            # Letter with no revision markers triggers REB-03 WARN
            letter.write_text("Dear Editor, we fixed everything.\n")
            rep_silent = cm.run_checks(d, _make_args())
            self.assertIn("REB-03", [w.rule for w in rep_silent.warns])

    def test_figures_tables_wrapped_locators_nature_pipes_and_external_refs(self) -> None:
        """Wrapped 'Figure\\n2', citation locators, local 'in Section', Nature pipe captions, and external refs work."""
        with tempfile.TemporaryDirectory() as td:
            ms = Path(td) / "paper.draft.md"
            ms.write_text(
                "# Title\n\n## Results\n"
                "See Table 2 and 14 exploratory analyses, Table 3 of Smith et al.,\n"
                "and prior results [@smith2020, p. 12, Table 9; @lee2021, Figure 8].\n"
                "As shown in Figure\n2 in Section 3 and Table 1 in Methods (plus Figure 5 in the Supplement),\n"
                "and Fig. 3 below.\n"
                "Table 2. Patients in the wrapped continuation line are not a caption.\n\n"
                "### Table 1. Baseline.\n\n"
                "**Table 2.** Secondary.\n\n"
                "**Figure 2.** Wrapped ref works.\n\n"
                "**Fig. 3 | Nature-style pipe caption.** Works too.\n",
                encoding="utf-8",
            )
            rep = cm.run_checks(ms, _make_args())
            self.assertEqual([f for f in rep.fails if f.rule in {"REF-01", "REF-02"}], [])

    def test_table_arithmetic_continuous_rows_fractions_and_overflow(self) -> None:
        """Mean (SD) rows skipped; n/N (%) checked; count > denom warned; bold/footnotes stripped."""
        with tempfile.TemporaryDirectory() as td:
            ms = Path(td) / "paper.draft.md"
            ms.write_text(
                "# T\n\n## Results\nSee Table 1.\n\n**Table 1.** Summary.\n\n"
                "Metric | Group A (n = 100), No. (%)\n"
                "--- | ---\n"
                "Age, mean (SD), y | 54 (12)\n"
                "Female, No. (%) | **50 (50.0)**†\n"
                "Subset assessed | 25/50 (50.0%)\n"
                "Bad fraction | 10/50 (40.0%)\n"
                "Overflow row | 130 (130.0)\n",
                encoding="utf-8",
            )
            rep = cm.run_checks(ms, _make_args())
            tab_warns = [w.msg for w in rep.warns if w.rule == "TAB-01"]
            self.assertEqual(len(tab_warns), 2)
            self.assertTrue(any("10/50" in m for m in tab_warns))
            self.assertTrue(any("130 > 100" in m for m in tab_warns))

    def test_headings_normalization_summary_isolation_and_placeholders(self) -> None:
        """normalize_heading preserves 3D/2020, strips Roman/bold; second Summary not absorbed; XX% caught."""
        self.assertEqual(cm.normalize_heading("3D Reconstruction Methods"), "3D Reconstruction Methods")
        self.assertEqual(cm.normalize_heading("2020 Cohort Results"), "2020 Cohort Results")
        self.assertEqual(cm.normalize_heading("II. Methods"), "Methods")
        self.assertEqual(cm.normalize_heading("**6.7 Limitations**"), "Limitations")
        self.assertEqual(cm.normalize_heading("(1) Introduction"), "Introduction")

        with tempfile.TemporaryDirectory() as td:
            ms = Path(td) / "paper.draft.md"
            ms.write_text(
                "# Title\n\n## Abstract\nEffect was +4.1.\n\n## Results\nEffect was +4.1 with XX% missing.\n\n"
                "## Summary and Outlook\nFuture cohort target is 999.\n",
                encoding="utf-8",
            )
            rep = cm.run_checks(ms, _make_args())
            self.assertEqual([w for w in rep.warns if w.rule == "NUM-01"], [])
            self.assertIn("PH-14", [f.rule for f in rep.fails])

    def test_missing_companion_flags_and_docx_deleted_text(self) -> None:
        """Nonexistent companion flags fail cleanly with IO-01 (no traceback); docx w:del ignored."""
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            ms = d / "paper.draft.md"
            ms.write_text("# T\n\n## Intro\nClean text.\n")
            rep = cm.run_checks(ms, _make_args(review=str(d / "missing-review.md")))
            self.assertIn("IO-01", [f.rule for f in rep.fails])

            docx = d / "paper.docx"
            _write_docx(
                docx,
                '<w:p><w:r><w:t>Clean text.</w:t></w:r>'
                '<w:del><w:r><w:delText>TODO [@deleted]</w:delText></w:r></w:del></w:p>',
            )
            rep_d = cm.run_checks(docx, _make_args())
            self.assertEqual(rep_d.fails, [])

    def test_rule_catalog_sync_with_code_and_readme(self) -> None:
        """Every rule ID in code and README must exist in RULE_CATALOG with consistent naming."""
        catalog_ids = {rid for rid, _, _ in cm.RULE_CATALOG}
        src = (ROOT / "scripts" / "check_manuscript.py").read_text(encoding="utf-8")
        # Every emitted rule ID literal inside report.fail/warn or pattern tuples
        code_ids = set(re.findall(r'"([A-Z]{2,3}-\d{2})"', src))
        self.assertTrue(code_ids <= catalog_ids, f"Rules in code missing from RULE_CATALOG: {code_ids - catalog_ids}")

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_ids = set(re.findall(r"`([A-Z]{2,3}-\d{2})`", readme))
        self.assertTrue(readme_ids <= catalog_ids, f"Unknown rule IDs in README.md: {readme_ids - catalog_ids}")

        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_manuscript.py"), "--list-rules"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("`REV-01`", proc.stdout)
        self.assertIn("`REB-02`", proc.stdout)

    def test_golden_worked_examples_fixtures_and_cli_exit_codes(self) -> None:
        """Golden verification of both worked examples, clean fixture, held-out RCT fixture, and CLI exits."""
        ex1 = cm.run_checks(ROOT / "examples" / "clinical-cohort", _make_args())
        self.assertEqual(ex1.fails, [])
        self.assertTrue(all(w.rule == "REV-05" for w in ex1.warns), ex1.warns)

        ex2 = cm.run_checks(ROOT / "examples" / "computational-method", _make_args())
        self.assertEqual(ex2.fails, [])
        self.assertTrue(all(w.rule == "REV-05" for w in ex2.warns), ex2.warns)
        self.assertTrue(any("Verified 3 quoted revision" in n for n in ex2.notes))

        sound = cm.run_checks(ROOT / "evals" / "fixtures" / "sound-clinical-short.md", _make_args())
        self.assertEqual(sound.fails, [])

        rct = cm.run_checks(ROOT / "evals" / "fixtures" / "flawed-rct-diagnostic.md", _make_args())
        self.assertIn("TAB-01", [w.rule for w in rct.warns])

        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_manuscript.py"), str(ROOT / "examples" / "computational-method")],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("PASS WITH WARNINGS", proc.stdout)


if __name__ == "__main__":
    unittest.main()
