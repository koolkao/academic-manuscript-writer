#!/usr/bin/env python3
"""Cross-section, reference, arithmetic, and artifact consistency checker for
academic-manuscript-writer.

Supports Markdown (.md, primary), Word (.docx), and LaTeX (.tex) manuscripts, plus companion
artifacts (manuscript-plan.md / PLAN.md, figure-plan.md, adversarial-review.md, rebuttal-plan.md,
response-letter.md) and Zotero reference files (checked refs JSON {key:{text,doi,src}},
zotero.json config wrapper pointing to refs, .bib, or Better BibTeX CSL-JSON).

Usage:
    python3 scripts/check_manuscript.py TARGET [options]

Options:
    --stage {draft,submission}  In 'draft' stage, deliberate working markers ([PENDING:...],
                                TODO, TBD, pending-author-data, [user-verify], [AUTHOR:...])
                                are grouped into one WARN instead of FAIL. Default: submission.
    --accept RULE_ID            Suppress an exact rule ID (e.g. REF-04; repeatable). Critical
                                IO-* rules are never suppressible; FATAL review gates require
                                --accept-fatal.
    --accept-substring TEXT     Suppress findings whose message contains TEXT (min 8 chars;
                                repeatable).
    --accept-file FILE          File with one accepted rule ID (or 'sub:TEXT') per line.
    --accept-fatal              Explicitly allow --accept on FATAL review gate rules (REV-*).
    --list-rules                Print the authoritative rule-ID catalog as a Markdown table.
    --style                     Enable opt-in prose/style WARNs (acronyms, short subsections,
                                structural tells, observational causal-verb lint).
    --bib FILE                  Checked refs JSON, zotero.json wrapper, .bib, or Better BibTeX JSON.
    --plan FILE                 Path to manuscript-plan.md (or project PLAN.md).
    --figure-plan FILE          Path to figure-plan.md.
    --review FILE               Path to adversarial-review.md.
    --rebuttal FILE             Path to rebuttal-plan.md.
    --response FILE             Path to response-letter.md (enables verbatim quote check).
    --max-abstract N            Override Abstract word limit.
    --max-words N               Override main body prose word limit.
    --format {auto,md,tex,docx} Force manuscript format.

Standard library only. Reads files and prints a Markdown report; modifies nothing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

ARTIFACT_NAMES = {
    "manuscript-plan.md",
    "figure-plan.md",
    "adversarial-review.md",
    "revision-notes.md",
    "rebuttal-plan.md",
    "response-letter.md",
    "cover-letter.md",
    "key-points.md",
    "readme.md",
    "claude.md",
    "agents.md",
    "gemini.md",
    "plan.md",
    "status.md",
    "outline.md",
    "validation-plan.md",
    "handoff.md",
    "changelog.md",
}

NON_MANUSCRIPT_PATTERNS = (
    re.compile(r"\.(?:changes|diff|review)\.md$", re.I),
    re.compile(r"\.pre-humanizer[^/]*\.md$", re.I),
    re.compile(r"^supplement", re.I),
)

# Working markers: FAIL at submission, grouped WARN at draft stage
WORKING_MARKER_PATTERNS = [
    ("PH-01", re.compile(r"\b(?:TODO|TBD|FIXME)\b"), "working marker"),
    ("PH-02", re.compile(r"\[(?:citation needed|ref needed|insert [^\]]*|TBD|TODO|XXX|\?\?|N|REF|CITE)\]", re.I), "bracketed placeholder"),
    ("PH-03", re.compile(r"\[PENDING(?::[^\]]*)?\]", re.I), "[PENDING] marker"),
    ("PH-04", re.compile(r"\bpending-author-data\b", re.I), "pending-author-data marker"),
    ("PH-05", re.compile(r"\[user-verify(?::[^\]]*)?\]", re.I), "[user-verify] marker"),
    ("PH-06", re.compile(r"\[(?:AUTHOR|OWNER):[^\]]*\]", re.I), "author/owner working marker"),
    ("PH-14", re.compile(r"(?:\bXX+%|\b[nN]\s*=\s*XX+\b|\b[pP]\s*=\s*0?\.XX+\b)"), "numeric XX placeholder"),
    ("PH-15", re.compile(r"\b(?:remove\s+before\s+submission|not\s+for\s+submission)\b", re.I), "internal-only submission note"),
]

# Always-FAIL broken technical tokens (even in draft stage)
BROKEN_TOKEN_PATTERNS = [
    ("PH-07", re.compile(r"Error!\s*(?:Reference source not found|Bookmark not defined)\.?", re.I), "Word broken cross-reference error"),
    ("PH-08", re.compile(r"\[@\s*\]"), "empty citation bracket"),
    ("PH-09", re.compile(r"\[@(?:TODO|TBD|cite|ref|xxx|placeholder)\b[^\]]*\]", re.I), "placeholder citation key"),
    ("PH-10", re.compile(r"\{Citation\}|\[Citation error\]"), "unresolved Zotero citation placeholder"),
    ("PH-11", re.compile(r"\\(?:cite[a-zA-Z]*|ref|cref|Cref|autoref|eqref)\{\s*\}"), "empty LaTeX citation/reference"),
]

# Standalone ambiguous tokens: WARN (not FAIL) to avoid false FAILs on Roman numerals or punctuation
SOFT_PLACEHOLDER_PATTERNS = [
    ("PH-12", re.compile(r"(?<!\w)\?\?(?!\w)"), "double question mark '??'"),
    ("PH-13", re.compile(r"\bXXX\b"), "possible placeholder 'XXX'"),
    ("PH-16", re.compile(r"\[[A-Z]{3,}(?::[^\]]*)?\]"), "uppercase bracketed marker"),
]

# Authoritative rule catalog (used by --list-rules and verified against README by unit tests)
RULE_CATALOG: list[tuple[str, str, str]] = [
    ("IO-01", "FAIL", "Target, companion artifact, or --accept-file path does not exist"),
    ("IO-02", "FAIL", "Invalid or malformed .docx archive"),
    ("IO-03", "FAIL", "No manuscript or companion artifacts found"),
    ("IO-04", "FAIL", "Unclosed Markdown code fence or HTML comment hiding downstream text"),
    ("IO-05", "FAIL", "Invalid --accept or --accept-substring argument"),
    ("DIS-01", "FAIL", "Ambiguous directory with multiple generic manuscripts; pass an explicit file"),
    ("DIS-02", "WARN", "Multiple manuscript candidates found; selected highest-ranked file"),
    ("DIS-03", "WARN", "Directory mode selected a generic Markdown file (pass an explicit file to confirm)"),
    ("PH-00", "FAIL/WARN", "Grouped working markers (WARN at --stage draft; FAIL if >10 at --stage submission)"),
    ("PH-01", "FAIL/WARN", "TODO / TBD / FIXME working marker"),
    ("PH-02", "FAIL/WARN", "Bracketed placeholder ([citation needed], [N], [REF], [CITE], [TBD], etc.)"),
    ("PH-03", "FAIL/WARN", "[PENDING: ...] working marker"),
    ("PH-04", "FAIL/WARN", "pending-author-data marker"),
    ("PH-05", "FAIL/WARN", "[user-verify] marker"),
    ("PH-06", "FAIL/WARN", "[AUTHOR: ...] or [OWNER: ...] working marker"),
    ("PH-07", "FAIL", "Word broken cross-reference error"),
    ("PH-08", "FAIL", "Empty citation bracket [@]"),
    ("PH-09", "FAIL", "Placeholder citation key ([@TODO], [@cite], etc.)"),
    ("PH-10", "FAIL", "Unresolved Zotero {Citation} or [Citation error] placeholder"),
    ("PH-11", "FAIL", "Empty LaTeX citation or reference command"),
    ("PH-12", "WARN", "Standalone double question mark '??'"),
    ("PH-13", "WARN", "Standalone 'XXX' token"),
    ("PH-14", "FAIL/WARN", "Numeric XX placeholder (XX%, n = XX, P = 0.XX)"),
    ("PH-15", "FAIL/WARN", "Internal-only submission note ('remove before submission' / 'not for submission')"),
    ("PH-16", "WARN", "Generic uppercase bracketed marker ([DRAFT], [INJECT], etc.)"),
    ("CIT-01", "FAIL", "Missing or unparseable bibliography / zotero.json 'refs' target"),
    ("CIT-02", "FAIL", "Citation key not found in bibliography / checked refs JSON"),
    ("CIT-03", "WARN", "CSL-JSON uses URI IDs without 'citation-key'"),
    ("CIT-04", "FAIL", "Unconverted literal [@key] citation survived into .docx"),
    ("CIT-05", "WARN", "Bibliography loaded but zero bracketed citekeys found in manuscript"),
    ("REF-01", "FAIL", "Dangling Figure or Table reference (not defined in captions/labels)"),
    ("REF-02", "FAIL", "Orphaned Figure or Table caption (never referenced in body prose)"),
    ("REF-04", "WARN", "Out-of-order first Figure or Table mention"),
    ("REF-05", "WARN", "Figure/Table count parity mismatch with figure-plan.md"),
    ("REF-06", "WARN", "Referenced local figure image path does not exist"),
    ("NUM-01", "WARN", "Title, Key Points, or Abstract number missing or sign-flipped in body/tables/captions"),
    ("TAB-01", "WARN", "Table count/percentage arithmetic mismatch or count exceeding denominator"),
    ("DEC-01", "WARN", "Missing lock-safe declaration heading (academic-humanizer DECLARATION_HEAD)"),
    ("DEC-02", "WARN", "Declaration heading/label is not auto-locked by academic-humanizer"),
    ("BUD-01", "WARN", "Abstract exceeds word budget"),
    ("BUD-02", "WARN", "Main body exceeds word budget"),
    ("BUD-03", "WARN", "Section exceeds plan word budget by >15%"),
    ("LIM-01", "WARN", "Discussion Limitations share exceeds field threshold (35% clinical / 25% computational)"),
    ("PLN-01", "WARN", "manuscript-plan.md missing concrete 'One-sentence contribution'"),
    ("PLN-02", "WARN", "manuscript-plan.md missing or empty Claims-Evidence Ledger"),
    ("LED-01", "FAIL", "Claims-Evidence Ledger row missing ID"),
    ("LED-02", "FAIL", "Duplicate claim ID in Claims-Evidence Ledger"),
    ("LED-03", "FAIL", "Invalid claim status in Claims-Evidence Ledger"),
    ("LED-04", "FAIL", "Verified claim has no concrete evidence source"),
    ("LED-05", "WARN", "Claim in ledger is still 'unverified'"),
    ("LED-06", "FAIL", "Gap claim targets a main manuscript section"),
    ("LED-07", "WARN", "Verified claim value(s) missing from manuscript"),
    ("REV-00", "FAIL", "Adversarial review file is empty or contains no parseable findings/matrix"),
    ("REV-01", "FAIL", "Unresolved or unaccounted FATAL finding in adversarial review"),
    ("REV-02", "FAIL/WARN", "Inline vs. matrix severity or status conflict in adversarial review"),
    ("REV-03", "WARN", "Unrecognized status value in adversarial review matrix"),
    ("REV-04", "FAIL", "FATAL finding marked resolved/narrowed without a concrete locator (or accepted-risk without attestation)"),
    ("REV-05", "WARN", "Open MAJOR finding in adversarial review"),
    ("REV-06", "FAIL/WARN", "Submission Verdict contradicts open FATAL (FAIL) or MAJOR (WARN) findings"),
    ("REB-01", "FAIL/WARN", "Invalid, unresolved, or unlocated item in rebuttal-plan.md (FAIL at submission, WARN at draft)"),
    ("REB-02", "FAIL", "Quoted manuscript revision in response-letter.md not found verbatim in manuscript"),
    ("REB-03", "WARN", "response-letter.md has zero verified revision quotes or unchecked quoted blockquotes"),
    ("REB-04", "WARN", "Critique ID in rebuttal-plan.md missing from response-letter.md"),
    ("STY-01", "WARN", "[--style] Reading instruction ('interpreted with caution')"),
    ("STY-02", "WARN", "[--style] Reading instruction ('readers should note/bear in mind')"),
    ("STY-03", "WARN", "[--style] Counted preface ('there are three main limitations')"),
    ("STY-04", "WARN", "[--style] Self-ranking of own results ('our most important finding')"),
    ("STY-05", "WARN", "[--style] Short single-paragraph subsection"),
    ("STY-06", "WARN", "[--style] Acronym defined multiple times in body prose"),
    ("STY-07", "WARN", "[--style] Repeated acronym used without definition"),
    ("STY-08", "WARN", "[--style] Causal verb in observational study Results/Discussion"),
]

RULE_ID_RE = re.compile(r"^[A-Z]{2,3}-\d{2}$")
NON_SUPPRESSIBLE_IO_PREFIX = "IO-"
FATAL_GATE_RULES = {"REV-00", "REV-01", "REV-02", "REV-04", "REV-06"}

ENGLISH_CAPS_IGNORE = {
    "DRAFT", "OWNER", "PLAN", "VALID", "NOTE", "NOTES", "TABLE", "FIGURE", "PART", "NONE",
    "TEXT", "DATA", "CODE", "TEST", "HIGH", "LOW", "FULL", "OPEN", "MAIN", "MEAN", "NULL",
    "TRUE", "FALSE", "INJECT", "TODO", "FIXME", "TBD", "PENDING", "AUTHOR", "PASS", "FAIL",
    "WARN", "MAJOR", "MINOR", "FATAL", "INFO", "CHECK", "STAGE", "STUDY", "GROUP", "TOTAL",
}

# Opt-in --style patterns
STRUCTURAL_TELL_PATTERNS = [
    ("STY-01", re.compile(r"\b(?:should|must)\s+be\s+interpreted\s+with\s+caution\b", re.I), "reading instruction ('interpreted with caution')"),
    ("STY-02", re.compile(r"\breaders\s+should\s+(?:note|bear\s+in\s+mind|interpret)\b", re.I), "reading instruction"),
    ("STY-03", re.compile(r"\bthere\s+are\s+(?:two|three|four|five|six|\d+)\s+(?:key|main|major|primary|notable|important)\s+(?:limitations|advantages|contributions|findings|reasons|factors)\b", re.I), "counted preface"),
    ("STY-04", re.compile(r"\bour\s+most\s+(?:important|informative|compelling|striking|consequential)\s+(?:finding|result)\b", re.I), "self-ranking of own results"),
]

CAUSAL_VERB_RE = re.compile(
    r"(?<!with\s)(?<!of\s)(?<!associated\swith\s)\b(?:causes|caused|causing|prevents|prevented|preventing|"
    r"improves|reduces|drives|drove|led\s+to|resulted\s+in|yielded)\b"
    r"|\b(?:improved|reduced)\s+(?:\d|pain|function|mortality|survival|risk|rates?|scores?|disability|opioid|outcomes?|symptoms?)\b",
    re.I,
)

COMMON_ACRONYMS = {
    "DNA", "RNA", "MRI", "PET", "ECG", "EEG", "EMG", "MEG", "HRV", "ICU", "IQR", "ROC", "AUC",
    "AUROC", "AUPRC", "SEM", "BMI", "VAS", "NRS", "PDF", "SVG", "PNG", "EPS", "CSV", "JSON",
    "API", "URL", "DOI", "CPU", "GPU", "TPU", "ARM", "LLM", "NLP", "RCT", "EHR", "IRB", "VIF",
    "USA", "FDA", "NIH", "WHO", "CDC", "ECE", "MIT", "SQL", "HTML", "XML", "HTTP", "HTTPS",
    "IEEE", "ACM", "STROBE", "CONSORT", "PRISMA", "TRIPOD", "ARRIVE", "IMRAD", "PROMIS",
    "ANOVA", "ANCOVA", "MANOVA", "RMSE", "MAE", "MAPE", "SHAP", "LASSO", "PCA", "UMAP", "TSNE",
    "CNN", "RNN", "LSTM", "BERT", "GPT", "LOS", "NYHA", "ICD", "CPT", "HIPAA", "GDPR", "OSF",
    "PROSPERO", "DAG", "IPTW", "PSM", "AMA", "ICMJE", "OOD", "SMD", "MCID", "FFN",
}

# Exact regex matching academic-humanizer/scripts/preservation_check.py DECLARATION_HEAD
HUMANIZER_DECLARATION_HEAD = re.compile(
    r"(?im)^(?:#{1,6}\s*|\\(?:section|subsection|paragraph)\*?\{)\s*"
    r"((?:declaration of )?(?:ai|generative ai|artificial intelligence)[^\n}]*|data availability[^\n}]*|"
    r"code availability[^\n}]*|conflicts? of interest[^\n}]*|competing interests?[^\n}]*|"
    r"funding[^\n}]*|author contributions[^\n}]*|credit[^\n}]*|ethics[^\n}]*|"
    r"acknowledg(?:e)?ments?[^\n}]*)\}?\s*$"
)

# Exact lock-safe prefixes matching academic-humanizer/scripts/preservation_check.py DECLARATION_HEAD
LOCK_SAFE_DECLARATIONS = {
    "Ethics": re.compile(r"^ethics\b", re.I),
    "Data Availability": re.compile(r"^data availability\b", re.I),
    "Funding": re.compile(r"^funding\b", re.I),
    "Conflicts of Interest": re.compile(r"^(?:conflicts? of interest|competing interests?)\b", re.I),
    "AI-Use Disclosure": re.compile(r"^(?:declaration of )?(?:ai|generative ai|artificial intelligence)\b", re.I),
}

# Common non-lock-safe declaration spellings that academic-humanizer will NOT FAIL-lock
NON_LOCK_SAFE_DECLARATIONS = re.compile(
    r"^(?:data and code availability|data sharing|irb\b|institutional review board|ethical approval|financial support|grant support)\b",
    re.I,
)

CANONICAL_BODY_SECTIONS = (
    "introduction", "methods", "materials", "results", "discussion", "conclusion",
    "declarations", "references", "bibliography", "acknowledg", "key points", "highlights",
    "tables", "figures", "figure legends",
)

STRUCTURED_ABS_SUBHEADS = (
    "importance", "background", "objective", "purpose", "design", "setting", "participants",
    "patients", "exposure", "intervention", "main outcomes", "measures", "methods",
    "results", "findings", "conclusions", "relevance", "meaning", "trial registration",
)

SKIP_BUDGET_PREFIXES = (
    "references", "bibliography", "acknowledg", "declarations", "funding", "ethics",
    "conflicts", "competing", "data availability", "code availability", "data sharing",
    "ai-use", "declaration of", "key points", "highlights", "figure legends", "figures", "tables",
)

REF_VALUE_KEYS = {"text", "doi", "src", "title", "author", "year", "zoteroKey", "itemKey", "key", "number", "citation"}
CROSSREF_PREFIXES = ("fig:", "tbl:", "eq:", "sec:", "lst:", "alg:")
CLAIM_STATUSES = {"verified", "unverified", "gap"}
RESOLVED_STATUSES = {"resolved", "narrowed", "accepted-risk"}
VALID_STATUSES = {"open", "pending-author-data", "resolved", "narrowed", "accepted-risk"}
SUPP_PREFIX_RE = re.compile(r"(?:Supplementary|Supplemental|Extended\s+Data|Appendix|Online)\s+$", re.I)


def normalize_heading(title: str) -> str:
    """Strip Markdown emphasis wrappers and leading section numbering ('1. ', '6.7 ', 'II. ', '(1) ', 'Part 1. ', '§2 ')
    without touching '3D ...' or 4-digit years like '2020 Cohort'."""
    t = title.strip()
    t = re.sub(r"^(?:\*\*|__|\*|_)(.+?)(?:\*\*|__|\*|_)$", r"\1", t).strip()
    t = re.sub(
        r"^(?:Part\s+(?:\d+|[IVXLCDM]+)[A-Za-z]?[.:\-—)\]]*\s+"
        r"|Section\s+\d+(?:\.\d+)*[.:\-—)\]]*\s+"
        r"|§\s*\d+(?:\.\d+)*[.:\-—)\]]*\s+"
        r"|\(\d{1,2}\)\s*"
        r"|[IVXLCDM]{1,4}[.)]\s+"
        r"|\d{1,2}(?:\.\d+)+[A-Za-z]?[.:\-—)\]]*\s*"
        r"|\d{1,2}[A-Za-z]?[.:)\-—]\s*)",
        "",
        t,
    )
    return t.strip()


@dataclass
class Finding:
    rule: str
    where: str
    msg: str


@dataclass
class Report:
    fails: list[Finding] = field(default_factory=list)
    warns: list[Finding] = field(default_factory=list)
    accepted: list[Finding] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    accept_rules: set[str] = field(default_factory=set)
    accept_substrings: list[str] = field(default_factory=list)
    accept_fatal: bool = False

    def is_rule_accepted(self, rule: str) -> bool:
        r = rule.upper()
        if r.startswith(NON_SUPPRESSIBLE_IO_PREFIX):
            return False
        if r in FATAL_GATE_RULES and not self.accept_fatal:
            return False
        return r in self.accept_rules

    def _is_accepted(self, rule: str, where: str, msg: str) -> bool:
        r = rule.upper()
        if r.startswith(NON_SUPPRESSIBLE_IO_PREFIX):
            return False
        if r in FATAL_GATE_RULES and not self.accept_fatal:
            return False
        if r in self.accept_rules:
            return True
        hay = f"{where} {msg}".lower()
        return any(sub.lower() in hay for sub in self.accept_substrings)

    def fail(self, rule: str, where: str, msg: str) -> None:
        f = Finding(rule, where, msg)
        if self._is_accepted(rule, where, msg):
            self.accepted.append(f)
        else:
            self.fails.append(f)

    def warn(self, rule: str, where: str, msg: str) -> None:
        f = Finding(rule, where, msg)
        if self._is_accepted(rule, where, msg):
            self.accepted.append(f)
        else:
            self.warns.append(f)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


# ---------------------------------------------------------------- file loading

def _extract_docx_paragraph_text(p_elem: ET.Element) -> str:
    """Extract paragraph text preserving spaces across <w:br/>, <w:cr/>, and <w:tab/>, skipping deletions."""
    parts: list[str] = []

    def _walk(node: ET.Element) -> None:
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in {"del", "delText", "instrText"}:
            return
        if tag == "t" and node.text:
            parts.append(node.text)
        elif tag in {"br", "cr", "tab"}:
            parts.append(" ")
        for ch in node:
            _walk(ch)

    _walk(p_elem)
    return re.sub(r"[ \t]+", " ", "".join(parts)).strip()


def _extract_docx_nodes(container: ET.Element, ns: dict[str, str], out_blocks: list[tuple[str, str]]) -> None:
    for child in container:
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            para = _extract_docx_paragraph_text(child)
            if not para:
                continue
            pstyle = child.find("./w:pPr/w:pStyle", ns)
            style_val = pstyle.attrib.get(f"{{{ns['w']}}}val", "") if pstyle is not None else ""
            out_blocks.append((style_val, para))
        elif tag == "tbl":
            for tr in child.findall("./w:tr", ns):
                cells = [
                    " ".join(_extract_docx_paragraph_text(p) for p in tc.findall("./w:p", ns)).strip()
                    for tc in tr.findall("./w:tc", ns)
                ]
                if any(cells):
                    out_blocks.append(("TableRow", "| " + " | ".join(cells) + " |"))
        elif tag == "sdt":
            sdt_content = child.find("./w:sdtContent", ns)
            if sdt_content is not None:
                _extract_docx_nodes(sdt_content, ns, out_blocks)


def load_docx_structured(path: Path) -> tuple[list[tuple[str, str]], list[str], list[str], str]:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    try:
        zf = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError) as exc:
        raise ValueError(f"invalid or unreadable .docx archive: {exc}") from exc

    with zf:
        if "word/document.xml" not in zf.namelist():
            raise ValueError("missing word/document.xml inside .docx archive")
        try:
            root = ET.fromstring(zf.read("word/document.xml"))
        except ET.ParseError as exc:
            raise ValueError(f"malformed word/document.xml: {exc}") from exc

        body = root.find("w:body", ns)
        blocks: list[tuple[str, str]] = []
        if body is not None:
            _extract_docx_nodes(body, ns, blocks)

        footnotes: list[str] = []
        for part in ("word/footnotes.xml", "word/endnotes.xml"):
            if part in zf.namelist():
                try:
                    proot = ET.fromstring(zf.read(part))
                    for p in proot.findall(".//w:p", ns):
                        t = _extract_docx_paragraph_text(p)
                        if t:
                            footnotes.append(t)
                except ET.ParseError:
                    pass

        comments: list[str] = []
        if "word/comments.xml" in zf.namelist():
            try:
                croot = ET.fromstring(zf.read("word/comments.xml"))
                for p in croot.findall(".//w:p", ns):
                    t = _extract_docx_paragraph_text(p)
                    if t:
                        comments.append(t)
            except ET.ParseError:
                pass

    heading_levels = [
        min(int(m.group(1)), 4)
        for style, _ in blocks
        if (m := re.match(r"Heading(\d)", style, re.I))
    ]
    abs_hashes = "#" * (min(heading_levels) if heading_levels else 1)

    md_lines: list[str] = []
    in_abs = False
    for style, text in blocks:
        m = re.match(r"Heading(\d)", style, re.I)
        if m:
            in_abs = False
            md_lines.append(f"{'#' * min(int(m.group(1)), 4)} {text}")
        elif re.match(r"Abstract", style, re.I):
            if not in_abs:
                md_lines.append(f"{abs_hashes} Abstract")
                in_abs = True
            md_lines.append(text)
        else:
            in_abs = False
            md_lines.append(text)
    return blocks, footnotes, comments, "\n".join(md_lines) + "\n"


def expand_tex_inputs(path: Path, seen: set[Path] | None = None, depth: int = 0) -> str:
    if seen is None:
        seen = set()
    resolved = path.resolve()
    if resolved in seen or depth > 5:
        return ""
    seen.add(resolved)
    text = path.read_text(encoding="utf-8", errors="replace")

    def _repl(m: re.Match) -> str:
        rel = m.group(2).strip()
        cand = path.parent / rel
        if not cand.exists() and not rel.endswith(".tex"):
            cand = path.parent / f"{rel}.tex"
        if cand.exists() and cand.is_file():
            return expand_tex_inputs(cand, seen, depth + 1)
        return m.group(0)

    return re.sub(r"(?<!\\)\\(input|include)\{([^}]+)\}", _repl, text)


def detect_format(path: Path, forced: str) -> str:
    if forced != "auto":
        return forced
    return {".tex": "tex", ".docx": "docx"}.get(path.suffix.lower(), "md")


def extract_yaml_frontmatter(lines: list[str]) -> tuple[str, str, int]:
    if not lines or lines[0].strip() != "---":
        return "", "", 0
    end_idx = next((i for i in range(1, len(lines)) if lines[i].strip() in {"---", "..."}), None)
    if end_idx is None:
        return "", "", 0
    title, abs_lines, in_abs, abs_indent = "", [], False, 0
    for fl in lines[1:end_idx]:
        if not in_abs:
            if tm := re.match(r"^title\s*:\s*(.+)$", fl, re.I):
                title = tm.group(1).strip().strip("\"'")
            if am := re.match(r"^abstract\s*:\s*(.*)$", fl, re.I):
                val = am.group(1).strip()
                if val in {"|", ">", "|-", ">-", ""}:
                    in_abs, abs_indent = True, 0
                else:
                    abs_lines.append(val.strip("\"'"))
        else:
            if not fl.strip():
                abs_lines.append("")
                continue
            indent = len(fl) - len(fl.lstrip(" "))
            if indent == 0:
                in_abs = False
            else:
                abs_indent = abs_indent or indent
                abs_lines.append(fl[min(indent, abs_indent):])
    return title, "\n".join(abs_lines).strip(), end_idx + 1


def strip_md_nonprose(lines: list[str], start_idx: int = 0) -> tuple[list[tuple[int, str]], list[tuple[int, str, int]]]:
    """Strip fenced code blocks and HTML comments, returning (numbered_lines, unclosed_issues).
    Each unclosed issue is (start_lineno, kind, skipped_line_count)."""
    out: list[tuple[int, str]] = []
    unclosed: list[tuple[int, str, int]] = []
    fence: str | None = None
    fence_start = 0
    in_comment = False
    comment_start = 0
    for i in range(start_idx, len(lines)):
        ln, line = i + 1, lines[i]
        s = line.lstrip()
        if fence is None:
            if s.startswith(("```", "~~~")):
                fence, fence_start = s[:3], ln
                continue
        else:
            if s.startswith(fence):
                fence = None
            continue
        if in_comment:
            if "-->" in line:
                line = line.split("-->", 1)[1]
                in_comment = False
            else:
                continue
        line = re.sub(r"<!--.*?-->", "", line)
        if "<!--" in line:
            line = line.split("<!--", 1)[0]
            in_comment, comment_start = True, ln
        out.append((ln, line))
    if fence is not None:
        unclosed.append((fence_start, f"unclosed code fence '{fence}'", len(lines) - fence_start))
    if in_comment:
        unclosed.append((comment_start, "unclosed HTML comment '<!--'", len(lines) - comment_start))
    return out, unclosed


def parse_all_tables(lines: list[tuple[int, str]]) -> list[list[tuple[int, dict[str, str]]]]:
    """Parse every Markdown pipe table in lines (ignoring fenced code blocks)."""
    tables: list[list[tuple[int, dict[str, str]]]] = []
    headers: list[str] | None = None
    cur_rows: list[tuple[int, dict[str, str]]] = []
    fence: str | None = None

    def _flush() -> None:
        nonlocal headers, cur_rows
        if headers and cur_rows:
            tables.append(cur_rows)
        headers, cur_rows = None, []

    for lineno, line in lines:
        s = line.strip()
        if fence is None and s.startswith(("```", "~~~")):
            _flush()
            fence = s[:3]
            continue
        if fence is not None:
            if s.startswith(fence):
                fence = None
            continue
        if "|" not in s or not (s.startswith("|") or re.search(r"\S\s*\|\s*\S", s)):
            _flush()
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2:
            _flush()
            continue
        if headers is None:
            headers = [re.sub(r"[*_`]", "", h).strip().lower() for h in cells]
        elif all(set(c) <= set("-: ") for c in cells):
            continue
        else:
            cur_rows.append((lineno, dict(zip(headers, cells))))
    _flush()
    return tables


def mask_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def strip_tex_comments(lines: list[str]) -> list[tuple[int, str]]:
    return [(i, re.sub(r"(?<!\\)%.*$", "", line)) for i, line in enumerate(lines, 1)]


# ---------------------------------------------------------------- artifact helpers

def parse_md_h2_sections(lines: list[str]) -> dict[str, list[tuple[int, str]]]:
    out: dict[str, list[tuple[int, str]]] = {}
    current, fence = None, None
    for i, line in enumerate(lines, 1):
        s = line.lstrip()
        if fence is None and s.startswith(("```", "~~~")):
            fence = s[:3]
        elif fence is not None and s.startswith(fence):
            fence = None
        if fence is None and line.startswith("## "):
            current = line[3:].strip()
            out[current] = []
        elif current is not None:
            out[current].append((i, line))
    return out


def find_section(secs: dict[str, list[tuple[int, str]]], prefix: str) -> list[tuple[int, str]] | None:
    low = prefix.lower()
    for k, v in secs.items():
        if normalize_heading(k).lower().startswith(low):
            return v
    return None


def parse_first_table(body: list[tuple[int, str]] | None) -> list[tuple[int, dict[str, str]]]:
    rows, headers = [], None
    for lineno, line in body or []:
        s = line.strip()
        if not s.startswith("|"):
            if headers and rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if headers is None:
            headers = [h.lower() for h in cells]
        elif all(set(c) <= set("-: ") for c in cells):
            continue
        else:
            rows.append((lineno, dict(zip(headers, cells))))
    return rows


def col(row: dict[str, str], *prefixes: str) -> str:
    for p in prefixes:
        for k, v in row.items():
            if k.startswith(p):
                return v
    return ""


# ---------------------------------------------------------------- manuscript parsing

def parse_manuscript_sections(
    numbered: list[tuple[int, str]],
    fmt: str,
    yaml_title: str = "",
    yaml_abstract: str = "",
) -> tuple[str, str, str, int, list[tuple[str, int, list[tuple[int, str]]]]]:
    """Return (title_text, keypoints_text, abstract_text, top_level, body_sections)."""
    if fmt == "tex":
        full = "\n".join(line for _, line in numbered)
        tm = re.search(r"\\title\{([^}]*)\}", full)
        title_text = tm.group(1).strip() if tm else ""
        abs_m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", full, re.S)
        abstract_text = abs_m.group(1).strip() if abs_m else ""
        no_abs = re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}", lambda m: "\n" * m.group(0).count("\n"), full, flags=re.S)
        secs: list[tuple[str, int, list[tuple[int, str]]]] = []
        cur_title, cur_level, cur_lines = "Preamble", 0, []
        sec_re = re.compile(r"\\(section|subsection|subsubsection)\*?\{([^}]*)\}")
        for ln, line in enumerate(no_abs.splitlines(), 1):
            pos, found = 0, False
            for m in sec_re.finditer(line):
                found = True
                if before := line[pos:m.start()].strip():
                    cur_lines.append((ln, before))
                if cur_lines or cur_title != "Preamble":
                    secs.append((cur_title, cur_level, cur_lines))
                cur_level = {"section": 1, "subsection": 2, "subsubsection": 3}[m.group(1)]
                cur_title, cur_lines, pos = m.group(2).strip(), [], m.end()
            if found:
                if after := line[pos:].strip():
                    cur_lines.append((ln, after))
            else:
                cur_lines.append((ln, line))
        if cur_lines or cur_title != "Preamble":
            secs.append((cur_title, cur_level, cur_lines))

        body_secs, kp_parts = [], []
        for title, level, body in secs:
            norm = normalize_heading(title).lower()
            if level == 1 and norm.startswith(("abstract", "summary")):
                if not abstract_text:
                    abstract_text = "\n".join(l for _, l in body).strip()
                continue
            if level == 1 and norm.startswith(("key points", "highlights")):
                kp_parts.append("\n".join(l for _, l in body))
            body_secs.append((title, level, body))
        return title_text, "\n".join(kp_parts).strip(), abstract_text, 1, body_secs

    # Markdown / DOCX: first pass collects headings (H1-H5 + Setext); bold **Abstract** gets level matched after top_level detection
    raw_secs: list[tuple[str, int, bool, list[tuple[int, str]]]] = []
    cur_title, cur_level, is_bold_abs, cur_lines = "Front", 0, False, []
    head_re = re.compile(r"^(#{1,5})\s+(.*)$")
    bold_abs_re = re.compile(r"^\*\*(Abstract|Summary)\*\*\s*[:.]?\s*$", re.I)

    idx = 0
    while idx < len(numbered):
        ln, line = numbered[idx]
        s = line.strip()
        if m := head_re.match(s):
            if cur_lines or cur_title != "Front":
                raw_secs.append((cur_title, cur_level, is_bold_abs, cur_lines))
            cur_level, cur_title, is_bold_abs, cur_lines = len(m.group(1)), m.group(2).strip(), False, []
            idx += 1
        elif (
            s
            and not s.startswith(("|", "-", "*", ">"))
            and idx + 1 < len(numbered)
            and re.match(r"^(={3,}|-{3,})$", numbered[idx + 1][1].strip())
        ):
            if cur_lines or cur_title != "Front":
                raw_secs.append((cur_title, cur_level, is_bold_abs, cur_lines))
            setext_lvl = 1 if numbered[idx + 1][1].strip().startswith("=") else 2
            cur_level, cur_title, is_bold_abs, cur_lines = setext_lvl, s, False, []
            idx += 2
        elif bm := bold_abs_re.match(s):
            if cur_lines or cur_title != "Front":
                raw_secs.append((cur_title, cur_level, is_bold_abs, cur_lines))
            cur_level, cur_title, is_bold_abs, cur_lines = 0, bm.group(1), True, []
            idx += 1
        else:
            cur_lines.append((ln, line))
            idx += 1
    if cur_lines or cur_title != "Front":
        raw_secs.append((cur_title, cur_level, is_bold_abs, cur_lines))

    # Derive top_level from normalized canonical BODY sections (so numbered '## 1. Introduction' works!)
    body_canon_levels = [
        lvl for title, lvl, _, _ in raw_secs
        if lvl > 0 and normalize_heading(title).lower().startswith(CANONICAL_BODY_SECTIONS)
    ]
    if body_canon_levels:
        top_level = min(body_canon_levels)
    else:
        non_zero = [lvl for _, lvl, _, _ in raw_secs if lvl > 0]
        if non_zero:
            top_level = 2 if (non_zero.count(1) == 1 and non_zero.count(2) >= 1) else min(non_zero)
        else:
            top_level = 1

    # Resolve bold **Abstract** level to top_level (works for BOTH H1 and H2 body manuscripts!)
    secs = [(t, top_level if ba else lvl, body) for t, lvl, ba, body in raw_secs]

    title_text = yaml_title
    if not title_text:
        for title, lvl, _ in secs:
            norm = normalize_heading(title).lower()
            if lvl == 1 and lvl < top_level and not norm.startswith(("abstract", "summary", "key points")):
                title_text = title
                break

    abs_parts = [yaml_abstract] if yaml_abstract else []
    abs_captured = bool(yaml_abstract)
    kp_parts: list[str] = []
    body_secs: list[tuple[str, int, list[tuple[int, str]]]] = []
    in_abs, abs_level = False, top_level

    for title, level, body in secs:
        norm = normalize_heading(title).lower()
        is_abs_head = norm.startswith("abstract") or (norm == "summary" and not abs_captured)
        if not in_abs and not abs_captured and level > 0 and is_abs_head and level <= top_level:
            in_abs, abs_level, abs_captured = True, level, True
            abs_parts.append("\n".join(l for _, l in body))
            continue
        if in_abs:
            if level > abs_level and level > top_level and norm.startswith(STRUCTURED_ABS_SUBHEADS):
                abs_parts.append(title + "\n" + "\n".join(l for _, l in body))
                continue
            in_abs = False
        if level == top_level and norm.startswith(("key points", "highlights")):
            kp_parts.append("\n".join(l for _, l in body))
        body_secs.append((title, level, body))

    return title_text, "\n".join(kp_parts).strip(), "\n".join(p for p in abs_parts if p.strip()).strip(), top_level, body_secs


def clean_prose_words(text: str, fmt: str, skip_tables: bool = True) -> list[str]:
    if fmt == "tex":
        text = re.sub(
            r"\\begin\{(?:equation|align|table|sidewaystable|tabular|figure|wrapfigure)\*?\}[\s\S]*?"
            r"\\end\{(?:equation|align|table|sidewaystable|tabular|figure|wrapfigure)\*?\}",
            " ",
            text,
        )
        text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?", " ", text)
        text = re.sub(r"\$[^$]*\$", " ", text)
    else:
        if skip_tables:
            text = "\n".join(l for l in text.splitlines() if not (l.strip().startswith("|") and l.strip().endswith("|")))
        text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
        text = re.sub(r"`[^`]+`", " ", text)
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text)


def loc(label: str, ln: int, fmt: str) -> str:
    return f"{label}:para {ln}" if fmt == "docx" else f"{label}:{ln}"


# ---------------------------------------------------------------- bibliography & citations

def inspect_zotero_config(path: Path) -> tuple[Path | None, str | None, str | None]:
    """Read a sync-refs zotero.json config. Return (resolved_refs_path, keys_filename, error_msg)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return None, None, f"could not parse {path.name}: {exc}"
    if not isinstance(data, dict):
        return None, None, None
    refs = data.get("refs")
    keys = data.get("keys") if isinstance(data.get("keys"), str) else None
    if isinstance(refs, str):
        target = (path.parent / refs).resolve()
        if not target.exists():
            return None, keys, f"zotero.json 'refs' target '{refs}' does not exist"
        return target, keys, None
    if any(k in data for k in ("about", "paper", "library", "style", "map")):
        return None, keys, f"{path.name} is a zotero config file without a 'refs' string; pass --bib <refs.json|.bib>"
    return None, None, None


def load_bib_keys(path: Path, report: Report) -> tuple[set[str], str]:
    actual_path = path
    if path.suffix.lower() == ".json":
        refs_target, _, err = inspect_zotero_config(path)
        if err:
            raise ValueError(err)
        if refs_target is not None:
            actual_path = refs_target

    if not actual_path.exists():
        raise FileNotFoundError(f"bibliography '{actual_path}' does not exist")

    raw = actual_path.read_text(encoding="utf-8", errors="replace")
    if actual_path.suffix.lower() == ".json":
        data = json.loads(raw)
        if isinstance(data, dict):
            if isinstance(data.get("items"), list):
                items = data["items"]
            elif isinstance(data.get("entries"), dict):
                return {str(k).strip() for k in data["entries"] if str(k).strip()}, actual_path.name
            elif isinstance(data.get("map"), dict):
                return {str(k).strip() for k in data["map"] if str(k).strip()}, actual_path.name
            else:
                dict_vals = [v for v in data.values() if isinstance(v, dict)]
                ref_like = [v for v in dict_vals if any(k in v for k in REF_VALUE_KEYS)]
                if not dict_vals or not ref_like:
                    raise ValueError(f"'{actual_path.name}' is not a checked-refs map ({{key: {{text, doi, src}}}})")
                return {str(k).strip() for k, v in data.items() if isinstance(v, dict) and str(k).strip()}, actual_path.name
        elif isinstance(data, list):
            items = data
        else:
            return set(), actual_path.name

        keys, uri_only = set(), 0
        for item in items:
            if not isinstance(item, dict):
                continue
            if ck := item.get("citation-key"):
                keys.add(str(ck).strip())
            elif iid := item.get("id"):
                s = str(iid).strip()
                keys.add(s)
                uri_only += int(s.startswith(("http://", "https://")))
        if uri_only and uri_only == len(keys):
            report.warn("CIT-03", actual_path.name, "CSL-JSON has URI 'id's without 'citation-key'; use checked refs JSON or Better BibTeX")
        return keys, actual_path.name

    return {m.group(1).strip() for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,", raw)}, actual_path.name


def extract_md_citekeys(line: str) -> list[str]:
    """Extract bracketed citation keys ([@key; -@key2, p. 3]), skipping crossrefs and emails.
    Character class matches sync-refs/number-refs.py keys."""
    keys: list[str] = []
    cleaned = re.sub(r"\[[^\]]*\]\([^)]*\)", "", mask_inline_code(line))
    for bm in re.finditer(r"\[([^\]]*@[^\]]+)\]", cleaned):
        inner = bm.group(1)
        for km in re.finditer(r"(?:^|[\s;,\-])@([A-Za-z0-9_][A-Za-z0-9_:.#$%&\-+~]*)", inner):
            key = km.group(1).rstrip(".,;:")
            if key.lower().startswith(CROSSREF_PREFIXES):
                continue
            keys.append(key)
    return keys


def check_citations_against_bib(
    numbered: list[tuple[int, str]],
    fmt: str,
    bib_path: Path,
    label: str,
    report: Report,
) -> None:
    if not bib_path.exists():
        report.fail("CIT-01", str(bib_path), "bibliography file does not exist")
        return
    try:
        valid_keys, resolved_name = load_bib_keys(bib_path, report)
    except Exception as exc:
        report.fail("CIT-01", bib_path.name, f"could not parse bibliography: {exc}")
        return

    used_keys: list[tuple[int, str]] = []
    if fmt == "tex":
        pat = re.compile(r"\\([a-zA-Z]*cites?[a-zA-Z]*)\*?((?:\s*(?:\[[^\]]*\])*\s*\{[^}]+\})+)")
        for ln, line in numbered:
            for m in pat.finditer(line):
                cmd = m.group(1).lower()
                for grp in re.findall(r"\{([^}]+)\}", m.group(2)):
                    for k in grp.split(","):
                        ks = k.strip()
                        if ks and not (cmd == "nocite" and ks == "*"):
                            used_keys.append((ln, ks))
    else:
        for ln, line in numbered:
            for key in extract_md_citekeys(line):
                used_keys.append((ln, key))

    seen_missing: set[str] = set()
    for ln, key in used_keys:
        if key not in valid_keys and key not in seen_missing:
            seen_missing.add(key)
            report.fail("CIT-02", loc(label, ln, fmt), f"citation key '@{key}' not found in {resolved_name}")
    report.note(
        f"Checked bracketed citations against {resolved_name}: {len(used_keys)} occurrence(s), {len(valid_keys)} library key(s)"
    )
    if not used_keys and valid_keys:
        report.warn("CIT-05", label, f"bibliography '{resolved_name}' loaded ({len(valid_keys)} keys) but 0 bracketed citekeys found (check if numbered [1] or bare @key citations are used)")


# ---------------------------------------------------------------- checks: placeholders

def check_placeholders(
    numbered: list[tuple[int, str]],
    fmt: str,
    label: str,
    report: Report,
    stage: str = "submission",
    comments_only: bool = False,
) -> None:
    working_hits: list[tuple[str, int, str, str]] = []
    for ln, line in numbered:
        scan = mask_inline_code(line) if fmt != "tex" else line
        for rule, pat, desc in BROKEN_TOKEN_PATTERNS:
            for m in pat.finditer(scan):
                (report.warn if comments_only else report.fail)(rule, loc(label, ln, fmt), f"{desc}: '{m.group(0)}'")
        matched_spans: list[tuple[int, int]] = []
        for rule, pat, desc in WORKING_MARKER_PATTERNS:
            for m in pat.finditer(scan):
                matched_spans.append(m.span())
                working_hits.append((rule, ln, desc, m.group(0)))
        for rule, pat, desc in SOFT_PLACEHOLDER_PATTERNS:
            for m in pat.finditer(scan):
                if rule == "PH-16":
                    # Avoid double-reporting tokens already caught as working markers or citations/checkboxes
                    if any(a <= m.start() < b for a, b in matched_spans):
                        continue
                    tok_inner = m.group(0)[1:-1].split(":")[0].strip()
                    if tok_inner in COMMON_ACRONYMS:
                        continue
                report.warn(rule, loc(label, ln, fmt), f"{desc}: '{m.group(0)}'")
        if fmt == "docx":
            if leftover := extract_md_citekeys(scan):
                (report.warn if comments_only else report.fail)(
                    "CIT-04", loc(label, ln, fmt),
                    f"unconverted literal citation key(s) in .docx: {', '.join('@' + k for k in leftover)}",
                )

    if not working_hits:
        return

    # Apply per-rule acceptance BEFORE grouping into PH-00 so '--accept PH-03' works at any count
    remaining: list[tuple[str, int, str, str]] = []
    for rule, ln, desc, tok in working_hits:
        where = loc(label, ln, fmt)
        msg = f"{desc}: '{tok}'"
        if report._is_accepted(rule, where, msg):
            report.accepted.append(Finding(rule, where, msg))
        else:
            remaining.append((rule, ln, desc, tok))
    if not remaining:
        return

    if comments_only or stage == "draft":
        sample = ", ".join(f"L{ln}:'{tok[:28]}'" for _, ln, _, tok in remaining[:4])
        report.warn(
            "PH-00", label,
            f"{len(remaining)} working marker(s) present (stage={stage}; resolve before submission): {sample}"
            + (" ..." if len(remaining) > 4 else ""),
        )
    elif len(remaining) > 10:
        sample = ", ".join(f"L{ln}:'{tok[:28]}'" for _, ln, _, tok in remaining[:5])
        report.fail(
            "PH-00", label,
            f"{len(remaining)} unresolved working marker(s) at submission stage (use --stage draft while drafting): {sample} ...",
        )
    else:
        for rule, ln, desc, tok in remaining:
            report.fail(rule, loc(label, ln, fmt), f"{desc}: '{tok}'")


# ---------------------------------------------------------------- checks: figures & tables

def _check_order(first_order: list[tuple[int, int, str]], kind: str, fmt: str, label: str, report: Report) -> None:
    max_seen = 0
    for num, ln, ref_txt in first_order:
        if num < max_seen:
            report.warn("REF-04", loc(label, ln, fmt), f"{kind} {num} ({ref_txt}) first cited after {kind} {max_seen} (out-of-order numbering)")
        else:
            max_seen = num


def check_figures_and_tables_tex(
    numbered: list[tuple[int, str]],
    label: str,
    report: Report,
    extra_fig_nums: set[int],
    extra_tab_nums: set[int],
) -> None:
    full = "\n".join(line for _, line in numbered)
    fig_labels, tab_labels = {}, {}
    fig_idx, tab_idx = 0, 0
    env_pat = re.compile(r"\\begin\{(figure|wrapfigure|table|sidewaystable)\*?\}(.*?)\\end\{\1\*?\}", re.S)
    for env_m in env_pat.finditer(full):
        if env_m.group(1) in {"figure", "wrapfigure"}:
            fig_idx += 1
            for lm in re.finditer(r"\\label\{([^}]+)\}", env_m.group(2)):
                fig_labels[lm.group(1).strip()] = fig_idx
        else:
            tab_idx += 1
            for lm in re.finditer(r"\\label\{([^}]+)\}", env_m.group(2)):
                tab_labels[lm.group(1).strip()] = tab_idx

    all_labels = set(re.findall(r"\\label\{([^}]+)\}", full))
    body_only = env_pat.sub(lambda m: "\n" * m.group(0).count("\n"), full)
    fig_first, tab_first, cited_figs, cited_tabs = [], [], set(), set()

    for ln, line in enumerate(body_only.splitlines(), 1):
        for rm in re.finditer(r"\\(?:ref|cref|Cref|autoref|eqref)\{([^}]+)\}", line):
            for key in (k.strip() for k in rm.group(1).split(",")):
                if not key:
                    continue
                if key not in all_labels:
                    report.fail("REF-01", f"{label}:{ln}", f"dangling LaTeX reference '\\ref{{{key}}}'")
                elif key in fig_labels:
                    num = fig_labels[key]
                    cited_figs.add(num)
                    if all(x[0] != num for x in fig_first):
                        fig_first.append((num, ln, key))
                elif key in tab_labels:
                    num = tab_labels[key]
                    cited_tabs.add(num)
                    if all(x[0] != num for x in tab_first):
                        tab_first.append((num, ln, key))

    for num in sorted(set(fig_labels.values()) - cited_figs):
        report.fail("REF-02", label, f"orphaned Figure {num} is never referenced in body text")
    for num in sorted(set(tab_labels.values()) - cited_tabs):
        report.fail("REF-02", label, f"orphaned Table {num} is never referenced in body text")

    _check_order(fig_first, "Figure", "tex", label, report)
    _check_order(tab_first, "Table", "tex", label, report)
    if extra_fig_nums and fig_idx and extra_fig_nums != set(range(1, fig_idx + 1)):
        report.warn("REF-05", label, f"figure parity mismatch: manuscript has {fig_idx}, figure-plan lists {sorted(extra_fig_nums)}")
    if extra_tab_nums and tab_idx and extra_tab_nums != set(range(1, tab_idx + 1)):
        report.warn("REF-05", label, f"table parity mismatch: manuscript has {tab_idx}, figure-plan lists {sorted(extra_tab_nums)}")


def _expand_segment_list(expr: str) -> list[int]:
    nums: list[int] = []
    for seg in re.split(r"\s*(?:,\s*(?:and|&)\s*|,|\band\b|&)\s*", expr.strip(), flags=re.I):
        seg = seg.strip()
        if not seg:
            continue
        if rm := re.match(r"^(\d+)[a-z]?\s*[-\u2013\u2014]\s*(\d+)[a-z]?$", seg, re.I):
            a, b = int(rm.group(1)), int(rm.group(2))
            if a <= b <= a + 20:
                nums.extend(range(a, b + 1))
        elif sm := re.match(r"^(\d+)[a-z]?$", seg, re.I):
            nums.append(int(sm.group(1)))
    return nums


def _extract_item_mentions(line: str, kind: str, prev_tail: str = "") -> list[tuple[int, str]]:
    """Extract main Figure/Table mentions, skipping Supplementary/Extended Data prefixes,
    citation locators ([@key, Table 3]), external-paper references ('Table 3 of Smith et al.'),
    and trailing counts ('Table 2 and 14 analyses')."""
    if kind == "Figure":
        head_plural, head_sing = r"(?:Figures|Figs\.?)", r"(?:Figure|Fig\.?)"
    else:
        head_plural, head_sing = r"Tables", r"Table"

    # Strip bracketed citation groups so '[@fonkoue2019, Table 3]' is not read as local Table 3
    line = re.sub(r"\[[^\]]*@[^\]]*\]", " ", line)

    item = r"\d+[a-z]?(?:\s*[-\u2013\u2014]\s*\d+[a-z]?)?"
    hits: list[tuple[int, int, str]] = []
    consumed: list[tuple[int, int]] = []
    local_in_re = re.compile(
        r"^\s+(?:in|of)\s+(?:the\s+)?(?:Section|Methods|Results|Discussion|Introduction|Abstract|Main\s+Text|Text|Part)\b",
        re.I,
    )
    supp_after_re = re.compile(r"^\s+(?:in|of)\s+(?:the\s+)?(?:Supplement\w*|Appendix|Online)\b", re.I)
    ext_after_re = re.compile(r"^\s+(?:of|in|from)\s+(?:[A-Z][a-z]+|Ref\.?|\[@)", re.ASCII)

    def _is_supp(pos: int, end_pos: int) -> bool:
        before = (prev_tail + " " + line[:pos]) if (pos == 0 or not line[:pos].strip()) else line[:pos]
        return bool(SUPP_PREFIX_RE.search(before) or supp_after_re.match(line[end_pos:]))

    def _is_external(end_pos: int) -> bool:
        tail = line[end_pos:]
        if local_in_re.match(tail):
            return False
        return bool(ext_after_re.match(tail))

    # 1. Plural lists/ranges: 'Figures 1, 2 and 4', 'Figures 1, 3-4', 'Tables 1 and 2'
    plural_re = re.compile(rf"\b{head_plural}\s+({item}(?:\s*,\s*{item})*(?:\s*,?\s*(?:and|&)\s*{item})?)", re.I)
    for m in plural_re.finditer(line):
        consumed.append(m.span())
        if _is_supp(m.start(), m.end()) or _is_external(m.end()):
            continue
        expr = m.group(1)
        if re.search(r",\s*\d+$", expr) and re.match(r"^\s+[a-z]{3,}", line[m.end():]):
            expr = re.sub(r",\s*\d+$", "", expr)
        for idx, n in enumerate(_expand_segment_list(expr)):
            hits.append((m.start() * 100 + idx, n, m.group(0)))

    # 2. Singular pairs/ranges: 'Figure 1 and 2', 'Table 1-2' — guard against 'Table 2 and 14 analyses'
    sing_pair_re = re.compile(
        rf"\b{head_sing}\s+(\d+)[a-z]?\s*(and|&|[-\u2013\u2014])\s*(\d+)[a-z]?",
        re.I,
    )
    for m in sing_pair_re.finditer(line):
        if any(a <= m.start() < b for a, b in consumed):
            continue
        a, op, b = int(m.group(1)), m.group(2).lower(), int(m.group(3))
        after = line[m.end():]
        # If 'and N <noun>' (e.g. 'Table 2 and 14 exploratory analyses', 'Figure 1 and 30 patients'), keep ONLY first num!
        if op in {"and", "&"} and (re.match(r"^\s+[a-z]{3,}", after) or b > a + 8):
            continue
        consumed.append(m.span())
        if _is_supp(m.start(), m.end()) or _is_external(m.end()):
            continue
        nums = list(range(a, b + 1)) if (op not in {"and", "&"} and a <= b <= a + 20) else [a, b]
        for idx, n in enumerate(nums):
            hits.append((m.start() * 100 + idx, n, m.group(0)))

    # 3. Simple singular: 'Figure 1', 'Fig 2', 'Fig. 2a', 'Table 1'
    sing_re = re.compile(rf"\b{head_sing}\s+(\d+)(?:[a-z]\b)?", re.I)
    for m in sing_re.finditer(line):
        if any(a <= m.start() < b for a, b in consumed):
            continue
        if _is_supp(m.start(), m.end()) or _is_external(m.end()):
            continue
        hits.append((m.start() * 100, int(m.group(1)), m.group(0)))

    hits.sort(key=lambda x: x[0])
    return [(n, raw) for _, n, raw in hits]


def check_figures_and_tables_md(
    numbered: list[tuple[int, str]],
    fmt: str,
    label: str,
    report: Report,
    extra_fig_nums: set[int],
    extra_tab_nums: set[int],
    base_dir: Path | None = None,
) -> None:
    # Captions: heading ('### Table 1.'), bold/italic ('**Figure 1.**', Nature '**Fig. 3 | Title.**'), or plain-line after blank
    styled_fig_cap = re.compile(r"^\s*(?:#{1,5}\s+|\*\*|\*)(?:Figure|Fig\.?)\s+(\d+)\s*[:.\-\u2014*|]", re.I)
    styled_tab_cap = re.compile(r"^\s*(?:#{1,5}\s+|\*\*|\*)Table\s+(\d+)\s*[:.\-\u2014*|]", re.I)
    plain_fig_cap = re.compile(r"^\s*(?:Figure|Fig\.?)\s+(\d+)\s*[:.\-\u2014|]\s+\S", re.I)
    plain_tab_cap = re.compile(r"^\s*Table\s+(\d+)\s*[:.\-\u2014|]\s+\S", re.I)
    roman_cap_re = re.compile(r"^\s*(?:#{1,5}\s+|\*\*|\*)?(?:Figure|Fig\.?|Table)\s+[IVXLCDM]+\s*[:.\-\u2014*|]", re.I)
    img_re = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    defined_figs, defined_tabs, caption_lines = set(), set(), set()
    caption_texts: list[str] = []
    roman_caps = 0
    prev_blank = True
    for ln, line in numbered:
        for im in img_re.finditer(line):
            alt, img_path = im.group(1), im.group(2).strip().split()[0]
            if fm := re.match(r"^(?:Figure|Fig\.?)\s+(\d+)\b", alt.strip(), re.I):
                defined_figs.add(int(fm.group(1)))
                caption_lines.add(ln)
            if base_dir and img_path and not re.match(r"^https?://", img_path, re.I):
                if not (base_dir / img_path).exists():
                    report.warn("REF-06", loc(label, ln, fmt), f"referenced figure image file not found: '{img_path}'")
        if m := styled_fig_cap.match(line):
            defined_figs.add(int(m.group(1)))
            caption_lines.add(ln)
            caption_texts.append(line)
        elif m := styled_tab_cap.match(line):
            defined_tabs.add(int(m.group(1)))
            caption_lines.add(ln)
            caption_texts.append(line)
        elif (prev_blank or fmt == "docx") and (m := plain_fig_cap.match(line)):
            defined_figs.add(int(m.group(1)))
            caption_lines.add(ln)
            caption_texts.append(line)
        elif (prev_blank or fmt == "docx") and (m := plain_tab_cap.match(line)):
            defined_tabs.add(int(m.group(1)))
            caption_lines.add(ln)
            caption_texts.append(line)
        elif roman_cap_re.match(line):
            roman_caps += 1
        prev_blank = not line.strip()

    known_figs = defined_figs | extra_fig_nums
    known_tabs = defined_tabs | extra_tab_nums
    if not known_figs and not known_tabs:
        if roman_caps:
            report.note(f"Detected {roman_caps} Roman-numeral Figure/Table caption(s) (IEEE style) — Arabic reference checks skipped")
        else:
            report.note("0 figure/table captions found — dangling/orphan reference checks skipped")
        return

    # Join wrapped body paragraphs so hard-wrapped 'Figure\n2' or 'Supplementary\nTable 1' is scanned accurately
    paragraphs: list[tuple[int, str]] = []
    cur_start, cur_parts = 0, []
    in_caption_para = False
    for ln, line in numbered:
        s = line.strip()
        if ln in caption_lines:
            if cur_parts:
                paragraphs.append((cur_start, " ".join(cur_parts)))
                cur_parts = []
            in_caption_para = True
            continue
        if not s or line.lstrip().startswith("#") or s.startswith("|"):
            if cur_parts:
                paragraphs.append((cur_start, " ".join(cur_parts)))
                cur_parts = []
            in_caption_para = False
            continue
        if in_caption_para:
            caption_texts.append(line)
            continue
        if not cur_parts:
            cur_start = ln
        cur_parts.append(mask_inline_code(line))
    if cur_parts:
        paragraphs.append((cur_start, " ".join(cur_parts)))

    cited_figs, cited_tabs, fig_first, tab_first = set(), set(), [], []
    for ln, para in paragraphs:
        for num, raw in _extract_item_mentions(para, "Figure"):
            cited_figs.add(num)
            if all(x[0] != num for x in fig_first):
                fig_first.append((num, ln, raw))
            if known_figs and num not in known_figs:
                report.fail("REF-01", loc(label, ln, fmt), f"dangling reference '{raw}' (Figure {num} not defined)")
        for num, raw in _extract_item_mentions(para, "Table"):
            cited_tabs.add(num)
            if all(x[0] != num for x in tab_first):
                tab_first.append((num, ln, raw))
            if known_tabs and num not in known_tabs:
                report.fail("REF-01", loc(label, ln, fmt), f"dangling reference '{raw}' (Table {num} not defined)")

    cap_joined = " ".join(caption_texts)
    cap_fig_mentions = {n for n, _ in _extract_item_mentions(cap_joined, "Figure")}
    cap_tab_mentions = {n for n, _ in _extract_item_mentions(cap_joined, "Table")}
    for num in sorted(defined_figs - cited_figs):
        extra = " outside captions" if num in cap_fig_mentions else ""
        report.fail("REF-02", label, f"orphaned Figure {num} caption is never referenced in body text{extra}")
    for num in sorted(defined_tabs - cited_tabs):
        extra = " outside captions" if num in cap_tab_mentions else ""
        report.fail("REF-02", label, f"orphaned Table {num} caption is never referenced in body text{extra}")

    _check_order(fig_first, "Figure", fmt, label, report)
    _check_order(tab_first, "Table", fmt, label, report)
    if extra_fig_nums and defined_figs and extra_fig_nums != defined_figs:
        report.warn("REF-05", label, f"figure parity mismatch: manuscript defines {sorted(defined_figs)}, figure-plan lists {sorted(extra_fig_nums)}")
    if extra_tab_nums and defined_tabs and extra_tab_nums != defined_tabs:
        report.warn("REF-05", label, f"table parity mismatch: manuscript defines {sorted(defined_tabs)}, figure-plan lists {sorted(extra_tab_nums)}")


# ---------------------------------------------------------------- checks: numbers & arithmetic

def extract_key_numbers(text: str) -> set[str]:
    """Extract salient quantitative numbers preserving leading negative sign ('-4.1')."""
    cleaned = re.sub(r"\b9[059]\s*%\s*(?:CI|confidence interval)\b", " ", text, flags=re.I)
    cleaned = re.sub(r"\b(?:19|20)\d{2}\b", " ", cleaned)
    cleaned = cleaned.replace("\u2212", "-")
    cleaned = re.sub(r"(?<![0-9A-Za-z])\.(\d+)", r"0.\1", cleaned)
    tokens: set[str] = set()
    # Negative sign preserved only when preceded by space, paren, comma, or start (not a range like '2.9-6.7')
    neg = r"(?:(?<=^)|(?<=[\s(,;]))-"
    for m in re.finditer(rf"({neg})?(?<![A-Za-z0-9.])\d{{1,3}}(?:,\d{{3}})*(?:\.\d+)?\s?%", cleaned):
        tokens.add(m.group(0).replace(",", "").replace(" ", ""))
    for m in re.finditer(rf"({neg})?(?<![A-Za-z0-9.])\d+\.\d+(?!\s?%)", cleaned):
        tokens.add(m.group(0))
    for m in re.finditer(r"\b[nN]\s*=\s*(\d{1,3}(?:,\d{3})*)", cleaned):
        tokens.add(m.group(1).replace(",", ""))
    for m in re.finditer(r"(?<![A-Za-z0-9.\-])(\d{1,3}(?:,\d{3})+|\d{2,})(?![A-Za-z0-9%]|\.\d)", cleaned):
        val = m.group(1).replace(",", "")
        if int(val) >= 20:
            tokens.add(val)
    return tokens


def normalize_numbers_text(text: str) -> str:
    t = text.replace("\u2212", "-")
    t = re.sub(r"(\d),(\d{3})", r"\1\2", t)
    t = re.sub(r"(\d)\s+%", r"\1%", t)
    return t


def number_present_in(tok: str, text_norm: str) -> bool:
    if tok.startswith("-"):
        mag = re.escape(tok[1:])
        return bool(re.search(rf"(?:^|[\s(,;])-{mag}(?![0-9]|\.[0-9])", text_norm))
    pat = re.escape(tok)
    # Require that a positive token is not ONLY matched as a negated value ('-4.1')
    if re.search(rf"(?<![0-9.\-]){pat}(?![0-9]|\.[0-9])", text_norm):
        return True
    if tok.startswith("0."):
        short_pat = re.escape(tok[1:])
        if re.search(rf"(?<![0-9\-]){short_pat}(?![0-9]|\.[0-9])", text_norm):
            return True
    return False


def check_frontmatter_body_numbers(
    title_text: str,
    keypoints_text: str,
    abstract_text: str,
    body_text_no_refs: str,
    label: str,
    report: Report,
) -> None:
    if not body_text_no_refs.strip():
        return
    body_norm = normalize_numbers_text(body_text_no_refs)
    for surface, txt in [("Title", title_text), ("Key Points", keypoints_text), ("Abstract", abstract_text)]:
        if not txt.strip():
            continue
        missing = [tok for tok in sorted(extract_key_numbers(txt)) if not number_present_in(tok, body_norm)]
        if missing:
            report.warn("NUM-01", label, f"{surface} value(s) not found in body/tables/captions (check drift or sign flip): {', '.join(missing)}")


def check_table_arithmetic(numbered: list[tuple[int, str]], fmt: str, label: str, report: Report) -> None:
    rows: list[tuple[int, list[str]]] = []
    for ln, line in numbered:
        s = line.strip()
        if "|" in s and (s.startswith("|") or re.search(r"\S\s*\|\s*\S", s)):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) >= 2:
                rows.append((ln, cells))
                continue
        if rows:
            _audit_single_table(rows, fmt, label, report)
            rows = []
    if rows:
        _audit_single_table(rows, fmt, label, report)


def _audit_single_table(rows: list[tuple[int, list[str]]], fmt: str, label: str, report: Report) -> None:
    if len(rows) < 2:
        return
    col_denoms, col_pct_hint, data_start, checked = {}, {}, 1, 0
    for ridx, (_, cells) in enumerate(rows[:4]):
        if all(set(c) <= set("-: ") for c in cells):
            data_start = ridx + 1
            continue
        if checked >= 2:
            break
        found = False
        for idx, h in enumerate(cells):
            if m := re.search(r"\b[nN]\s*=\s*(\d{1,3}(?:,\d{3})*)", h):
                val = int(m.group(1).replace(",", ""))
                if val > 0:
                    col_denoms[idx], found = val, True
            if re.search(r"(?:%|no\.\s*\(%\)|n\s*\(%\))", h, re.I):
                col_pct_hint[idx] = True
        checked += 1
        if ridx == 1 and found:
            data_start = max(data_start, 2)

    subset_row_re = re.compile(r"\b(?:among|subset|assessed|evaluated|tested|with\s+data)\b|\bn\s*=\s*\d+", re.I)
    continuous_row_re = re.compile(r"\b(?:mean|median|sd|iqr|range|sem|se|min|max)\b", re.I)
    for ln, cells in rows[data_start:]:
        if all(set(c) <= set("-: ") for c in cells):
            continue
        row_label = cells[0] if cells else ""
        if continuous_row_re.search(row_label):
            continue
        row_pct_hint = bool(re.search(r"(?:no\.|n)\s*\(%\)|%", row_label, re.I))
        for idx, raw_cell in enumerate(cells):
            if idx == 0:
                continue
            cell = re.sub(r"^\*\*|\*\*$", "", raw_cell.strip())
            cell = re.sub(r"[*†‡§ᵃᵇᶜᵈ]+$", "", cell).strip()
            # Explicit 'n/N (pct%)' cell works even without a column header denominator or on subset rows
            if fm := re.match(r"^(\d{1,3}(?:,\d{3})*)\s*/\s*(\d{1,3}(?:,\d{3})*)\s*\((\d+(?:\.\d+)?)\s*(%?)\)$", cell):
                num = int(fm.group(1).replace(",", ""))
                denom = int(fm.group(2).replace(",", ""))
                pct_str = fm.group(3)
                if denom <= 0:
                    continue
                if num > denom:
                    report.warn("TAB-01", loc(label, ln, fmt), f"table count exceeds denominator: {num}/{denom}")
                else:
                    decimals = len(pct_str.split(".")[1]) if "." in pct_str else 0
                    tol = 0.55 if decimals == 0 else (0.15 if decimals == 1 else 0.05)
                    expected = 100.0 * num / denom
                    if abs(expected - float(pct_str)) > tol:
                        report.warn("TAB-01", loc(label, ln, fmt), f"table arithmetic mismatch: {num}/{denom} is {expected:.{max(decimals, 1)}f}%, not {pct_str}%")
                continue
            if idx not in col_denoms or subset_row_re.search(row_label):
                continue
            denom = col_denoms[idx]
            m = re.match(r"^(\d{1,3}(?:,\d{3})*)\s*\((\d+(?:\.\d+)?)\s*(%?)\)$", cell)
            if not m or (not m.group(3) and not (row_pct_hint or col_pct_hint.get(idx))):
                continue
            num, pct_str = int(m.group(1).replace(",", "")), m.group(2)
            if num > denom:
                report.warn("TAB-01", loc(label, ln, fmt), f"table count exceeds column denominator: {num} > {denom}")
                continue
            decimals = len(pct_str.split(".")[1]) if "." in pct_str else 0
            tol = 0.55 if decimals == 0 else (0.15 if decimals == 1 else 0.05)
            expected = 100.0 * num / denom
            if abs(expected - float(pct_str)) > tol:
                report.warn("TAB-01", loc(label, ln, fmt), f"table arithmetic mismatch: {num}/{denom} is {expected:.{max(decimals, 1)}f}%, not {pct_str}%")


# ---------------------------------------------------------------- checks: declarations, budgets, style

def check_declarations_present(
    body_secs: list[tuple[str, int, list[tuple[int, str]]]],
    total_words: int,
    label: str,
    report: Report,
) -> None:
    """Verify required declarations use raw unnumbered Markdown headings that match
    academic-humanizer/scripts/preservation_check.py's exact DECLARATION_HEAD regex."""
    if total_words < 400:
        return
    locked_raw: list[str] = []
    warned_dec: set[str] = set()

    for title, lvl, lines in body_secs:
        if lvl > 0:
            raw_line = f"{'#' * lvl} {title.strip()}"
            if HUMANIZER_DECLARATION_HEAD.match(raw_line):
                locked_raw.append(title.strip())
            else:
                norm = normalize_heading(title)
                if NON_LOCK_SAFE_DECLARATIONS.search(norm) or any(p.search(norm) for p in LOCK_SAFE_DECLARATIONS.values()):
                    key = title.strip().lower()
                    if key not in warned_dec:
                        warned_dec.add(key)
                        report.warn(
                            "DEC-02", label,
                            f"declaration heading '{title.strip()}' is not auto-locked by academic-humanizer "
                            f"(use an unnumbered bare heading like '### Funding', '### Data Availability', '### Code Availability')",
                        )
        if normalize_heading(title).lower().startswith(("declaration", "ethics", "acknowledg", "disclosure", "funding")):
            for _, line in lines:
                if bm := re.match(r"^\*\*([^*]{3,60})\*\*", line.strip()):
                    lbl = bm.group(1).strip(" :.")
                    if NON_LOCK_SAFE_DECLARATIONS.search(lbl) or any(p.search(lbl) for p in LOCK_SAFE_DECLARATIONS.values()):
                        key = f"bold:{lbl.lower()}"
                        if key not in warned_dec:
                            warned_dec.add(key)
                            report.warn(
                                "DEC-02", label,
                                f"bold run-in declaration '**{lbl}**' is not auto-locked by academic-humanizer "
                                f"(promote to a bare heading like '### {lbl}')",
                            )

    missing = [name for name, pat in LOCK_SAFE_DECLARATIONS.items() if not any(pat.search(h) for h in locked_raw)]
    if missing:
        report.warn("DEC-01", label, f"missing lock-safe declaration heading(s): {', '.join(missing)}")


def check_budgets_and_limitations(
    abstract_text: str,
    top_level: int,
    body_secs: list[tuple[str, int, list[tuple[int, str]]]],
    fmt: str,
    label: str,
    report: Report,
    max_abstract: int | None,
    max_words: int | None,
    section_budgets: dict[str, int] | None,
    lim_threshold: float,
    style_mode: bool,
) -> int:
    abs_words = len(clean_prose_words(abstract_text, fmt)) if abstract_text.strip() else 0
    total_words, disc_words, lim_words = 0, 0, 0
    in_discussion, in_skipped = False, False
    sec_totals: dict[str, int] = {"Abstract": abs_words} if abs_words else {}
    current_top: str | None = None

    for title, level, body in body_secs:
        body_str = "\n".join(line for _, line in body)
        w = len(clean_prose_words(body_str, fmt, skip_tables=True))
        norm = normalize_heading(title).lower()
        if level == top_level:
            in_skipped = norm.startswith(SKIP_BUDGET_PREFIXES)
        if norm in {"front", "preamble"} or level < top_level or norm.startswith(SKIP_BUDGET_PREFIXES) or in_skipped:
            continue
        total_words += w
        if level == top_level:
            current_top = title
            sec_totals[current_top] = sec_totals.get(current_top, 0) + w
            in_discussion = norm.startswith("discussion")
            if in_discussion:
                disc_words += w
        else:
            if current_top:
                sec_totals[current_top] = sec_totals.get(current_top, 0) + w
            if in_discussion:
                disc_words += w
                if "limitation" in norm:
                    lim_words += w

        if style_mode and level == top_level + 1:
            if not any(k in norm for k in ("limitation", "conclusion", "ethic", "funding", "data", "code", "conflict", "disclosure", "ai-use", "acknowledg")):
                blocks = [b.strip() for b in re.split(r"\n\s*\n", body_str) if b.strip()]
                has_struct = any(b.startswith(("|", "-", "*", "1.", "![", "\\begin{")) for b in blocks)
                sentences = len(re.findall(r"[.!?](?:\s|$)", body_str))
                if len(blocks) == 1 and not has_struct and (w < 50 or sentences <= 2):
                    report.warn("STY-05", label, f"short single-paragraph subsection '{title}' ({w} words)")

    report.note(f"Word counts ({label}): total body={total_words}" + (f", abstract={abs_words}" if abs_words else ""))
    if sec_totals:
        report.note("Sections: " + ", ".join(f"{k}={v}" for k, v in list(sec_totals.items())[:10]))

    if max_abstract is not None and abs_words > max_abstract:
        report.warn("BUD-01", label, f"Abstract has {abs_words} words, exceeding limit of {max_abstract}")
    if max_words is not None and total_words > max_words:
        report.warn("BUD-02", label, f"Main body has {total_words} words, exceeding limit of {max_words}")
    if section_budgets:
        for sec_name, actual in sec_totals.items():
            snorm = normalize_heading(sec_name).lower()
            if snorm == "abstract":
                continue
            for bk, blim in section_budgets.items():
                if snorm.startswith(bk) and actual > int(blim * 1.15):
                    report.warn("BUD-03", label, f"section '{sec_name}' has {actual} words, exceeding plan budget of {blim} by >15%")
                    break
    if disc_words >= 80 and lim_words > 0 and (lim_words / disc_words) > lim_threshold:
        pct = round(100 * lim_words / disc_words)
        report.warn("LIM-01", label, f"Limitations subsection is {pct}% of Discussion ({lim_words}/{disc_words} words; threshold {round(lim_threshold * 100)}%)")
    return total_words


def check_opt_in_style(
    numbered: list[tuple[int, str]],
    body_secs: list[tuple[str, int, list[tuple[int, str]]]],
    keypoints_text: str,
    abstract_text: str,
    fmt: str,
    label: str,
    is_observational: bool,
    report: Report,
) -> None:
    # Structural tells
    for ln, line in numbered:
        scan = mask_inline_code(line) if fmt != "tex" else line
        for rule, pat, desc in STRUCTURAL_TELL_PATTERNS:
            if pat.search(scan):
                report.warn(rule, loc(label, ln, fmt), f"structural tell — {desc}")
    # Acronyms (excluding References & captions; 1x Abstract + 1x Body allowed)
    cap_re = re.compile(r"^\s*(?:#{1,4}\s+|\*\*|\*)?(?:Figure|Fig\.?|Table)\s+\d+\s*[:.\-\u2014*]", re.I)
    body_lines, prose_lines = [], []
    for title, _, lines in body_secs:
        if normalize_heading(title).lower().startswith(("references", "bibliography")):
            continue
        in_cap = False
        for _, line in lines:
            body_lines.append(line)
            if fmt != "tex":
                if cap_re.match(line):
                    in_cap = True
                    continue
                if in_cap:
                    if not line.strip():
                        in_cap = False
                    continue
                prose_lines.append(mask_inline_code(line))
            else:
                prose_lines.append(line)
    prose_txt = "\n".join(prose_lines)
    body_txt = "\n".join(body_lines)
    defs: dict[str, int] = {}
    for m in re.finditer(r"\b[A-Za-z][A-Za-z0-9\- ]{3,80}\(([A-Z]{3,6})\)", prose_txt):
        defs[m.group(1)] = defs.get(m.group(1), 0) + 1
    for acr, cnt in sorted(defs.items()):
        if cnt > 1 and acr not in COMMON_ACRONYMS:
            report.warn("STY-06", label, f"acronym '{acr}' defined {cnt} times in body prose")
    all_defs = set(defs) | {m.group(1) for m in re.finditer(r"\b[A-Za-z][A-Za-z0-9\- ]{3,80}\(([A-Z]{3,6})\)", body_txt + "\n" + abstract_text)}
    body_no_brackets = re.sub(r"\[[^\]]*\]", " ", body_txt)
    uses: dict[str, int] = {}
    for m in re.finditer(r"\b([A-Z]{3,6})\b", body_no_brackets):
        tok = m.group(1)
        if tok not in COMMON_ACRONYMS and tok not in ENGLISH_CAPS_IGNORE:
            uses[tok] = uses.get(tok, 0) + 1
    if undef := [f"{a} ({c}x)" for a, c in sorted(uses.items()) if c >= 3 and a not in all_defs]:
        report.warn("STY-07", label, f"repeated acronym(s) without definition: {', '.join(undef)}")
    # Observational causal verbs
    if is_observational:
        hits = [f"{sn} ('{m.group(0)}')" for sn, txt in [("Key Points", keypoints_text), ("Abstract", abstract_text)] for m in CAUSAL_VERB_RE.finditer(txt)]
        for title, _, body in body_secs:
            norm = normalize_heading(title).lower()
            if "limitation" not in norm and norm.startswith(("results", "discussion", "conclusion")):
                for ln, line in body:
                    for m in CAUSAL_VERB_RE.finditer(line):
                        hits.append(f"{loc(label, ln, fmt)} ('{m.group(0)}')")
        if hits:
            report.warn("STY-08", label, f"observational design causal verb(s): {', '.join(hits[:6])}" + (f" (+{len(hits)-6} more)" if len(hits) > 6 else ""))


# ---------------------------------------------------------------- checks: companion artifacts

@dataclass
class PlanMeta:
    is_observational: bool = False
    is_clinical: bool = False
    plan_max_abstract: int | None = None
    plan_max_words: int | None = None
    section_budgets: dict[str, int] = field(default_factory=dict)


def _parse_budget_upper(raw: str) -> int | None:
    nums = [int(n) for n in re.findall(r"\b(\d{2,5})\b", raw.replace(",", ""))]
    return max(nums) if nums else None


def check_manuscript_plan(path: Path, manuscript_text: str, report: Report) -> PlanMeta:
    meta = PlanMeta()
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    full, name = "\n".join(lines), path.name
    secs = parse_md_h2_sections(lines)

    if re.search(r"Field family & study type:.*(?:clinical|epidemiolog|strobe|consort)", full, re.I):
        meta.is_clinical = True
    if re.search(r"Field family & study type:.*(?:observational|cohort|case-control|cross-sectional)", full, re.I):
        meta.is_observational = True

    body_sum = 0
    for _, r in parse_first_table(find_section(secs, "Section Architecture")):
        sn = col(r, "section").strip().lower()
        val = _parse_budget_upper(col(r, "budget"))
        if val is None:
            continue
        if sn.startswith("abstract"):
            meta.plan_max_abstract = val
        elif sn:
            meta.section_budgets[sn] = val
            body_sum += val
    if body_sum > 0:
        meta.plan_max_words = body_sum

    sel = find_section(secs, "Selected Framing")
    ledger_sec = find_section(secs, "Claims-Evidence Ledger")
    # If using a non-template project PLAN.md that has neither template section, stay quiet rather than emitting template noise
    if name.lower() != "manuscript-plan.md" and sel is None and ledger_sec is None:
        return meta

    if not sel or not any(
        (m := re.match(r"^\s*-\s*\*\*One-sentence contribution:\*\*\s*(.+)$", l, re.I)) and not re.search(r"<[^>]+>|TODO|TBD", m.group(1))
        for _, l in sel
    ):
        report.warn("PLN-01", name, "missing concrete 'One-sentence contribution' under '## Selected Framing'")

    rows = parse_first_table(ledger_sec)
    if not rows:
        report.warn("PLN-02", name, "missing or empty '## Claims-Evidence Ledger'")
        return meta

    seen_ids, verified_vals = set(), []
    for ln, r in rows:
        cid = col(r, "id").strip()
        src = col(r, "evidence", "source").strip()
        vals = col(r, "exact values", "values").strip()
        status = col(r, "status").strip().lower()
        target_sec = col(r, "target", "main", "section").strip()
        if not cid:
            report.fail("LED-01", f"{name}:{ln}", "claim row missing ID")
            continue
        if cid in seen_ids:
            report.fail("LED-02", f"{name}:{ln}", f"duplicate claim ID '{cid}'")
        seen_ids.add(cid)
        if status not in CLAIM_STATUSES:
            report.fail("LED-03", f"{name}:{ln}", f"claim {cid} has invalid status '{status}'")
        elif status == "verified":
            if not src or src in {"-", "—", "none", "TBD", "TODO"} or src.startswith("<"):
                report.fail("LED-04", f"{name}:{ln}", f"verified claim {cid} has no concrete evidence source")
            elif vals:
                verified_vals.append((cid, vals))
        elif status == "unverified":
            report.warn("LED-05", f"{name}:{ln}", f"claim {cid} is still 'unverified'")
        elif status == "gap":
            if target_sec and not re.search(r"exclud|none|omit|future|internal|scoped|not in|limitation", target_sec, re.I):
                report.fail("LED-06", f"{name}:{ln}", f"gap claim {cid} targets main section '{target_sec}'")

    if manuscript_text and verified_vals:
        ms_norm = normalize_numbers_text(manuscript_text)
        for cid, vals in verified_vals:
            if missing := [tok for tok in sorted(extract_key_numbers(vals)) if not number_present_in(tok, ms_norm)]:
                report.warn("LED-07", name, f"verified claim {cid} value(s) not found in manuscript: {', '.join(missing)}")
    return meta


def check_figure_plan(path: Path) -> tuple[set[int], set[int]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    secs = parse_md_h2_sections(lines)
    fig_nums, tab_nums = set(), set()
    for _, r in parse_first_table(find_section(secs, "Main Figure")):
        item = col(r, "item", "figure", "id")
        if fm := re.match(r"^(?:Figure|Fig\.?)\s+(\d+)\b", item, re.I):
            fig_nums.add(int(fm.group(1)))
        elif tm := re.match(r"^Table\s+(\d+)\b", item, re.I):
            tab_nums.add(int(tm.group(1)))
    return fig_nums, tab_nums


def _parse_status_cell(raw: str) -> tuple[str, str]:
    """Parse '**Resolved** (see Methods)' or 'resolved: Table 2' -> ('resolved', 'see Methods')."""
    s = re.sub(r"[*_`]", "", raw).strip()
    m = re.match(r"^([a-z][a-z\-]*)\s*(?:\(([^)]*)\)|[:—\-]\s*(.+))?$", s, re.I)
    if not m:
        return s.lower(), ""
    return m.group(1).lower(), (m.group(2) or m.group(3) or "").strip()


def _parse_severity_cell(raw: str) -> str:
    """Normalize '**FATAL** (methods)' -> 'FATAL'."""
    s = re.sub(r"[*_`\[\]]", "", raw).strip()
    m = re.match(r"^(FATAL|MAJOR|MINOR|INFO)\b", s, re.I)
    return m.group(1).upper() if m else s.upper()


def _is_concrete_locator(loc_txt: str) -> bool:
    s = re.sub(r"[*_`]", "", loc_txt).strip()
    if len(s) < 3:
        return False
    if re.fullmatch(r"(?:tbd|todo|pending|none|n/?a|unknown|\?+|-+|—+|see\s+text)", s, re.I):
        return False
    return True


def check_adversarial_review(path: Path, report: Report) -> None:
    """Deny-by-default fail-closed adversarial review check.
    Scans every finding table regardless of heading level/name, ignores fenced code blocks,
    and requires every live FATAL mention to resolve cleanly with a concrete locator."""
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    name = path.name
    numbered, _ = strip_md_nonprose(raw_lines, 0)

    # 1. Scan EVERY table in the file that has an ID-like column AND a Severity column
    matrix: dict[str, tuple[str, str, str, int]] = {}
    for tbl in parse_all_tables(numbered):
        for ln, r in tbl:
            fid = re.sub(r"[*_`]", "", col(r, "id", "finding", "#", "item")).strip().upper()
            sev = _parse_severity_cell(col(r, "severity", "level", "grade"))
            if not fid or not sev:
                continue
            st_word, st_loc = _parse_status_cell(col(r, "status", "state"))
            loc_col = col(r, "locator", "edit", "resolution", "location").strip()
            matrix[fid] = (sev, st_word, st_loc or loc_col, ln)

    # 2. Scan non-table lines for findings & deny-by-default FATAL tokens
    tagged_finding_re = re.compile(
        r"^(?:[-*#>\s]*)(?:\*\*|__)?(?:\[)?(FATAL|MAJOR)(?:\])?(?:\*\*|__)?(?:\s*[:\-—]\s*|\s+)(?:([A-Z]{1,4}[-]?\d+)\b)?",
        re.I,
    )
    boilerplate_fatal_re = re.compile(
        r"(?:\b(?:zero|0|no)\s+(?:open\s+)?FATAL\b"
        r"|\bif\s+any\s+FATAL\b"
        r"|\bany\s+resolved\s+FATAL\b"
        r"|\b(?:one|two|three|\d+)\s+or\s+more\s+FATAL\b"
        r"|\bSubmission\s+Verdict\b"
        r"|\*\*Verdict:\*\*"
        r"|Kill-Switch\s*/\s*Pivot"
        r"|Residual\s+Objections"
        r"|Decision\s+Matrix"
        r"|Single\s+source\s+of\s+truth)",
        re.I,
    )

    seen_ids: set[str] = set()
    parsed_any_finding = bool(matrix)
    verdict_line: tuple[int, str] | None = None

    for ln, line in numbered:
        s = line.strip()
        if not s or s.startswith("|"):
            continue
        if re.match(r"^(?:-\s*)?\*\*Verdict:\*\*", s, re.I):
            verdict_line = (ln, s)
            continue

        m = tagged_finding_re.match(s)
        if not m and (bm := re.search(r"\[(FATAL|MAJOR)\]\s*([A-Z]{1,4}[-]?\d+)?", s, re.I)):
            m = bm

        if m and not boilerplate_fatal_re.search(s):
            parsed_any_finding = True
            sev = m.group(1).upper()
            fid = (m.group(2) or "").upper()
            sm = re.search(r"Status:\s*([^\n`]+)", s, re.I)
            in_st, in_loc = _parse_status_cell(sm.group(1)) if sm else ("", "")
            if fid:
                seen_ids.add(fid)
                if fid in matrix:
                    m_sev, m_st, m_loc, m_ln = matrix[fid]
                    eff_sev = "FATAL" if ("FATAL" in {sev, m_sev}) else "MAJOR"
                    if m_sev and m_sev != sev:
                        report.fail("REV-02", f"{name}:{ln}", f"severity conflict for {fid}: inline {sev} vs matrix {m_sev}")
                    if in_st and m_st and in_st != m_st:
                        (report.fail if eff_sev == "FATAL" else report.warn)(
                            "REV-02", f"{name}:{ln}", f"status conflict for {fid}: inline '{in_st}' vs matrix '{m_st}'"
                        )
                    _eval_review_item(eff_sev, fid, m_st or in_st, m_loc or in_loc, f"{name}:{m_ln}", report)
                else:
                    _eval_review_item(sev, fid, in_st, in_loc, f"{name}:{ln}", report)
            else:
                _eval_review_item(sev, f"line-{ln}", in_st, in_loc, f"{name}:{ln}", report)
            continue

        # Deny-by-default fallback: any remaining uppercase FATAL mention not in boilerplate fails closed
        if re.search(r"\bFATAL\b", s) and not boilerplate_fatal_re.search(s):
            parsed_any_finding = True
            sm = re.search(r"Status:\s*([^\n`]+)", s, re.I)
            in_st, in_loc = _parse_status_cell(sm.group(1)) if sm else ("", "")
            _eval_review_item("FATAL", f"line-{ln}", in_st, in_loc, f"{name}:{ln}", report)

    open_fatals, open_majors = [], []
    for fid, (sev, st, loc_txt, ln) in matrix.items():
        if st and st not in VALID_STATUSES:
            report.warn("REV-03", f"{name}:{ln}", f"finding {fid} has unrecognized status '{st}'")
        if sev == "FATAL" and (st not in RESOLVED_STATUSES or (st in {"resolved", "narrowed"} and not _is_concrete_locator(loc_txt))):
            open_fatals.append(fid)
        if sev == "MAJOR" and st not in RESOLVED_STATUSES:
            open_majors.append(fid)
        if fid not in seen_ids and sev in {"FATAL", "MAJOR"}:
            _eval_review_item(sev, fid, st, loc_txt, f"{name}:{ln}", report)

    if not parsed_any_finding and not any(re.search(r"\b(?:MINOR|Residual\s+Objections)\b", l, re.I) for _, l in numbered):
        report.fail("REV-00", name, "adversarial review file is empty or contains no parseable findings or decision matrix")

    if verdict_line and re.search(r"\bReady\s+after\s+minor\s+fixes\b", verdict_line[1], re.I):
        if open_fatals:
            report.fail("REV-06", f"{name}:{verdict_line[0]}", f"Verdict claims 'Ready after minor fixes' while FATAL finding(s) remain open: {', '.join(open_fatals)}")
        elif open_majors:
            report.warn("REV-06", f"{name}:{verdict_line[0]}", f"Verdict claims 'Ready after minor fixes' while MAJOR finding(s) remain open: {', '.join(open_majors)}")


def _eval_review_item(sev: str, fid: str, st: str, loc_txt: str, where: str, report: Report) -> None:
    if sev == "FATAL":
        if st not in RESOLVED_STATUSES:
            report.fail("REV-01", where, f"unresolved FATAL finding {fid} (Status: '{st or 'missing'}')")
        elif st in {"resolved", "narrowed"} and not _is_concrete_locator(loc_txt):
            report.fail("REV-04", where, f"FATAL finding {fid} marked '{st}' without citing a concrete edit locator")
        elif st == "accepted-risk" and not _is_concrete_locator(loc_txt):
            report.fail("REV-04", where, f"FATAL finding {fid} marked 'accepted-risk' without author attestation/rationale")
    elif sev == "MAJOR" and st not in RESOLVED_STATUSES:
        report.warn("REV-05", where, f"open MAJOR finding {fid} (Status: '{st or 'missing'}')")


def check_rebuttal_plan(path: Path, report: Report, stage: str = "submission") -> list[str]:
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    name = path.name
    numbered, _ = strip_md_nonprose(raw_lines, 0)
    rows = parse_first_table(find_section(parse_md_h2_sections(raw_lines), "Atomic Reviewer"))
    if not rows:
        # Fallback: any table with an ID + Status column
        for tbl in parse_all_tables(numbered):
            if tbl and col(tbl[0][1], "id") and col(tbl[0][1], "status"):
                rows = tbl
                break
    emit = report.fail if stage == "submission" else report.warn
    if not rows:
        emit("REB-01", name, "no rows in '## Atomic Reviewer Critiques'")
        return []
    critique_ids: list[str] = []
    for ln, r in rows:
        rid = re.sub(r"[*_`]", "", col(r, "id")).strip() or f"row@{ln}"
        if not rid.startswith("row@"):
            critique_ids.append(rid)
        st, _ = _parse_status_cell(col(r, "status"))
        loc_val = col(r, "target", "location", "manuscript").strip()
        if st not in VALID_STATUSES:
            emit("REB-01", f"{name}:{ln}", f"rebuttal item {rid} has non-standard status '{st or 'missing'}' (expected {'|'.join(sorted(VALID_STATUSES))})")
        elif st not in RESOLVED_STATUSES:
            emit("REB-01", f"{name}:{ln}", f"rebuttal item {rid} is unresolved (Status: '{st}')")
        if not loc_val or loc_val in {"-", "—", "TBD", "TODO"}:
            emit("REB-01", f"{name}:{ln}", f"rebuttal item {rid} has no target manuscript location")
    return critique_ids


def _normalize_quote_text(text: str) -> str:
    t = text.replace("\u00a0", " ")
    t = t.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")
    t = re.sub(r"\[[^\]]*@[^\]]*\]|\[\d+(?:[\s,\-–]+\d+)*\]", "", t)
    t = re.sub(r"[*_`]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t.lower()


def check_response_letter_quotes(
    letter_path: Path,
    manuscript_clean_text: str,
    report: Report,
    rebuttal_ids: list[str] | None = None,
) -> None:
    """Mechanically verify every revision quote in response-letter.md against comment-stripped manuscript text."""
    if not manuscript_clean_text.strip():
        return
    ms_norm = _normalize_quote_text(manuscript_clean_text)
    raw_lines = letter_path.read_text(encoding="utf-8", errors="replace").splitlines()
    full_letter = "\n".join(raw_lines)
    marker_re = re.compile(
        r"^(?:\*\*)?(?:Manuscript\s+(?:revision|change|edit|text)|Revised\s+(?:text|passage|manuscript))\b[^:]*:(?:\*\*)?\s*(.*)$",
        re.I,
    )

    def _verify_quote(raw_q: str, ln: int) -> bool:
        q = re.sub(r"\s+", " ", raw_q).strip()
        # Strip optional trailing parenthetical locator like '(Methods — Splits)'
        q = re.sub(r"\s*\([^)]{3,60}\)\s*$", "", q).strip().strip('"\'\u201c\u201d')
        if len(q) < 12:
            return False
        parts = [p.strip(' "\'\u201c\u201d') for p in re.split(r"\.{3}|\u2026|\[\.\.\.\]", q) if len(p.strip()) >= 12]
        if not parts:
            parts = [q]
        pos = 0
        for part in parts:
            pn = _normalize_quote_text(part)
            if not pn:
                continue
            found = ms_norm.find(pn, pos)
            if found == -1:
                report.fail("REB-02", f"{letter_path.name}:{ln}", f"quoted manuscript revision not found in manuscript: '{q[:65]}...'")
                return True
            pos = found + len(pn)
        return True

    checked = 0
    checked_quote_lines: set[int] = set()
    i = 0
    while i < len(raw_lines):
        s = raw_lines[i].strip()
        if m := marker_re.match(s):
            inline_tail = m.group(1).strip()
            if inline_tail and (inline_tail.startswith(('"', "\u201c")) or len(inline_tail) >= 20):
                if _verify_quote(inline_tail, i + 1):
                    checked += 1
                    checked_quote_lines.add(i + 1)
                i += 1
                continue
            j = i + 1
            skipped_intro = 0
            # Collect one or more blockquotes under this marker (allowing 1 short intro line or blank line)
            while j < len(raw_lines):
                js = raw_lines[j].strip()
                if js.startswith(">"):
                    q_lines: list[str] = []
                    q_start = j + 1
                    while j < len(raw_lines) and raw_lines[j].lstrip().startswith(">"):
                        checked_quote_lines.add(j + 1)
                        q_lines.append(raw_lines[j].lstrip()[1:].strip())
                        j += 1
                    if q_lines and _verify_quote(" ".join(q_lines), q_start):
                        checked += 1
                    continue
                if not js:
                    # Peek ahead: continue if next non-blank line is another blockquote
                    k = j + 1
                    while k < len(raw_lines) and not raw_lines[k].strip():
                        k += 1
                    if k < len(raw_lines) and raw_lines[k].lstrip().startswith(">"):
                        j = k
                        continue
                    break
                if skipped_intro == 0 and not js.startswith(("#", "**Response", "**Comment", "---")):
                    skipped_intro += 1
                    j += 1
                    continue
                break
            i = max(j, i + 1)
        else:
            i += 1

    if checked:
        report.note(f"Verified {checked} quoted revision passage(s) in {letter_path.name} against manuscript")
    else:
        report.warn("REB-03", letter_path.name, "no revision quote blocks were found/verified in response-letter.md")

    # Cross-check rebuttal-plan IDs against response-letter.md
    if rebuttal_ids:
        missing_ids = [rid for rid in rebuttal_ids if not re.search(rf"\b{re.escape(rid)}\b", full_letter)]
        if missing_ids:
            report.warn("REB-04", letter_path.name, f"rebuttal-plan critique ID(s) missing from response-letter.md: {', '.join(missing_ids)}")


# ---------------------------------------------------------------- discovery & driver

def _is_manuscript_candidate(p: Path) -> bool:
    if not p.is_file():
        return False
    low = p.name.lower()
    if low in ARTIFACT_NAMES or any(pat.search(low) for pat in NON_MANUSCRIPT_PATTERNS):
        return False
    return p.suffix.lower() in {".md", ".qmd", ".rmd", ".docx", ".tex"}


def _candidate_rank(p: Path, zotero_keys_name: str | None = None) -> tuple[int, int, str]:
    low, stem = p.name.lower(), p.stem.lower()
    if ".revised." in low or stem.endswith(("-revised", "_revised")):
        stage = 0
    elif ".structural." in low or stem.endswith(("-structural", "_structural")):
        stage = 1
    elif zotero_keys_name and low == zotero_keys_name.lower():
        stage = 2
    elif ".keys." in low:
        stage = 3
    elif ".draft." in low or stem.startswith("draft") or "manuscript" in stem:
        stage = 4
    else:
        stage = 5
    return (stage, {".md": 0, ".qmd": 0, ".rmd": 0, ".docx": 1, ".tex": 2}.get(p.suffix.lower(), 3), p.name)


def discover_files(target: Path, args: argparse.Namespace, report: Report) -> tuple[Path | None, dict[str, Path]]:
    artifacts: dict[str, Path] = {}
    manuscript: Path | None = None
    zotero_keys_name: str | None = None

    def _scan_dir(d: Path, exclude: Path | None = None) -> None:
        nonlocal zotero_keys_name
        for key, fname in [
            ("plan", "manuscript-plan.md"),
            ("figure_plan", "figure-plan.md"),
            ("review", "adversarial-review.md"),
            ("rebuttal", "rebuttal-plan.md"),
            ("response", "response-letter.md"),
        ]:
            p = d / fname
            if p.exists() and p != exclude:
                artifacts[key] = p
        if "plan" not in artifacts:
            p = d / "PLAN.md"
            if p.exists() and p != exclude:
                artifacts["plan"] = p

        zcfg = d / "zotero.json"
        if zcfg.exists() and zcfg != exclude:
            resolved_refs, zkeys, zerr = inspect_zotero_config(zcfg)
            if zkeys:
                zotero_keys_name = zkeys
            if zerr:
                report.fail("CIT-01", zcfg.name, zerr)
            elif resolved_refs is not None:
                artifacts["bib"] = resolved_refs
                report.note("sync-refs project detected (zotero.json); project sync-refs/docx_checks remain authoritative for live Zotero assembly")
        else:
            preferred = d / "manuscript-refs.json"
            if preferred.exists() and preferred != exclude:
                artifacts["bib"] = preferred
            else:
                for cand in sorted(d.glob("*refs.json")):
                    if cand != exclude:
                        artifacts["bib"] = cand
                        break
            if "bib" not in artifacts:
                for fname in ("references.bib", "references.json"):
                    p = d / fname
                    if p.exists() and p != exclude:
                        artifacts["bib"] = p
                        break

    if target.is_dir():
        _scan_dir(target)
        candidates = sorted((p for p in target.iterdir() if _is_manuscript_candidate(p)), key=lambda p: _candidate_rank(p, zotero_keys_name))
        if candidates:
            top_rank = _candidate_rank(candidates[0], zotero_keys_name)[0]
            if len(candidates) > 1 and top_rank == 5:
                report.fail("DIS-01", target.resolve().name, f"ambiguous directory with no draft/keys/manuscript file; pass an explicit file ({', '.join(p.name for p in candidates)})")
            else:
                manuscript = candidates[0]
                if len(candidates) > 1:
                    report.warn("DIS-02", target.resolve().name, f"multiple candidates; checking '{manuscript.name}' (skipped: {', '.join(p.name for p in candidates[1:])})")
                elif top_rank == 5:
                    report.warn("DIS-03", target.resolve().name, f"checking generic Markdown file '{manuscript.name}' (pass an explicit file path to confirm)")
    else:
        direct_artifact = {
            "manuscript-plan.md": "plan",
            "figure-plan.md": "figure_plan",
            "adversarial-review.md": "review",
            "rebuttal-plan.md": "rebuttal",
            "response-letter.md": "response",
        }.get(target.name.lower())
        if direct_artifact is not None:
            artifacts[direct_artifact] = target
        else:
            manuscript = target
            _scan_dir(target.parent, exclude=target)

    for attr, key in [("plan", "plan"), ("figure_plan", "figure_plan"), ("review", "review"), ("rebuttal", "rebuttal"), ("response", "response"), ("bib", "bib")]:
        if raw_val := getattr(args, attr, None):
            p = Path(raw_val)
            if not p.exists():
                report.fail("IO-01", str(p), f"--{attr.replace('_', '-')} path does not exist")
            else:
                artifacts[key] = p

    return manuscript, artifacts


def run_checks(target: Path, args: argparse.Namespace) -> Report:
    accept_rules: set[str] = set()
    accept_substrings: list[str] = []
    accept_errors: list[tuple[str, str]] = []

    raw_accepts = list(getattr(args, "accept", None) or [])
    raw_subs = list(getattr(args, "accept_substring", None) or [])
    if af := getattr(args, "accept_file", None):
        p = Path(af)
        if not p.exists():
            accept_errors.append((str(p), "--accept-file path does not exist"))
        else:
            for line in p.read_text(encoding="utf-8").splitlines():
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                if s.lower().startswith("sub:"):
                    raw_subs.append(s[4:].strip())
                else:
                    raw_accepts.append(s)

    for tok in raw_accepts:
        t = tok.strip().upper()
        if not t or not RULE_ID_RE.match(t):
            accept_errors.append(("--accept", f"invalid rule ID '{tok}' (expected exact rule ID like 'REF-04'; use --accept-substring for message text)"))
        else:
            accept_rules.add(t)

    for sub in raw_subs:
        s = sub.strip()
        if len(s) < 8:
            accept_errors.append(("--accept-substring", f"substring '{sub}' is too short (minimum 8 characters required)"))
        else:
            accept_substrings.append(s)

    report = Report(
        accept_rules=accept_rules,
        accept_substrings=accept_substrings,
        accept_fatal=bool(getattr(args, "accept_fatal", False)),
    )
    for where, msg in accept_errors:
        rule = "IO-01" if "does not exist" in msg else "IO-05"
        report.fail(rule, where, msg)
    if accept_errors:
        return report

    if not target.exists():
        report.fail("IO-01", str(target), "target path does not exist")
        return report

    manuscript, artifacts = discover_files(target, args, report)
    extra_fig_nums, extra_tab_nums = (check_figure_plan(artifacts["figure_plan"]) if "figure_plan" in artifacts else (set(), set()))
    if "figure_plan" in artifacts:
        report.note(f"Checked figure plan: {artifacts['figure_plan'].name}")

    manuscript_raw, manuscript_clean, numbered, fmt = "", "", [], "md"
    yaml_title, yaml_abs, docx_footnotes, docx_comments = "", "", [], []

    if manuscript is not None:
        fmt = detect_format(manuscript, args.format)
        if fmt == "docx":
            try:
                _, docx_footnotes, docx_comments, manuscript_raw = load_docx_structured(manuscript)
            except ValueError as exc:
                report.fail("IO-02", manuscript.name, str(exc))
                return report
            numbered = list(enumerate(manuscript_raw.splitlines(), 1))
            manuscript_clean = manuscript_raw
        elif fmt == "tex":
            manuscript_raw = expand_tex_inputs(manuscript)
            numbered = strip_tex_comments(manuscript_raw.splitlines())
            manuscript_clean = "\n".join(line for _, line in numbered)
        else:
            manuscript_raw = manuscript.read_text(encoding="utf-8", errors="replace")
            raw_lines = manuscript_raw.splitlines()
            yaml_title, yaml_abs, start_idx = extract_yaml_frontmatter(raw_lines)
            numbered, unclosed = strip_md_nonprose(raw_lines, start_idx)
            for start_ln, kind, skipped in unclosed:
                report.fail("IO-04", f"{manuscript.name}:{start_ln}", f"{kind} remains open at end of file ({skipped} line(s) hidden)")
            manuscript_clean = "\n".join(line for _, line in numbered)

    plan_meta = check_manuscript_plan(artifacts["plan"], manuscript_clean, report) if "plan" in artifacts else PlanMeta()
    if "plan" in artifacts:
        report.note(f"Checked manuscript plan: {artifacts['plan'].name}")

    if manuscript is not None:
        label = manuscript.name
        report.note(f"Checked manuscript ({fmt}, stage={args.stage}): {label}")
        check_placeholders(numbered, fmt, label, report, stage=args.stage)
        if docx_footnotes:
            check_placeholders(list(enumerate(docx_footnotes, 1)), "docx", f"{label}[footnotes]", report, stage=args.stage)
        if docx_comments:
            check_placeholders(list(enumerate(docx_comments, 1)), "docx", f"{label}[comments]", report, stage=args.stage, comments_only=True)

        if fmt == "tex":
            check_figures_and_tables_tex(numbered, label, report, extra_fig_nums, extra_tab_nums)
        else:
            check_figures_and_tables_md(numbered, fmt, label, report, extra_fig_nums, extra_tab_nums, base_dir=manuscript.parent)

        title_text, keypoints_text, abstract_text, top_level, body_secs = parse_manuscript_sections(
            numbered, fmt, yaml_title=yaml_title, yaml_abstract=yaml_abs
        )
        # Exclude Key Points and References/Bibliography from body drift comparison
        body_no_refs = "\n".join(
            line for title, _, body in body_secs
            if not normalize_heading(title).lower().startswith(("key points", "highlights", "references", "bibliography"))
            for _, line in body
        )
        check_frontmatter_body_numbers(title_text, keypoints_text, abstract_text, body_no_refs, label, report)

        eff_max_abs = args.max_abstract if args.max_abstract is not None else plan_meta.plan_max_abstract
        eff_max_words = args.max_words if args.max_words is not None else plan_meta.plan_max_words
        lim_threshold = 0.35 if plan_meta.is_clinical else 0.25
        total_words = check_budgets_and_limitations(
            abstract_text, top_level, body_secs, fmt, label, report,
            eff_max_abs, eff_max_words, plan_meta.section_budgets or None,
            lim_threshold=lim_threshold, style_mode=bool(args.style),
        )
        check_table_arithmetic(numbered, fmt, label, report)
        check_declarations_present(body_secs, total_words, label, report)
        if args.style:
            check_opt_in_style(numbered, body_secs, keypoints_text, abstract_text, fmt, label, plan_meta.is_observational, report)
        if "bib" in artifacts:
            if fmt == "docx":
                report.note(f"Skipped --bib key lookup on .docx ({artifacts['bib'].name}); checking only for unconverted literal [@key] tokens")
            else:
                check_citations_against_bib(numbered, fmt, artifacts["bib"], label, report)

    rebuttal_ids: list[str] = []
    if "review" in artifacts:
        check_adversarial_review(artifacts["review"], report)
        report.note(f"Checked adversarial review: {artifacts['review'].name}")
    if "rebuttal" in artifacts:
        rebuttal_ids = check_rebuttal_plan(artifacts["rebuttal"], report, stage=args.stage)
        report.note(f"Checked rebuttal plan: {artifacts['rebuttal'].name}")
    if manuscript is not None and "response" in artifacts:
        check_response_letter_quotes(artifacts["response"], manuscript_clean, report, rebuttal_ids=rebuttal_ids)

    if manuscript is None and not artifacts:
        report.fail("IO-03", str(target), "no manuscript or companion artifacts found")
    return report


def format_rules_table() -> str:
    lines = ["| Rule | Severity | Meaning |", "| --- | --- | --- |"]
    for rid, sev, desc in RULE_CATALOG:
        lines.append(f"| `{rid}` | {sev} | {desc} |")
    return "\n".join(lines)


def format_report(report: Report) -> str:
    if report.fails:
        status = "FAIL"
    elif report.warns:
        status = "PASS WITH WARNINGS"
    elif report.accepted:
        status = "PASS WITH ACCEPTED"
    else:
        status = "PASS"
    lines = ["# Manuscript Consistency Check", "", f"**Status:** {status} ({len(report.fails)} FAIL, {len(report.warns)} WARN" + (f", {len(report.accepted)} ACCEPTED" if report.accepted else "") + ")", ""]
    if report.notes:
        lines.extend(["## Summary", *(f"- {n}" for n in report.notes), ""])
    lines.append("## FAIL")
    lines.extend([*(f"- [FAIL:{f.rule}] {f.where}: {f.msg}" for f in report.fails)] if report.fails else ["- None."])
    lines.extend(["", "## WARN"])
    lines.extend([*(f"- [WARN:{w.rule}] {w.where}: {w.msg}" for w in report.warns)] if report.warns else ["- None."])
    if report.accepted:
        lines.extend(["", "## ACCEPTED", *(f"- [ACCEPTED:{a.rule}] {a.where}: {a.msg}" for a in report.accepted)])
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check manuscript and planning artifacts for consistency.")
    parser.add_argument("target", nargs="?", help="Manuscript file (.md, .docx, .tex) or project directory")
    parser.add_argument("--list-rules", action="store_true", help="Print authoritative rule-ID catalog and exit")
    parser.add_argument("--stage", choices=["draft", "submission"], default="submission")
    parser.add_argument("--accept", action="append", default=[], help="Exact rule ID to suppress (e.g. REF-04; repeatable)")
    parser.add_argument("--accept-substring", action="append", default=[], help="Message substring to suppress (min 8 chars; repeatable)")
    parser.add_argument("--accept-file", help="File with one accepted rule ID (or 'sub:TEXT') per line")
    parser.add_argument("--accept-fatal", action="store_true", help="Allow --accept on FATAL review gate rules (REV-*)")
    parser.add_argument("--style", action="store_true", help="Enable opt-in style/acronym/causal-verb warnings")
    parser.add_argument("--plan", help="Path to manuscript-plan.md or PLAN.md")
    parser.add_argument("--figure-plan", help="Path to figure-plan.md")
    parser.add_argument("--review", help="Path to adversarial-review.md")
    parser.add_argument("--rebuttal", help="Path to rebuttal-plan.md")
    parser.add_argument("--response", help="Path to response-letter.md (verifies quoted passages verbatim)")
    parser.add_argument("--bib", help="Checked refs JSON, zotero.json wrapper, .bib, or Better BibTeX CSL-JSON")
    parser.add_argument("--max-abstract", type=int)
    parser.add_argument("--max-words", type=int)
    parser.add_argument("--format", choices=["auto", "md", "tex", "docx"], default="auto")
    args = parser.parse_args(argv)

    if args.list_rules:
        print(format_rules_table())
        return 0
    if not args.target:
        parser.error("the following arguments are required: target")

    report = run_checks(Path(args.target), args)
    print(format_report(report))
    return 1 if report.fails else 0


if __name__ == "__main__":
    sys.exit(main())
