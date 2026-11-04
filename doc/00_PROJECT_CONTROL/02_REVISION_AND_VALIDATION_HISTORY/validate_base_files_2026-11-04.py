#!/usr/bin/env python3
"""Validate the algocore_system documentation package: the foundation set at Revision 3 or later, the approved folder
and file manifest, the Decision Register, the open-items table, the publication copies of the existing technical
records, and the security patterns of the publication set (Decision Register, D-05).

Usage (Python 3, standard library only; <root> is the folder that contains doc/):
  python3 validate_base_files_2026-11-04.py <root>                 local package: every folder, empty ones included
  python3 validate_base_files_2026-11-04.py --publication <root>   a Git checkout: folders without files may be absent
  python3 validate_base_files_2026-11-04.py --self-test <root>     positive and negative tests on temporary copies
Exit status: 0 = every check (or test) passed; 1 = at least one genuine failure; 2 = usage error.
Every check runs in isolation. An unexpected condition is reported as FAIL with its reason, never as a traceback.

Conventions checked (Revision 3 and later):
- A foundation document keeps its file name and its **Date:** line (its creation date) when it is revised.
- **Status:** <status> - Revision N, where <status> is one of the document statuses in Document 07, section 4.
- Revision numbers are review rounds. A document's status shows the last round that changed it. Its revision history
  names Revision 1, each later round that changed it and the current revision, in order, each with its date; the same
  revision number has the same date in every document.
- Document 10, section 11 has a Status column: OPEN, or CLOSED with the date and the decision (D-NN) that closed the
  item. An item is CLOSED if, and only if, a Decision Register entry closes it ("OI-NN: CLOSED" in its Status field).
- Nothing is kept private (Decision Register, D-08): the five existing technical records are public in their original
  form, beside their redacted copies, and the revision instructions, reviews and reports are in the history folder.
The scope and limits of the security-pattern checks are printed with every run (SECURITY_SCOPE below).
"""
import datetime
import hashlib
import re
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path

# ----------------------------------------------------------------------------------------------- approved manifest
FND = "doc/00_PROJECT_CONTROL/01_PROJECT_FOUNDATION"
HIS = "doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY"
GIT = "doc/00_PROJECT_CONTROL/03_GITHUB_AND_REPOSITORY_RECORDS"
REG = "doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS"
SRC = "doc/01_PRE_PHASE/01_SOURCE_INVENTORY"
REC = "doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS"
COP = REC + "/PUBLICATION_REDACTED_COPIES"
FOUNDATION = [
    "01_PROJECT_FOUNDATION_AND_SCOPE_2026-11-03.md",
    "02_PROJECT_PHASES_AND_MASTER_WORKFLOW_2026-11-03.md",
    "03_AI_ROLES_RESPONSIBILITIES_AND_OPERATING_INSTRUCTIONS_2026-11-03.md",
    "04_TOPIC_INVESTIGATION_WORKFLOW_AND_AI_CONTINUITY_PROTOCOL_2026-11-03.md",
    "05_PROJECT_GOVERNANCE_AND_DECISION_CONTROL_2026-11-03.md",
    "06_TECHNICAL_ENVIRONMENT_TOOLS_AND_RESEARCH_SOURCES_2026-11-03.md",
    "07_REPOSITORY_DOCUMENTATION_AND_RECORD_MANAGEMENT_2026-11-03.md",
    "08_LEGACY_STUDY_AND_AUDIT_METHODOLOGY_2026-11-03.md",
    "09_NEW_SYSTEM_DESIGN_AND_DEVELOPMENT_FRAMEWORK_2026-11-03.md",
    "10_MASTER_PROJECT_INDEX_AND_CONTROL_REGISTERS_2026-11-03.md",
]
RECORDS = ["01_SYSTEM_OVERVIEW.md", "02_REPOSITORY_AND_FILE_MAP.md", "03_STARTUP_RUNTIME_AND_SCHEDULER.md",
           "03A_CRON_REGISTRY_TABLE.md", "LEGACY_SYSTEM_MANUAL_INDEX.md"]
REGISTER = REG + "/DECISION_REGISTER_2026-11-04.md"
README = SRC + "/README.md"
OLD_VALIDATOR = HIS + "/validate_base_files_2026-11-03.py"
THIS_VALIDATOR = HIS + "/validate_base_files_2026-11-04.py"
ORIGINALS = [f"{REC}/{n}" for n in RECORDS]
COPIES = [f"{COP}/{n}" for n in RECORDS]

ROLE = {f"{FND}/{n}": "foundation" for n in FOUNDATION}
ROLE.update({f"{HIS}/BASE_FILES_REVISION_1_REPORT_2026-11-03.txt": "history",
             f"{HIS}/BASE_FILES_REVISION_2_REPORT_2026-11-03.txt": "history",
             f"{HIS}/BASE_FILES_REVISION_2_CORRECTION_REPORT_2026-11-03.txt": "history",
             OLD_VALIDATOR: "old_validator", THIS_VALIDATOR: "validator",
             f"{GIT}/GITHUB_ALGOCORE_SYSTEM_SETUP_RECORD_2026-11-03.txt": "history",
             REGISTER: "register", README: "note"})
ROLE.update({p: "original" for p in ORIGINALS})
ROLE.update({p: "copy" for p in COPIES})
HANDOFF = [  # revision instructions, reviews and reports kept in the history folder (Decision Register, D-08)
    "CLAUDE_OI01_FOLDER_SETUP_AND_FILE_STAGING_INSTRUCTION_2026-11-04.txt",
    "OI01_FOLDER_SETUP_AND_FILE_STAGING_REPORT_2026-11-04.txt",
    "CHATGPT_REVIEW_OI01_STAGING_PACKAGE_2026-11-04.txt",
    "CLAUDE_RESPONSE_TO_CHATGPT_OI01_REVIEW_2026-11-04.txt",
    "CHATGPT_SUPPLEMENTAL_REVIEW_CLAUDE_RESPONSE_AND_ZIP_2026-11-04.txt",
    "CLAUDE_CONSOLIDATED_OI01_FOUNDATION_CORRECTION_INSTRUCTION_2026-11-04.txt",
    "BASE_FILES_REVISION_3_CORRECTION_REPORT_2026-11-04.txt",
    "CLAUDE_REV3_REVIEW_GITHUB_WORKSPACE_INSTRUCTION_2026-11-04.txt",
]
ROLE.update({f"{HIS}/{n}": "history" for n in HANDOFF})
ROLE[f"{HIS}/BASE_FILES_REVISION_4_REPORT_2026-11-04.txt"] = "history"

EXPECTED_DIRS = sorted([
    "doc", "doc/00_PROJECT_CONTROL", FND, HIS, GIT, REG,
    "doc/01_PRE_PHASE", SRC, "doc/01_PRE_PHASE/02_WHOLE_SYSTEM_OVERVIEW", "doc/01_PRE_PHASE/03_OPERATIONAL_WORKFLOW",
    "doc/01_PRE_PHASE/04_MASTER_SYSTEM_INVESTIGATION_INDEX", "doc/01_PRE_PHASE/05_PHASE1_METHODOLOGY",
    "doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT", REC, COP, "doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION",
    "doc/03_PHASE2_NEW_SYSTEM_DESIGN", "doc/03_PHASE2_NEW_SYSTEM_DESIGN/DESIGN_TOPIC_DOCUMENTATION", "doc/99_ARCHIVE"])

# Files that must stay byte-for-byte unchanged (SHA-256).
PINNED = {
    f"{HIS}/BASE_FILES_REVISION_1_REPORT_2026-11-03.txt": "85d71849594242de25f31eb1a7d989338dbebdb33832ad987f67bbef689fe69b",
    f"{HIS}/BASE_FILES_REVISION_2_REPORT_2026-11-03.txt": "c96c29dce282b8e8b2d552b5eb3ecf1330e21b232c54763bf20500676b94c0aa",
    f"{HIS}/BASE_FILES_REVISION_2_CORRECTION_REPORT_2026-11-03.txt": "4ebf55f577db5999bf77de6cb612e13333ef7318efdb73d5ccdffe2d01f28a4d",
    OLD_VALIDATOR: "e9b30765e408be753f444e484b27747910fb8b2b102209f5813d5a41d566c563",
    f"{GIT}/GITHUB_ALGOCORE_SYSTEM_SETUP_RECORD_2026-11-03.txt": "8337e083afbd6454ee50bff99ee02ad5a9f0dbb959425fba4ede998cba464911",
    f"{REC}/01_SYSTEM_OVERVIEW.md": "51d5f315ba9a949f3807e5a68c6d48a46411b0e2eaeaaf9da1bf4693cb3283a9",
    f"{REC}/02_REPOSITORY_AND_FILE_MAP.md": "8b5aec74544c7a613ced958f90ca9deedb524db321ae7101b9a577015cbf6d49",
    f"{REC}/03_STARTUP_RUNTIME_AND_SCHEDULER.md": "f7d38f2d0f7ea2d61783970b1e8a81fc06d1676ab613ee4db18178ee5cbc3087",
    f"{REC}/03A_CRON_REGISTRY_TABLE.md": "85d0bd23f087f33f9ff1724469faa30893ac3a26fb138abc86c7bfa5e82ece3c",
    f"{REC}/LEGACY_SYSTEM_MANUAL_INDEX.md": "dfe1ac19890df8fffc450adb627b49fcebe73d8545c91ac5ff83448de46c3287",
    f"{HIS}/CLAUDE_OI01_FOLDER_SETUP_AND_FILE_STAGING_INSTRUCTION_2026-11-04.txt":
        "51d0a0882c72ab48340edfd46c3e12871cc58efbef37045c9daa8cc3033d2270",
    f"{HIS}/OI01_FOLDER_SETUP_AND_FILE_STAGING_REPORT_2026-11-04.txt":
        "7a4c7568d2a0f5845c926a89d4b34955d5f8b4c396f40ef48ab27217eccaaff6",
    f"{HIS}/CHATGPT_REVIEW_OI01_STAGING_PACKAGE_2026-11-04.txt":
        "c68faf464ce2d2f55d95e4d080a35d3c3b2b1ad4fad0176397b7a2b1539cafab",
    f"{HIS}/CLAUDE_RESPONSE_TO_CHATGPT_OI01_REVIEW_2026-11-04.txt":
        "3bb157411f52feff04dc10ca2a0e0e59a5b178a28ef37d7a8015b44a9c3e5391",
    f"{HIS}/CHATGPT_SUPPLEMENTAL_REVIEW_CLAUDE_RESPONSE_AND_ZIP_2026-11-04.txt":
        "c44de8f979c0d5ae195a73453e9bdda94d0202a47e0ccb0f11cd62c45bb60d2c",
    f"{HIS}/CLAUDE_CONSOLIDATED_OI01_FOUNDATION_CORRECTION_INSTRUCTION_2026-11-04.txt":
        "a22272ab5b1e50cd16a5d8560aa11477f9b1a0c787bd7dca9943c9bf4383c4b0",
    f"{HIS}/BASE_FILES_REVISION_3_CORRECTION_REPORT_2026-11-04.txt":
        "821a15ca03f5573533be1b61cfcc9e1237327ffa1ba0cccf4740df803652d925",
    f"{HIS}/CLAUDE_REV3_REVIEW_GITHUB_WORKSPACE_INSTRUCTION_2026-11-04.txt":
        "fa4e53fbdbed33cf4fcb049ba730f6ba70ee8367168c3aa7b7b19e94103baa51",
}

# Wording that must be gone once the open item is CLOSED in Document 10, section 11.
STALE = {
    "OI-01": [r"Who creates algocore_system is OPEN", r"Who creates the repository: OPEN",
              r"first folder layout \(OPEN FOR RAMA", r"Proposed folder layout for algocore_system",
              r"settled when the repository is created"],
    "OI-05": [r"Claude's working environment for this project: a new Claude Project, or new instructions"],
}
# Wording that must be gone once the decision is in the Decision Register (checked in the foundation documents and
# in the redaction notes of the copies).
STALE_BY_DECISION = {
    "D-08": [r"kept privately and (?:are|is) not published", r"only their publication copies are"],
}

# ---------------------------------------------------------------------------------- security patterns (general)
# An address may end a sentence, before a full stop; only a following digit, or a dot and a digit, extends the number.
IPV4 = re.compile(r"(?<!\d)(?<!\d\.)(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?!\.?\d)")
ACCOUNT_LIKE = re.compile(r"(?<![A-Za-z0-9_])[A-Z]{2,4}\d{3,6}(?![A-Za-z0-9_])")
ACCOUNT_LIKE_ALLOWED = re.compile(r"^(?:SHA(?:224|256|384|512)|ISO8601|RFC\d{3,5}|AES(?:128|192|256))$")
MACHINE_PATH = re.compile(r"/home/[A-Za-z0-9_.-]+|/Users/[A-Za-z0-9_.-]+|(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
CREDENTIAL = re.compile(r"(?i)\b(?:api[_ -]?key|api[_ -]?secret|secret|access[_ -]?token|token|password|passwd|totp)"
                        r"\b[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_+/=-]{12,})")
LONG_KEY = re.compile(r"(?<![A-Za-z0-9])(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[A-Za-z])[A-Za-z0-9]{32,}(?![A-Za-z0-9])")
HASH_HEX = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
KNOWN_SECRET = re.compile("|".join([
    r"gh[pousr]_[A-Za-z0-9]{36,}", r"github_pat_[A-Za-z0-9_]{20,}", r"AKIA[0-9A-Z]{16}", r"xox[abprs]-[A-Za-z0-9-]{10,}",
    r"(?<!\d)\d{8,10}:[A-Za-z0-9_-]{35}(?![A-Za-z0-9_-])", "-----BEGIN " + r"[A-Z ]*" + "PRIVATE KEY-----"]))
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
SESSION_MARKS = ["claude" + ".ai/code", "Claude" + "-Session"]
PLACEHOLDERS = {"ACCOUNT_ID_1_REDACTED": "account", "ACCOUNT_ID_2_REDACTED": "account",
                "PRODUCTION_VM_IP_REDACTED": "ip", "TEST_VM_IP_REDACTED": "ip"}
CATEGORY_TEXT = {"account": "trading-account identifier", "ip": "VM IP address"}
CATEGORY_RE = {"account": r"[A-Z]{2,4}\d{3,6}", "ip": IPV4.pattern}

SECURITY_SCOPE = """SECURITY-PATTERN CHECKS - SCOPE AND LIMITS
Scope: every file of the package, line by line. Nothing is kept private (D-08): the five original
technical records are public as they are, so S1 to S3 do not apply to them; their redacted copies are checked.
S1 IPv4 addresses (dotted quads of valid octets); loopback 127.x.x.x and 0.0.0.0 are allowed.
   Not covered: IPv6, host names, addresses written in other forms.
S2 tokens shaped like account identifiers: 2 to 4 capital letters followed by 3 to 6 digits, as a separate word.
   Allowed technical terms: SHA224/256/384/512, ISO8601, RFC numbers, AES128/192/256.
   Not covered: identifiers of other shapes (lower case, separators, other lengths).
S3 machine paths: home folders under /home or /Users, and a drive letter followed by a colon and a slash or backslash.
   Applies to project-control files only. The redacted copies keep their paths by decision (D-02); the 2026-11-03
   validator holds such paths as search patterns and is exempt (its content is pinned by SHA-256).
S4 credential-like assignments: api key, api secret, secret, access token, token, password, passwd or totp, then = or :,
   then a value of 12 or more key characters with both letters and digits.
   Not covered: secrets without such a key word, or shorter values.
S5 long key-like strings: 32 or more letters and digits, mixed; lower-case hexadecimal of 40 or 64 characters
   (git commit and SHA-256 hashes) is allowed.
S6 known secret formats: GitHub tokens, AWS access key IDs, Slack tokens, Telegram bot tokens, private-key blocks.
   Not covered: other providers' formats.
S7 e-mail addresses.
S8 Claude session links; the 2026-11-03 validator holds them as search strings and is exempt (content pinned).
S9 redacted copies: the redaction note, only the four allowed placeholders, their declared counts, the original's
   SHA-256, and a line-by-line comparison with the original in which only placeholder positions may differ, each
   by one value of the placeholder's category, used consistently in all copies.
These are pattern checks. A PASS means that no listed pattern was found; it does not prove that a file holds no
sensitive information. Values that the patterns do not describe can be found only by human review."""

STATUS_RE = re.compile(r"^\*\*Status:\*\* (?P<word>[A-Z][A-Z ]*?) — Revision (?P<rev>\d+)\b", re.M)
REVISION_RE = re.compile(r"^\*\*Status:\*\*[^\n]*?— Revision (\d+)\b", re.M)
DATE_RE = re.compile(r"^\*\*Date:\*\* (\d{4}-\d{2}-\d{2})$", re.M)
HISTORY_RE = re.compile(r"^\*\*Revision history:\*\*(.*)$", re.M)
ENTRY_RE = re.compile(r"Revision (\d+), (\d{4}-\d{2}-\d{2}):")
DREF_RE = re.compile(r"(?<![A-Za-z0-9-])D-(\d\d)(?!\d)")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def section(text, num):
    m = re.search(rf"^## {num}\. .*$", text, re.M)
    if not m:
        raise ValueError(f"section {num} not found")
    rest = text[m.end():]
    nxt = re.search(r"^## |^\*\*Related documents:\*\*", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def table(block):
    rows = [ln for ln in block.split("\n") if ln.startswith("|")]
    cells = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in rows]
    if len(cells) < 2:
        raise ValueError("table not found")
    return cells[0], cells[2:]


def iso_date(s):
    datetime.date.fromisoformat(s)
    return s


class Run:
    def __init__(self, root, publication):
        self.root, self.publication = Path(root), publication
        self.results, self.cache, self.sections, self.texts = [], {}, {}, {}

    def ok(self, cid, cond, msg):
        self.results.append((cid, bool(cond), msg))

    def guard(self, cid, fn):
        try:
            fn()
        except Exception as exc:  # report, never crash
            self.results.append((cid, False, f"{cid} check could not complete: {type(exc).__name__}: {exc}"))

    def read(self, rel):
        if rel not in self.cache:
            try:
                self.cache[rel] = (self.root / rel).read_bytes().decode("utf-8")
            except (OSError, UnicodeDecodeError):
                self.cache[rel] = None
        return self.cache[rel]

    def need(self, rel):
        t = self.read(rel)
        if t is None:
            raise FileNotFoundError(f"{rel} missing or not UTF-8")
        return t

    def expected_files(self):
        return sorted(ROLE)

    def publication_files(self):
        return sorted(ROLE)

    def register_entries(self):
        parts = re.split(r"^## (D-\d\d) — .*$", self.need(REGISTER), flags=re.M)
        entries = {}
        for i in range(1, len(parts), 2):
            head, rows = table(parts[i + 1])
            entries[parts[i]] = (head, rows)
        return entries


# ------------------------------------------------------------------------------------------------- manifest checks
def check_manifest(r):
    base = r.root / "doc"
    present_dirs = sorted(["doc"] + [p.relative_to(r.root).as_posix() for p in base.rglob("*") if p.is_dir()]) \
        if base.is_dir() else []
    files = sorted(p.relative_to(r.root).as_posix() for p in base.rglob("*") if p.is_file()) if base.is_dir() else []
    exp_files = r.expected_files()
    if r.publication:
        need_dirs = set()
        for f in exp_files:
            d = f.rsplit("/", 1)[0]
            while d:
                need_dirs.add(d)
                d = d.rsplit("/", 1)[0] if "/" in d else ""
    else:
        need_dirs = set(EXPECTED_DIRS)
    miss_d = sorted(need_dirs - set(present_dirs))
    extra_d = sorted(set(present_dirs) - set(EXPECTED_DIRS))
    r.ok("M1", not miss_d and not extra_d, f"M1 approved folders present ({len(present_dirs)} found), none unexpected"
         + (f"; missing {miss_d}" if miss_d else "") + (f"; unexpected {extra_d}" if extra_d else ""))
    miss_f = sorted(set(exp_files) - set(files))
    extra_f = sorted(set(files) - set(exp_files))
    r.ok("M2", not miss_f and not extra_f, f"M2 exactly the {len(exp_files)} expected files ({len(files)} found)"
         + (f"; missing {miss_f}" if miss_f else "") + (f"; unexpected {extra_f}" if extra_f else ""))


def check_pinned(r):
    bad = []
    for rel, h in PINNED.items():
        p = r.root / rel
        if not p.is_file() or sha256(p.read_bytes()) != h:
            bad.append(rel.split("/")[-1])
    what = (f"the {sum(1 for p in PINNED if ROLE[p] == 'history')} history records, the 2026-11-03 validator"
            " and the five originals")
    r.ok("M3", not bad, f"M3 {what} byte-for-byte unchanged (SHA-256)" + (f"; changed or missing: {bad}" if bad else ""))


def check_publication_guard(r):
    missing = [p.split("/", 3)[-1] for p in ORIGINALS + COPIES if not (r.root / p).is_file()]
    r.ok("M4", not missing, "M4 the five original technical records (public by decision D-08) and their five redacted"
         " copies are present" + (f"; missing: {missing}" if missing else ""))


def check_superseded(r):
    ids = set(r.register_entries())
    notes = "\n".join("\n".join((r.read(f"{COP}/{n}") or "").split("\n")[:5]) for n in RECORDS)
    scope = "\n".join(r.texts.values()) + "\n" + notes
    stale = [f"{d}: '{p}'" for d, pats in STALE_BY_DECISION.items() if d in ids for p in pats if re.search(p, scope)]
    r.ok("V10c", not stale, "V10c no wording left that a later decision superseded" + (f": {stale}" if stale else ""))


# ---------------------------------------------------------------------------------------- foundation documents
def load_foundation(r):
    names = sorted(p.name for p in (r.root / FND).glob("*.md")) if (r.root / FND).is_dir() else []
    r.ok("V1", names == sorted(FOUNDATION), f"V1 exactly the ten foundation documents present ({len(names)} .md files)")
    for n in FOUNDATION:
        t = r.read(f"{FND}/{n}")
        if t is not None:
            r.texts[n[:2]] = t


def allowed_statuses(r):
    words = set()
    try:
        words = set(re.findall(r"^\| ([A-Z][A-Z ]*[A-Z]) \|", section(r.texts["07"], 4), re.M))
    except Exception:
        pass
    return words or {"DRAFT", "UNDER REVIEW", "APPROVED", "SUPERSEDED"}


def fmt_ok(raw):
    t = raw.decode("utf-8")
    return (b"\r" not in raw and b"\t" not in raw and raw.endswith(b"\n") and not raw.endswith(b"\n\n")
            and not any(ln.endswith(" ") for ln in t.split("\n")))


def check_documents(r):
    allowed = allowed_statuses(r)
    for n in FOUNDATION:
        d = n[:2]
        if d not in r.texts:
            r.ok("V2", False, f"V2 {d} missing or not UTF-8")
            continue
        t = r.texts[d]

        def one(d=d, t=t, n=n):
            r.ok("V2", fmt_ok((r.root / FND / n).read_bytes()), f"V2 {d} UTF-8, LF only, no tabs, no trailing spaces, single final newline")
            st = STATUS_RE.search(t)
            dl = DATE_RE.search(t)
            fdate = re.search(r"_(\d{4}-\d{2}-\d{2})\.md$", n).group(1)
            problems = []
            if not t.split("\n")[0].startswith(f"# {d} — "):
                problems.append("title")
            if not st:
                problems.append("status line")
            elif st.group("word") not in allowed:
                problems.append(f"status '{st.group('word')}' is not one of {sorted(allowed)}")
            if not dl or dl.group(1) != fdate:
                problems.append("Date line differs from the file-name date")
            if not HISTORY_RE.search(t):
                problems.append("revision history")
            r.ok("V3", not problems, f"V3 {d} title, status (a Document 07 status, Revision N), Date line equal to the"
                 " file-name date, revision history" + (f": {problems}" if problems else ""))
            secs, nums = set(), []
            for line in t.split("\n"):
                m = re.match(r"^## (\d+)\. ", line)
                if m:
                    secs.add(m.group(1))
                    nums.append(int(m.group(1)))
                m = re.match(r"^### (\d+\.\d+) ", line)
                if m:
                    secs.add(m.group(1))
            r.sections[d] = secs
            r.ok("V4", nums == list(range(1, len(nums) + 1)), f"V4 {d} top-level sections numbered 1..{len(nums)} without gaps")
            r.ok("V5", "\\&" not in t and not re.search(r"\d\\\.", t), f"V5 {d} no leftover Markdown escapes")
            r.ok("V6", re.search(r"\*\*(?:Related documents|Mandatory cross-reference):\*\*", t) is not None,
                 f"V6 {d} has a related-documents line")
        r.guard("V2", one)


def resolve_refs(r, owner, t, own_sections=True):
    bad, count = [], 0
    for m in re.finditer(r"Document (\d\d), sections? ([\d.]+)(?: and ([\d.]+))?", t):
        for s in (m.group(2), m.group(3)):
            if s:
                count += 1
                if s.rstrip(".") not in r.sections.get(m.group(1), set()):
                    bad.append(f"{owner}: Document {m.group(1)}, section {s.rstrip('.')}")
    if own_sections:
        for m in re.finditer(r"(?<!Document \d\d, )(?<![\w,] )\bsection (\d+(?:\.\d+)?)\b", t):
            pre = t[max(0, m.start() - 20):m.start()]
            if re.search(r"Document \d\d, $", pre) or "sections" in pre[-10:]:
                continue
            count += 1
            if m.group(1) not in r.sections.get(owner, set()):
                bad.append(f"{owner}: own section {m.group(1)}")
    for m in re.finditer(r"\b(\d\d) §(\d+(?:\.\d+)?)(?: and §(\d+(?:\.\d+)?))?", t):
        for s in (m.group(2), m.group(3)):
            if s:
                count += 1
                if s not in r.sections.get(m.group(1), set()):
                    bad.append(f"{owner}: {m.group(1)} §{s}")
    return count, bad


def check_cross_references(r):
    ids = set(r.register_entries())
    bad, count = [], 0
    for d, t in r.texts.items():
        c, b = resolve_refs(r, d, t)
        count, bad = count + c, bad + b
        rel = re.search(r"\*\*(?:Related documents|Mandatory cross-reference):\*\*(.*)", t)
        for x in re.findall(r"\b(\d\d)\b", rel.group(1) if rel else ""):
            count += 1
            if x not in r.texts:
                bad.append(f"{d}: related document {x}")
    for rel_path, owner in ((REGISTER, "register"), (README, "README")):
        c, b = resolve_refs(r, owner, r.need(rel_path), own_sections=False)
        count, bad = count + c, bad + b
    for owner, t in list(r.texts.items()) + [("register", r.need(REGISTER)), ("README", r.need(README))]:
        for m in DREF_RE.finditer(t):
            count += 1
            if f"D-{m.group(1)}" not in ids:
                bad.append(f"{owner}: decision D-{m.group(1)} not in the Decision Register")
    r.ok("V7", not bad, f"V7 all {count} cross-references (documents, sections, decisions) resolve" + (f": {bad}" if bad else ""))


def check_terms(r):
    T = r.texts
    alltext = "\n".join(T.values())
    r.ok("V8", not re.search(r"sandbox|duplicate/sandbox|duplicate copy", alltext, re.I),
         "V8 no 'sandbox'/'duplicate copy' study method left (replaced by the read-only clone)")
    r.ok("V9", not re.search(r"algocore[ -]system|algocore_systems|AlgoCore", alltext), "V9 algocore_system spelled one way only")
    r.ok("V9b", len(re.findall(r"algocore_system", alltext)) >= 8, "V9b algocore_system named in the repository, publication and open-item sections")
    r.ok("V10", not re.search(r"visibility.*remains OPEN|strategy after Phase 1 remains OPEN", alltext), "V10 settled repository visibility no longer shown as OPEN")
    r.ok("V11", not re.search(r"Phase 0|Phase-1|Phase-2|Phase-3|Pre Phase|Prephase", alltext), "V11 phase names consistent (Pre-Phase, Phase 1, Phase 2, Phase 3)")
    labels = "RETAIN / REVISE / UPGRADE / REPLACE / REJECT / NEW"
    lab09 = re.findall(r"^- (RETAIN|REVISE|UPGRADE|REPLACE|REJECT|NEW)\.$", T["09"], re.M)
    r.ok("V12", labels in T["02"] and " / ".join(lab09) == labels, "V12 the six Phase 2 outcome labels identical in 02 section 4 and 09 section 2")
    ev04 = re.findall(r"^- (FACT|UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL|KNOWN DEFECT|OPEN QUESTION) —", T["04"], re.M)
    ev08 = re.findall(r"^- (FACT|UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL|KNOWN DEFECT|OPEN QUESTION)\.$", T["08"], re.M)
    r.ok("V13", ev04 == ev08 and len(ev04) == 6, "V13 the six evidence classifications identical in 04 section 6 and 08 section 7")
    seq = ["study", "audit", "reconciliation", "proposal", "retain", "freeze", "code"]
    r.ok("V14", all(s in section(T["01"], 5).lower() for s in seq), "V14 approved sequence complete in 01 section 5")
    r.ok("V15", all(s in section(T["02"], 1).lower() for s in seq), "V15 approved sequence mapped completely in 02 section 1")
    r.ok("V16", all("Document 04, section 5" in T[d] for d in ["01", "02", "03", "08", "09"])
         and "## 5. Intended and actual behaviour — the whole-system audit" in T["04"] and "### 5.1 The rule" in T["04"],
         "V16 intended-vs-actual whole-system audit rule stated once (04 section 5) and referenced from 01, 02, 03, 08, 09")
    s52 = T["04"].split("### 5.2")[1].split("### 5.3")[0]
    areas = ["signals", "capital", "order management", "alerts", "market data", "reconciliation", "kill switch", "failure and recovery"]
    r.ok("V17", "entire system" in s52 and "one illustration of the kind of problem, not its limit" in s52
         and all(a in s52 for a in areas) and "never limit the audit to configuration settings" in T["04"],
         "V17 audit rule scoped to the entire system (all areas and flows), stop-loss shown as one illustration only")
    narrow = [r"comparison of configured and documented", r"configured and documented behaviour with actual",
              r"Configured or documented value and its source", r"for every item in the topic", r"Comparing configured"]
    left = [p for p in narrow if re.search(p, alltext)]
    r.ok("V23", not left, "V23 no Revision 1 wording left that limits the audit to configuration items" + (f": {left}" if left else ""))
    r.ok("V18", "05-Oct-2026" in T["06"] and "Document 06, section 4.2" in T["04"] and "Document 06, section 4.2" in T["08"],
         "V18 runtime limitation stated once (06 section 4.2) and referenced from 04 and 08")
    r.ok("V19", "## 10. Review-round control" in T["05"], "V19 review-round control present (05 section 10)")


def open_items(r):
    head, rows = table(section(r.texts["10"], 11))
    if head != ["Ref", "Open item", "Where", "Decides", "Status"]:
        raise ValueError(f"unexpected columns {head}")
    return rows


def check_open_items(r):
    rows = open_items(r)
    entries = r.register_entries()
    closes = {}  # OI -> decision closing it, from the register's Status field
    for did, (_, rws) in entries.items():
        status = dict((x[0], x[1]) for x in rws if len(x) >= 2).get("Status", "")
        for oi in re.findall(r"\b(OI-\d\d): CLOSED\b", status):
            closes.setdefault(oi, []).append(did)
    problems, refs, opened, closed = [], [], [], []
    for cells in rows:
        if len(cells) != 5:
            problems.append(f"row with {len(cells)} cells")
            continue
        ref, status = cells[0], cells[4]
        if not re.fullmatch(r"OI-\d\d", ref):
            problems.append(f"bad reference {ref}")
        refs.append(ref)
        m = re.fullmatch(r"CLOSED, (\d{4}-\d{2}-\d{2}) \(Decision Register, (D-\d\d)\)(?:: .+)?", status)
        if status == "OPEN":
            opened.append(ref)
            if ref in closes:
                problems.append(f"{ref} is OPEN but {closes[ref]} closes it")
        elif m:
            closed.append(ref)
            did = m.group(2)
            if did not in entries:
                problems.append(f"{ref} cites {did}, which is not in the Decision Register")
            elif did not in closes.get(ref, []):
                problems.append(f"{ref} is CLOSED by {did}, but {did} does not close it")
            else:
                date = dict((x[0], x[1]) for x in entries[did][1] if len(x) >= 2).get("Date", "")
                if date != m.group(1):
                    problems.append(f"{ref} closure date differs from {did}'s Date")
        else:
            problems.append(f"{ref} status is neither OPEN nor CLOSED, <date> (Decision Register, D-NN)")
    dup = [x for x, c in Counter(refs).items() if c > 1]
    if dup:
        problems.append(f"duplicate references {dup}")
    for oi in closes:
        if oi not in refs:
            problems.append(f"{oi} is closed in the register but not listed in section 11")
    markers = {d: t.count("OPEN FOR RAMA") for d, t in sorted(r.texts.items()) if "OPEN FOR RAMA" in t}
    r.ok("V20", not problems, f"V20 open-items table in 10 section 11 agrees with the Decision Register: OPEN {opened},"
         f" CLOSED {closed}; OPEN FOR RAMA markers per file {markers}" + (f"; problems: {problems}" if problems else ""))
    stale = []
    alltext = "\n".join(r.texts.values())
    for oi in closed:
        stale += [f"{oi}: '{p}'" for p in STALE.get(oi, []) if re.search(p, alltext)]
    r.ok("V10b", not stale, "V10b no wording left that shows a CLOSED item as open or proposed" + (f": {stale}" if stale else ""))


def check_revisions(r):
    problems, round_dates = [], {}
    for d, t in sorted(r.texts.items()):
        m = REVISION_RE.search(t)
        h = HISTORY_RE.search(t)
        if not m or not h:
            problems.append(f"{d}: no revision in the status line" if not m else f"{d}: no revision history")
            continue
        rev = int(m.group(1))
        entries = [(int(a), b) for a, b in ENTRY_RE.findall(h.group(1))]
        nums, dates = [a for a, _ in entries], [b for _, b in entries]
        try:
            [iso_date(x) for x in dates]
        except ValueError:
            problems.append(f"{d}: invalid date in the revision history")
            continue
        if not entries or nums[0] != 1:
            problems.append(f"{d}: history does not start with Revision 1")
        elif nums != sorted(set(nums)):
            problems.append(f"{d}: revisions not in increasing order {nums}")
        elif nums[-1] != rev:
            problems.append(f"{d}: status Revision {rev}, history ends at Revision {nums[-1]}")
        if dates != sorted(dates):
            problems.append(f"{d}: revision dates not in order")
        created = DATE_RE.search(t)
        if created and dates and dates[0] < created.group(1):
            problems.append(f"{d}: a revision is dated before the document's date")
        for a, b in entries:
            round_dates.setdefault(a, set()).add(b)
    for a, ds in sorted(round_dates.items()):
        if len(ds) > 1:
            problems.append(f"Revision {a} has different dates {sorted(ds)}")
    t10 = r.texts.get("10", "")
    head = re.search(r"^## 11\. Open items at Revision (\d+)$", t10, re.M)
    rev10 = REVISION_RE.search(t10)
    if not head or not rev10 or head.group(1) != rev10.group(1):
        problems.append("10: section 11 heading revision differs from 10's status revision")
    r.ok("V24", not problems, "V24 revision histories follow the review-round convention, and 10 section 11's heading"
         " matches 10's revision" + (f": {problems}" if problems else ""))


# ------------------------------------------------------------------------------------ register and folder note
def check_register(r):
    fields = re.findall(r"^- (.+)\.$", section(r.texts["10"], 5), re.M)
    problems = [] if len(fields) == 9 else [f"Document 10, section 5 lists {len(fields)} fields, not nine"]
    t = r.need(REGISTER)
    for k in ("**Status:**", "**Date:**", "**Related documents:**"):
        if k not in t:
            problems.append(f"register header lacks {k}")
    entries = r.register_entries()
    if not entries:
        problems.append("no decisions found")
    if list(entries) != sorted(entries):
        problems.append("decision IDs not in order")
    for did, (head, rows) in entries.items():
        names = [x[0] for x in rows]
        if head != ["Field", "Entry"] or names != fields:
            problems.append(f"{did}: fields {names} differ from Document 10, section 5")
            continue
        vals = dict((x[0], x[1] if len(x) > 1 else "") for x in rows)
        if vals["Decision ID"] != did:
            problems.append(f"{did}: Decision ID cell says {vals['Decision ID']}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", vals["Date"]):
            problems.append(f"{did}: Date is not an ISO date")
        else:
            try:
                iso_date(vals["Date"])
            except ValueError:
                problems.append(f"{did}: Date is not a calendar date")
        empty = [k for k, v in vals.items() if not v]
        if empty:
            problems.append(f"{did}: empty fields {empty}")
    r.ok("R1", not problems, f"R1 Decision Register: {len(entries)} decisions, each with exactly the nine fields of"
         " Document 10, section 5" + (f"; problems: {problems}" if problems else ""))
    head, rows = table(section(r.texts["05"], 4))
    names05 = [x[0] for x in rows]
    r.ok("R2", names05 == fields, "R2 Document 05, section 4 uses the field names of Document 10, section 5"
         + ("" if names05 == fields else f": {names05}"))
    raws = [(rel, (r.root / rel).read_bytes()) for rel in (REGISTER, README)]
    badfmt = [rel.split("/")[-1] for rel, b in raws if not fmt_ok(b)]
    r.ok("R4", not badfmt, "R4 register and README: UTF-8, LF only, no tabs, no trailing spaces, single final newline"
         + (f": {badfmt}" if badfmt else ""))


def check_readme(r):
    t = r.need(README)
    others = sorted(p.name for p in (r.root / SRC).iterdir() if p.name != "README.md")
    r.ok("R3", "NOT the authoritative Source Inventory" in t and f"{REG}/" in t and not others,
         "R3 Pre-Phase source-inventory folder holds only its README, which names the one authoritative register"
         + (f"; other files: {others}" if others else ""))


# ----------------------------------------------------------------------------------------------- security checks
def check_security(r):
    hits = {k: [] for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8")}
    unreadable = []
    for rel in r.publication_files():
        t = r.read(rel)
        if t is None:
            if (r.root / rel).exists():
                unreadable.append(rel)
            continue
        role, short = ROLE[rel], rel.replace("doc/", "", 1)
        for i, line in enumerate(t.split("\n"), 1):
            where = f"{short}:{i}"
            public_as_is = role == "original"  # D-08: the originals are published as they are
            if not public_as_is and any(not (m.group(0).startswith("127.") or m.group(0) == "0.0.0.0")
                                        for m in IPV4.finditer(line)):
                hits["S1"].append(where)
            if not public_as_is and any(not ACCOUNT_LIKE_ALLOWED.match(m.group(0)) for m in ACCOUNT_LIKE.finditer(line)):
                hits["S2"].append(where)
            if role not in ("copy", "old_validator", "original") and MACHINE_PATH.search(line):
                hits["S3"].append(where)
            if any(re.search(r"[A-Za-z]", m.group(1)) and re.search(r"\d", m.group(1)) for m in CREDENTIAL.finditer(line)):
                hits["S4"].append(where)
            if any(not HASH_HEX.match(m.group(0)) for m in LONG_KEY.finditer(line)):
                hits["S5"].append(where)
            if KNOWN_SECRET.search(line):
                hits["S6"].append(where)
            if EMAIL.search(line):
                hits["S7"].append(where)
            if role != "old_validator" and any(s in line for s in SESSION_MARKS):
                hits["S8"].append(where)
    r.ok("S0", not unreadable, "S0 every file is readable as UTF-8 text" + (f": {unreadable}" if unreadable else ""))
    names = {"S1": "no IPv4 address other than loopback", "S2": "no token shaped like an account identifier",
             "S3": "no machine path in project-control files", "S4": "no credential-like assignment",
             "S5": "no long key-like string other than commit or SHA-256 hashes", "S6": "no known secret format",
             "S7": "no e-mail address", "S8": "no Claude session link"}
    for k, desc in names.items():
        locs = hits[k]
        r.ok(k, not locs, f"{k} {desc} (exemptions: see the scope below)" + (f": {locs[:20]}" if locs else ""))


def check_copies(r):
    problems, values = [], {}
    for n in RECORDS:
        t = r.read(f"{COP}/{n}")
        if t is None:
            problems.append(f"{n}: copy missing")
            continue
        lines = t.split("\n")
        note, body = lines[:6], lines[6:]
        if not (note[0].startswith("> **PUBLICATION COPY") and "(Decision Register, D-02)" in note[0]
                and note[1].startswith("> Masked categories: ") and note[2].startswith("> Placeholders: ")
                and note[5] == ""):
            problems.append(f"{n}: redaction note missing or malformed")
            continue
        declared = {k: int(c) for k, c in re.findall(r"`\[([A-Z0-9_]+)\]` \((\d+)\)", note[2])}
        if not declared and note[2] != "> Placeholders: none.":
            problems.append(f"{n}: placeholder line not understood")
        used = Counter(re.findall(r"\[([A-Z0-9_]+_REDACTED)\]", "\n".join(body)))
        unknown = sorted(set(used) - set(PLACEHOLDERS))
        if unknown:
            problems.append(f"{n}: unknown placeholders {unknown}")
        if dict(used) != declared:
            problems.append(f"{n}: placeholders used {dict(used)} differ from the note {declared}")
        for k in used:
            if k in PLACEHOLDERS and CATEGORY_TEXT[PLACEHOLDERS[k]] not in note[1]:
                problems.append(f"{n}: category of {k} not named in the note")
        m = re.search(r"SHA-256 of the unchanged original: `([0-9a-f]{64})`", note[4])
        if not m or m.group(1) != PINNED[f"{REC}/{n}"]:
            problems.append(f"{n}: the note's SHA-256 is not the original's")
        orig = r.read(f"{REC}/{n}")
        if orig is None:
            continue
        olines = orig.split("\n")
        if len(olines) != len(body):
            problems.append(f"{n}: copy body has {len(body)} lines, original {len(olines)}")
            continue
        for i, (b, o) in enumerate(zip(body, olines)):
            if b == o:
                continue
            labels = re.findall(r"\[([A-Z0-9_]+_REDACTED)\]", b)
            if not labels or any(k not in PLACEHOLDERS for k in labels):
                problems.append(f"{n}: line {i + 7} differs from the original without a placeholder")
                continue
            pat = re.split(r"\[(?:[A-Z0-9_]+_REDACTED)\]", b)
            rx = "".join(re.escape(p) + (f"({CATEGORY_RE[PLACEHOLDERS[labels[j]]]})" if j < len(labels) else "")
                         for j, p in enumerate(pat))
            mm = re.fullmatch(rx, o)
            if not mm:
                problems.append(f"{n}: line {i + 7} differs from the original beyond its placeholders")
                continue
            for j, k in enumerate(labels):
                values.setdefault(k, set()).add(mm.group(j + 1))
    if any(len(v) != 1 for v in values.values()):
        problems.append("a placeholder stands for more than one value")
    flat = [next(iter(v)) for v in values.values() if len(v) == 1]
    if len(flat) != len(set(flat)):
        problems.append("two placeholders stand for the same value")
    for n in RECORDS:
        t = r.read(f"{COP}/{n}") or ""
        for v in flat:
            if re.search(rf"(?<![A-Za-z0-9_.]){re.escape(v)}(?![A-Za-z0-9_])", t):
                problems.append(f"{n}: a masked value is still present")
    r.ok("S9", not problems, "S9 redacted copies: redaction note, allowed placeholders and counts, original SHA-256,"
         " line-by-line match with the originals, one value per placeholder" + (f"; problems: {problems}" if problems else ""))


# ------------------------------------------------------------------------------------------------------- runner
def run_all(root, publication):
    r = Run(root, publication)
    r.guard("M1", lambda: check_manifest(r))
    r.guard("M3", lambda: check_pinned(r))
    r.guard("M4", lambda: check_publication_guard(r))
    r.guard("V1", lambda: load_foundation(r))
    r.guard("V2", lambda: check_documents(r))
    r.guard("V7", lambda: check_cross_references(r))
    r.guard("V8", lambda: check_terms(r))
    r.guard("V20", lambda: check_open_items(r))
    r.guard("V10c", lambda: check_superseded(r))
    r.guard("V24", lambda: check_revisions(r))
    r.guard("R1", lambda: check_register(r))
    r.guard("R3", lambda: check_readme(r))
    r.guard("S0", lambda: check_security(r))
    r.guard("S9", lambda: check_copies(r))
    return r


def report(r):
    print(f"VALIDATION OF {r.root} (mode: {'Git checkout (--publication)' if r.publication else 'local package'})")
    for _, good, msg in r.results:
        print(("PASS " if good else "FAIL ") + msg)
    print("\n" + SECURITY_SCOPE)
    fails = sum(1 for _, g, _ in r.results if not g)
    print(f"\nCHECKS RUN: {len(r.results)}")
    print(f"\nRESULT: {'PASS' if not fails else 'FAIL'} ({fails} failed)")
    return 0 if not fails else 1


# ---------------------------------------------------------------------------------------------------- self-tests
DOC_IP = ".".join(["192", "0", "2", "10"])            # documentation address range (RFC 5737), not a real host
FAKE_ID = "ABC" + "123"
FAKE_PATH = "/ho" + "me/someone/notes"
FAKE_TOKEN = "gh" + "p_" + "A" * 36
FAKE_MAIL = "someone" + "@" + "example.com"
FAKE_LINK = "https://" + "claude" + ".ai/code/" + "session_" + "x" * 12
FAKE_CRED = "pass" + "word = " + "Abcdef" + "123456789"
F = {d: f"{FND}/{n}" for d, n in ((n[:2], n) for n in FOUNDATION)}
TAIL = "\n**Related documents:**"


def edit(root, rel, old, new, regex=False, count=1):
    p = Path(root) / rel
    t = p.read_text(encoding="utf-8")
    if regex:
        t2, k = re.subn(old, new, t, count=count, flags=re.M)
    else:
        k = t.count(old)
        t2 = t.replace(old, new, count)
    if not k:
        raise LookupError(f"self-test target not found in {rel}")
    p.write_text(t2, encoding="utf-8")


def append(root, rel, s):
    with (Path(root) / rel).open("a", encoding="utf-8") as fh:
        fh.write(s)


def next_revision(root, rel):
    """Move one document to the revision after the highest one in use, with a matching history entry."""
    top = max(int(a) for n in FOUNDATION for a, _ in ENTRY_RE.findall((Path(root) / FND / n).read_text(encoding="utf-8")))
    edit(root, rel, r"(^\*\*Status:\*\*[^\n]*?— Revision )\d+", rf"\g<1>{top + 1}", regex=True)
    edit(root, rel, r"(^\*\*Revision history:\*\*.*)$", rf"\1 Revision {top + 1}, 2099-01-01: self-test.", regex=True)


def edit_line(root, rel, index, suffix):
    p = Path(root) / rel
    lines = p.read_text(encoding="utf-8").split("\n")
    lines[index] += suffix
    p.write_text("\n".join(lines), encoding="utf-8")


D06 = ("## D-06 — Self-test closure\n\n| Field | Entry |\n|---|---|\n| Decision ID | D-06 |\n| Date | 2026-11-05 |\n"
       "| Subject | Self-test |\n| Exact decision | Self-test. |\n| Rationale | Self-test. |\n| Evidence | Self-test. |\n"
       "| Rama approval | Self-test. |\n| Affected documents | 09 §2; 10 §11 (OI-06). |\n"
       "| Status | APPROVED. OI-06: CLOSED (Document 10, section 11). |\n\n**Related documents:**")

TESTS = [
    # (id, kind, description, publication mode, mutation, check IDs that must fail; empty = the run must pass)
    ("T01", "positive", "the package as it stands passes", False, lambda d: None, []),
    ("T02", "revision", "status at Revision 4 without a history entry fails", False,
     lambda d: edit(d, F["05"], "**Status:** DRAFT — Revision 3,", "**Status:** DRAFT — Revision 4,"), ["V24"]),
    ("T03", "revision", "the next revision with its own history entry passes", False,
     lambda d: next_revision(d, F["09"]), []),
    ("T04", "revision", "one revision number with two different dates fails", False,
     lambda d: edit(d, F["02"], "Revision 3, 2026-11-04:", "Revision 3, 2026-11-05:"), ["V24"]),
    ("T05", "revision", "section 11 heading at another revision than Document 10 fails", False,
     lambda d: edit(d, F["10"], "## 11. Open items at Revision 3", "## 11. Open items at Revision 2"), ["V24"]),
    ("T06", "revision", "Date line different from the file-name date fails", False,
     lambda d: edit(d, F["07"], "**Date:** 2026-11-03", "**Date:** 2026-11-04"), ["V3"]),
    ("T07", "status", "status APPROVED is accepted", False,
     lambda d: edit(d, F["01"], "**Status:** DRAFT — Revision 2", "**Status:** APPROVED — Revision 2"), []),
    ("T08", "status", "a status outside Document 07, section 4 fails cleanly", False,
     lambda d: edit(d, F["01"], "**Status:** DRAFT — Revision 2", "**Status:** FINAL — Revision 2"), ["V3"]),
    ("T09", "status", "a missing status line fails cleanly, without a crash", False,
     lambda d: edit(d, F["03"], r"^\*\*Status:\*\*.*\n", "", regex=True), ["V3", "V24"]),
    ("T10", "open item", "closing OI-02 without a decision that closes it fails", False,
     lambda d: edit(d, F["10"], "| 06 §3 | Rama | OPEN |", "| 06 §3 | Rama | CLOSED, 2026-11-04 (Decision Register, D-01): self-test |"), ["V20"]),
    ("T11", "open item", "reopening OI-01 while D-01 closes it fails", False,
     lambda d: edit(d, F["10"], r"\| CLOSED, 2026-11-04 \(Decision Register, D-01\)[^|]*\|", "| OPEN |", regex=True), ["V20"]),
    ("T12", "open item", "stale open wording for a closed item fails", False,
     lambda d: edit(d, F["07"], "Rama created algocore_system on 03-Nov-2026 (Decision Register, D-01).",
                    "Who creates algocore_system is OPEN FOR RAMA."), ["V10b"]),
    ("T13", "open item", "closing OI-06 with a matching new decision passes", False,
     lambda d: (edit(d, REGISTER, "**Related documents:**", D06),
                edit(d, F["10"], "| 09 §2 | Rama | OPEN |", "| 09 §2 | Rama | CLOSED, 2026-11-05 (Decision Register, D-06): self-test |")), []),
    ("T14", "open item", "an added open item passes (no fixed number of rows)", False,
     lambda d: edit(d, F["10"], "| 07 §5 | ChatGPT proposes (Claude if ChatGPT does not); Rama | OPEN |",
                    "| 07 §5 | ChatGPT proposes (Claude if ChatGPT does not); Rama | OPEN |\n| OI-08 | Self-test item | 09 §2 | Rama | OPEN |"), []),
    ("T15", "register", "a decision without the Rationale field fails", False,
     lambda d: edit(d, REGISTER, r"^\| Rationale \| Document 02, section 2 makes.*\n", "", regex=True), ["R1"]),
    ("T16", "register", "Document 05 with an old field name fails", False,
     lambda d: edit(d, F["05"], "|Rationale|Supporting rationale|", "|Reason|Supporting rationale|"), ["R2"]),
    ("T17", "security", "an IPv4 address in a foundation document fails", False,
     lambda d: edit(d, F["08"], "## 10. Runtime evidence\n", f"## 10. Runtime evidence\n\nSelf-test address {DOC_IP}.\n"), ["S1"]),
    ("T18", "security", "an account-shaped token in a publication copy fails", False,
     lambda d: edit_line(d, f"{COP}/03A_CRON_REGISTRY_TABLE.md", 6, f" {FAKE_ID}"), ["S2", "S9"]),
    ("T19", "security", "a machine path in the Decision Register fails", False,
     lambda d: edit(d, REGISTER, "**Related documents:**", f"{FAKE_PATH}\n\n**Related documents:**"), ["S3"]),
    ("T20", "security", "a token in a known secret format fails", False,
     lambda d: edit(d, README, "**Related documents:**", f"{FAKE_TOKEN}\n\n**Related documents:**"), ["S6"]),
    ("T21", "security", "an e-mail address fails", False,
     lambda d: edit(d, README, "**Related documents:**", f"{FAKE_MAIL}\n\n**Related documents:**"), ["S7"]),
    ("T22", "security", "a Claude session link fails", False,
     lambda d: edit(d, F["09"], TAIL, f"\n{FAKE_LINK}\n{TAIL}"), ["S8"]),
    ("T23", "security", "a credential-like assignment fails", False,
     lambda d: edit(d, F["09"], TAIL, f"\n`{FAKE_CRED}`\n{TAIL}"), ["S4"]),
    ("T24", "security", "loopback address and the term SHA256 pass (no false positive)", False,
     lambda d: edit(d, F["09"], TAIL, "\nLoopback 127.0.0.1 and the term SHA256 are allowed.\n" + TAIL), []),
    ("T25", "security", "an unknown placeholder in a copy fails", False,
     lambda d: edit(d, f"{COP}/01_SYSTEM_OVERVIEW.md", "[TEST_VM_IP_REDACTED]", "[TEST_VM_IP_3_REDACTED]"), ["S9"]),
    ("T26", "security", "a wrong original SHA-256 in a redaction note fails", False,
     lambda d: edit(d, f"{COP}/02_REPOSITORY_AND_FILE_MAP.md", "`8b5aec7", "`0b5aec7"), ["S9"]),
    ("T27", "security", "a changed line in a copy fails", False,
     lambda d: edit_line(d, f"{COP}/03_STARTUP_RUNTIME_AND_SCHEDULER.md", 8, " (edited)"), ["S9"]),
    ("T28", "security", "a placeholder replaced by an address fails", False,
     lambda d: edit(d, f"{COP}/01_SYSTEM_OVERVIEW.md", "[TEST_VM_IP_REDACTED]", DOC_IP), ["S1", "S9"]),
    ("T29", "manifest", "a changed original fails", False,
     lambda d: append(d, f"{REC}/03A_CRON_REGISTRY_TABLE.md", "x"), ["M3"]),
    ("T30", "manifest", "an unexpected extra file fails", False,
     lambda d: (Path(d) / "doc/99_ARCHIVE/extra.txt").write_text("extra\n", encoding="utf-8"), ["M2"]),
    ("T31", "manifest", "a missing foundation document fails cleanly", False,
     lambda d: (Path(d) / F["04"]).unlink(), ["M2", "V1"]),
    ("T32", "publication", "a Git checkout without the empty folders passes in --publication mode", True,
     lambda d: [p.rmdir() for p in sorted((Path(d) / "doc").rglob("*"), reverse=True) if p.is_dir() and not any(p.iterdir())], []),
    ("T33", "manifest", "a missing original technical record fails (they are public by D-08)", False,
     lambda d: (Path(d) / ORIGINALS[0]).unlink(), ["M2", "M4"]),
]


def self_test(root):
    print(f"SELF-TESTS ON TEMPORARY COPIES OF {root}")
    passed = 0
    for tid, kind, desc, pub, mutate, must_fail in TESTS:
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "pkg"
            shutil.copytree(root, dst)
            try:
                mutate(dst)
                r = run_all(dst, pub)
                failed = {cid for cid, good, _ in r.results if not good}
                crashed = [m for _, g, m in r.results if "could not complete" in m and not g]
                if must_fail:
                    good = set(must_fail) <= failed
                    detail = f"failed as expected: {sorted(set(must_fail))}" if good else f"expected failures {must_fail}, got {sorted(failed)}"
                else:
                    good = not failed
                    detail = "passed as expected" if good else f"unexpected failures {sorted(failed)}"
                if must_fail and crashed and tid not in ("T31",):
                    detail += f"; note: {len(crashed)} check(s) could not complete"
            except Exception as exc:
                good, detail = False, f"test could not run: {type(exc).__name__}: {exc}"
        passed += good
        print(f"{'PASS' if good else 'FAIL'} {tid} [{kind}] {desc} - {detail}")
    print(f"\nSELF-TESTS RUN: {len(TESTS)}; PASSED: {passed}; FAILED: {len(TESTS) - passed}")
    return 0 if passed == len(TESTS) else 1


def main(argv):
    args = list(argv)
    mode = args.pop(0) if args and args[0] in ("--publication", "--self-test") else ""
    if len(args) != 1 or not (Path(args[0]) / "doc").is_dir():
        print(__doc__.split("Conventions")[0].strip())
        print("\nUSAGE ERROR: give one folder that contains doc/.")
        return 2
    if mode == "--self-test":
        return self_test(Path(args[0]))
    return report(run_all(Path(args[0]), mode == "--publication"))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
