#!/usr/bin/env python3
"""Validate an algocore_system working tree (Document 07, section 6.5): the folder layout and the naming and placement
rules of Document 07, sections 3 and 5; the pinned historical records; the foundation set at Revision 5 or later; the
Decision Register and the open-items table; and the security patterns of every file under doc/.

validate_base_files_2026-11-04.py stays unchanged as the validator of the Revision 4 baseline. This script has no
fixed file list: new working records may be added in the approved folders, under the naming rules, without a new
version of the script. Empty folders are never required, because Git does not keep them; approved folders that are
absent are listed as a note.

Change of 2026-11-04, after the foundation approval (Decision Register, D-19): self-tests T02, T07 and T08 find a
document's status line by pattern instead of by the word DRAFT, so they run whatever the status is. No check of a
working tree changed.

Usage (Python 3, standard library only; <root> is the folder that contains doc/):
  python3 validate_algocore_workspace_2026-11-04.py <root>              a working tree: a local copy or a Git checkout
  python3 validate_algocore_workspace_2026-11-04.py --baseline <root>   as above, and exactly the files of the
                                                                        Revision 5 foundation baseline
  python3 validate_algocore_workspace_2026-11-04.py --self-test <root>  positive and negative tests on temporary copies
Exit status: 0 = every check (or test) passed; 1 = at least one genuine failure; 2 = usage error.
Every check runs in isolation. An unexpected condition is reported as FAIL with its reason, never as a traceback.

Conventions checked:
- A foundation document keeps its file name and its **Date:** line (its creation date) when it is revised.
- **Status:** <status> - Revision N, where <status> is one of the document statuses in Document 07, section 4.
- Revision numbers are review rounds. A document's status shows the last round that changed it. Its revision history
  names Revision 1, each later round that changed it and the current revision, in order, each with its date; the same
  revision number has the same date in every document.
- Document 10, section 11 has a Status column: OPEN, or CLOSED with the date and the decision (D-NN) that closed the
  item. An item is CLOSED if, and only if, a Decision Register entry closes it ("OI-NN: CLOSED" in its Status field).
- Files: the ten foundation documents only in their folder; the five existing technical records only in theirs (their
  redacted copies were removed as duplicates, D-18); elsewhere, names of the form <FILE_NAME>_YYYY-MM-DD.<type> or README.md, in an
  approved folder or below an open folder (Phase 1 topics, design topics, archive); nothing outside doc/; and no
  standalone AI instruction, review or response file (Document 07, section 3, the retention rule).
- The Revision 5 decisions: one commit and approval rule (Document 07, section 6), ChatGPT's review and Rama's
  explicit approval at every gate (Document 02, section 6), the ignored repositories, the register governance
  (Document 05, section 11.1) and the two index names (Document 10, section 1).
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

# ------------------------------------------------------------------------------------------- folders and files
FND = "doc/00_PROJECT_CONTROL/01_PROJECT_FOUNDATION"
HIS = "doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY"
GIT = "doc/00_PROJECT_CONTROL/03_GITHUB_AND_REPOSITORY_RECORDS"
REG = "doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS"
SRC = "doc/01_PRE_PHASE/01_SOURCE_INVENTORY"
REC = "doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS"
TOPICS = "doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION"
DESIGN = "doc/03_PHASE2_NEW_SYSTEM_DESIGN/DESIGN_TOPIC_DOCUMENTATION"
ARCHIVE = "doc/99_ARCHIVE"
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
BASE_VALIDATOR = HIS + "/validate_base_files_2026-11-04.py"
THIS_VALIDATOR = HIS + "/validate_algocore_workspace_2026-11-04.py"
SETUP_RECORD = GIT + "/GITHUB_ALGOCORE_SYSTEM_SETUP_RECORD_2026-11-03.txt"
ORIGINALS = [f"{REC}/{n}" for n in RECORDS]

# Approved folders (Document 07, section 3). Below the three open folders, subfolders may be added: one per Phase 1
# topic, one per design topic, and the archive's own structure. Folders without files may be absent.
APPROVED_DIRS = sorted([
    "doc", "doc/00_PROJECT_CONTROL", FND, HIS, GIT, REG,
    "doc/01_PRE_PHASE", SRC, "doc/01_PRE_PHASE/02_WHOLE_SYSTEM_OVERVIEW", "doc/01_PRE_PHASE/03_OPERATIONAL_WORKFLOW",
    "doc/01_PRE_PHASE/04_MASTER_SYSTEM_INVESTIGATION_INDEX", "doc/01_PRE_PHASE/05_PHASE1_METHODOLOGY",
    "doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT", REC, TOPICS, "doc/03_PHASE2_NEW_SYSTEM_DESIGN", DESIGN, ARCHIVE])
OPEN_DIRS = [TOPICS, DESIGN, ARCHIVE]
CONTAINERS = ["doc", "doc/00_PROJECT_CONTROL", "doc/01_PRE_PHASE", "doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT",
              "doc/03_PHASE2_NEW_SYSTEM_DESIGN"]  # these hold folders, and at most a README.md
TEXT_TYPES = ["md", "txt", "py", "csv", "json", "yaml", "yml"]
DATED_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*_(\d{4}-\d{2}-\d{2})\.(?:" + "|".join(TEXT_TYPES) + r")$")

HISTORY = [  # the change report of each revision round (Document 07, section 3; Decision Register, D-17)
    "BASE_FILES_REVISION_1_REPORT_2026-11-03.txt",
    "BASE_FILES_REVISION_2_REPORT_2026-11-03.txt",
    "BASE_FILES_REVISION_2_CORRECTION_REPORT_2026-11-03.txt",
    "BASE_FILES_REVISION_3_CORRECTION_REPORT_2026-11-04.txt",
    "BASE_FILES_REVISION_4_REPORT_2026-11-04.txt",
    "BASE_FILES_REVISION_5_REPORT_2026-11-04.txt",
]
# Roles of the known files. Any other file is a working record ("record"), checked like the project-control files.
ROLE = {f"{FND}/{n}": "foundation" for n in FOUNDATION}
ROLE.update({f"{HIS}/{n}": "history" for n in HISTORY})
ROLE.update({OLD_VALIDATOR: "old_validator", BASE_VALIDATOR: "validator", THIS_VALIDATOR: "validator",
             SETUP_RECORD: "history", REGISTER: "register", README: "note"})
ROLE.update({p: "original" for p in ORIGINALS})

# Files every working tree must hold. The Revision 5 foundation baseline (--baseline) is exactly the same set.
REQUIRED = sorted(ROLE)
BASELINE_FILES = list(REQUIRED)

# Files that must stay byte-for-byte unchanged (SHA-256). The Revision 5 report is not pinned: it records this
# script's own SHA-256. Instructions, reviews and responses are not kept at all (Decision Register, D-17).
PINNED = {
    f"{HIS}/BASE_FILES_REVISION_1_REPORT_2026-11-03.txt": "85d71849594242de25f31eb1a7d989338dbebdb33832ad987f67bbef689fe69b",
    f"{HIS}/BASE_FILES_REVISION_2_REPORT_2026-11-03.txt": "c96c29dce282b8e8b2d552b5eb3ecf1330e21b232c54763bf20500676b94c0aa",
    f"{HIS}/BASE_FILES_REVISION_2_CORRECTION_REPORT_2026-11-03.txt": "4ebf55f577db5999bf77de6cb612e13333ef7318efdb73d5ccdffe2d01f28a4d",
    OLD_VALIDATOR: "e9b30765e408be753f444e484b27747910fb8b2b102209f5813d5a41d566c563",
    BASE_VALIDATOR: "368dc0fe8ea4e1471aa6a20e38d9cd05038eb1ee983e4e249c34c6bafb991e43",
    SETUP_RECORD: "8337e083afbd6454ee50bff99ee02ad5a9f0dbb959425fba4ede998cba464911",
    f"{REC}/01_SYSTEM_OVERVIEW.md": "51d5f315ba9a949f3807e5a68c6d48a46411b0e2eaeaaf9da1bf4693cb3283a9",
    f"{REC}/02_REPOSITORY_AND_FILE_MAP.md": "8b5aec74544c7a613ced958f90ca9deedb524db321ae7101b9a577015cbf6d49",
    f"{REC}/03_STARTUP_RUNTIME_AND_SCHEDULER.md": "f7d38f2d0f7ea2d61783970b1e8a81fc06d1676ab613ee4db18178ee5cbc3087",
    f"{REC}/03A_CRON_REGISTRY_TABLE.md": "85d0bd23f087f33f9ff1724469faa30893ac3a26fb138abc86c7bfa5e82ece3c",
    f"{REC}/LEGACY_SYSTEM_MANUAL_INDEX.md": "dfe1ac19890df8fffc450adb627b49fcebe73d8545c91ac5ff83448de46c3287",
    f"{HIS}/BASE_FILES_REVISION_3_CORRECTION_REPORT_2026-11-04.txt":
        "821a15ca03f5573533be1b61cfcc9e1237327ffa1ba0cccf4740df803652d925",
    f"{HIS}/BASE_FILES_REVISION_4_REPORT_2026-11-04.txt":
        "42c9f24586f88fbe866e6eecc1a621f902f3907ff19afd3ce365dc27ad5551ce",
}

# Wording that must be gone once the open item is CLOSED in Document 10, section 11 (revision histories excepted).
STALE = {
    "OI-01": [r"Who creates algocore_system is OPEN", r"Who creates the repository: OPEN",
              r"first folder layout \(OPEN FOR RAMA", r"Proposed folder layout for algocore_system",
              r"settled when the repository is created"],
    "OI-02": [r"Its status \(retain as reference material, or set aside\) is OPEN FOR RAMA"],
    "OI-03": [r"Register responsibilities — RECOMMENDATION, OPEN FOR RAMA", r"a recommendation is in Document 05, section 11\.1",
              r"is recommended in Document 05, section 11\.1", r"Only the first row's maintainer is already set"],
    "OI-05": [r"Claude's working environment for this project: a new Claude Project, or new instructions"],
    "OI-08": [r"OPEN FOR RAMA, Document 10, section 11, OI-08", r"OPEN FOR RAMA, OI-08"],
    "OI-09": [r"OPEN FOR RAMA, OI-09", r"Proposed minimum content", r"proposed minimum content"],
    "OI-10": [r"OPEN FOR RAMA, Document 10, section 11, OI-10", r"OPEN FOR RAMA, OI-10"],
}
# Wording that must be gone once the decision is in the Decision Register (checked in the foundation documents,
# revision histories excepted).
STALE_BY_DECISION = {
    "D-08": [r"kept privately and (?:are|is) not published", r"only their publication copies are"],
    "D-10": [r"Files are published (?:there )?only after ChatGPT approval", r"Publish to algocore_system only after ChatGPT approval",
             r"Claude publishes after ChatGPT approval", r"Publish only after approval", r"Approve documents for publication",
             r"Claude must not publish before the required approval"],
    "D-11": [r"Final document is approved for publication", r"ChatGPT reviews the final document\."],
    "D-14": [r"until the new system design is reached"],
    "D-17": [r"the AI instructions, reviews and reports", r"Revision instructions, reviews and reports"],
    "D-18": [r"PUBLICATION_REDACTED_COPIES", r"beside their redacted copies", r"as redacted copies with identifying values masked"],
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

SECURITY_SCOPE = """SECURITY-PATTERN CHECKS - SCOPE AND LIMITS
Scope: every file under doc/, line by line, new working records included. Only text files are allowed there (M2b), so
every file is scanned. Nothing is kept private (D-08): the five original technical records are public as they are,
so S1 to S3 do not apply to them. (Their redacted copies were removed as duplicates, D-18.)
S1 IPv4 addresses (dotted quads of valid octets); loopback 127.x.x.x and 0.0.0.0 are allowed.
   Not covered: IPv6, host names, addresses written in other forms.
S2 tokens shaped like account identifiers: 2 to 4 capital letters followed by 3 to 6 digits, as a separate word.
   Allowed technical terms: SHA224/256/384/512, ISO8601, RFC numbers, AES128/192/256.
   Not covered: identifiers of other shapes (lower case, separators, other lengths).
S3 machine paths: home folders under /home or /Users, and a drive letter followed by a colon and a slash or backslash.
   The 2026-11-03 validator holds such paths as search patterns and is exempt (its content is pinned by SHA-256).
S4 credential-like assignments: api key, api secret, secret, access token, token, password, passwd or totp, then = or :,
   then a value of 12 or more key characters with both letters and digits.
   Not covered: secrets without such a key word, or shorter values.
S5 long key-like strings: 32 or more letters and digits, mixed; lower-case hexadecimal of 40 or 64 characters
   (git commit and SHA-256 hashes) is allowed.
S6 known secret formats: GitHub tokens, AWS access key IDs, Slack tokens, Telegram bot tokens, private-key blocks.
   Not covered: other providers' formats.
S7 e-mail addresses.
S8 Claude session links; the 2026-11-03 validator holds them as search strings and is exempt (content pinned).
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
    def __init__(self, root, baseline=False):
        self.root, self.baseline = Path(root), baseline
        self.results, self.notes, self.cache, self.sections, self.texts = [], [], {}, {}, {}

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

    def tree(self):
        """The folders and files under doc/, as paths relative to the root."""
        base = self.root / "doc"
        if not base.is_dir():
            return [], []
        dirs = sorted(["doc"] + [p.relative_to(self.root).as_posix() for p in base.rglob("*") if p.is_dir()])
        files = sorted(p.relative_to(self.root).as_posix() for p in base.rglob("*") if p.is_file())
        return dirs, files

    def register_entries(self):
        parts = re.split(r"^## (D-\d\d) — .*$", self.need(REGISTER), flags=re.M)
        entries = {}
        for i in range(1, len(parts), 2):
            head, rows = table(parts[i + 1])
            entries[parts[i]] = (head, rows)
        return entries


def body(t):
    """A document's text without its revision-history line, which records earlier states on purpose."""
    return "\n".join(ln for ln in t.split("\n") if not ln.startswith("**Revision history:**"))


# ------------------------------------------------------------------------------------------ folder and file checks
def below_open(path):
    return any(path.startswith(o + "/") for o in OPEN_DIRS)


def placement(rel):
    """Why a file may not be where it is, or "" if it may (Document 07, sections 3 and 5)."""
    folder, name = rel.rsplit("/", 1)
    if folder == FND:
        return "" if name in FOUNDATION else "only the ten foundation documents belong in this folder"
    if folder == REC:
        return "" if name in RECORDS else "only the five existing technical records belong here"
    if folder not in APPROVED_DIRS and not below_open(folder):
        return "not in an approved folder"
    if name == "README.md":
        return ""
    if folder in CONTAINERS:
        return "this folder holds folders and at most a README.md"
    if folder in (TOPICS, DESIGN):
        return "files go in the topic's own subfolder"
    m = DATED_NAME.match(name)
    if not m:
        return f"the name is not <FILE_NAME>_YYYY-MM-DD.<type> (types: {', '.join(TEXT_TYPES)}) or README.md"
    try:
        datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return "the date in the name is not a calendar date"
    return ""


def check_manifest(r):
    dirs, files = r.tree()
    bad = [d for d in dirs if d not in APPROVED_DIRS and not below_open(d)]
    r.ok("M1", "doc" in dirs and not bad, f"M1 every folder is an approved folder (Document 07, section 3) or lies below"
         f" an open folder ({len(dirs)} folders found)" + (f"; not approved: {bad}" if bad else ""))
    absent = [d for d in APPROVED_DIRS if d not in dirs]
    if absent:
        r.notes.append(f"approved folders not present, which is allowed (Git keeps no empty folders): {absent}")
    missing = [f for f in REQUIRED if f not in files]
    r.ok("M2", not missing, f"M2 the {len(REQUIRED)} required files are present ({len(files)} files found under doc/)"
         + (f"; missing: {missing}" if missing else ""))
    wrong = [f"{f}: {why}" for f in files for why in (placement(f),) if why]
    r.ok("M2b", not wrong, "M2b every file is in a folder that may hold it, with an approved name and file type"
         + (f"; {wrong[:20]}" if wrong else ""))
    ai = [f for f in files if re.match(r"(?:CLAUDE|CHATGPT)_", f.rsplit("/", 1)[1])]
    r.ok("M7", not ai, "M7 no standalone AI instruction, review or response file (a name beginning CLAUDE_ or CHATGPT_),"
         " under the retention rule (Document 07, section 3)" + (f"; found: {ai}" if ai else ""))
    outside = sorted(p.name for p in r.root.iterdir() if p.name not in ("doc", ".git"))
    r.ok("M5", not outside, "M5 nothing outside doc/, apart from Git's own .git folder"
         + (f"; found: {outside}" if outside else ""))
    if r.baseline:
        extra = sorted(set(files) - set(BASELINE_FILES))
        miss = sorted(set(BASELINE_FILES) - set(files))
        r.ok("M6", not extra and not miss, f"M6 baseline: exactly the {len(BASELINE_FILES)} files of the Revision 5"
             " foundation baseline" + (f"; missing {miss}" if miss else "") + (f"; not in the baseline {extra}" if extra else ""))


def check_pinned(r):
    bad = [rel.split("/")[-1] for rel, h in PINNED.items()
           if not (r.root / rel).is_file() or sha256((r.root / rel).read_bytes()) != h]
    r.ok("M3", not bad, f"M3 the {len(PINNED)} pinned historical files (the revision reports of Revisions 1 to 4,"
         " the two earlier validators, the setup record and the five originals) are byte-for-byte unchanged (SHA-256)"
         + (f"; changed or missing: {bad}" if bad else ""))


def check_publication_guard(r):
    missing = [p.split("/", 3)[-1] for p in ORIGINALS if not (r.root / p).is_file()]
    r.ok("M4", not missing, "M4 the five original technical records are present (public by decision D-08)"
         + (f"; missing: {missing}" if missing else ""))


def check_superseded(r):
    ids = set(r.register_entries())
    scope = "\n".join(body(t) for t in r.texts.values())
    stale = [f"{d}: '{p}'" for d, pats in STALE_BY_DECISION.items() if d in ids for p in pats if re.search(p, scope)]
    r.ok("V10c", not stale, "V10c no wording left that a later decision superseded (revision histories excepted)"
         + (f": {stale}" if stale else ""))


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
    alltext = "\n".join(body(t) for t in r.texts.values())
    for oi in closed:
        stale += [f"{oi}: '{p}'" for p in STALE.get(oi, []) if re.search(p, alltext)]
    r.ok("V10b", not stale, "V10b no wording left that shows a CLOSED item as open or proposed (revision histories"
         " excepted)" + (f": {stale}" if stale else ""))


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


# ------------------------------------------------------------------------------------------ Revision 5 decisions
GATES = ["Foundation → Pre-Phase", "Pre-Phase → Phase 1", "Phase 1 → Phase 2", "Phase 2 → Phase 3",
         "Phase 3 → Live deployment"]
REGISTER_ROWS = ["Master System Investigation Index", "Topic Completion Register", "Decision Register",
                 "Open Issues Register", "Audit Findings Register", "Source Inventory", "Open items table"]
SUBSECTIONS = ["6.1", "6.2", "6.3", "6.4", "6.5"]


def check_rules(r):
    T = r.texts

    def v25():
        t07 = T["07"]
        subs = re.findall(r"^### (6\.\d) ", t07, re.M)
        missing = [d for d in ("01", "02", "03", "04", "05", "06", "08") if "Document 07, section 6" not in T[d]]
        good = re.search(r"^## 6\. Commits, approval and validation$", t07, re.M) is not None
        r.ok("V25", good and subs == SUBSECTIONS and not missing, "V25 one commit and approval rule, in 07 section 6"
             " (6.1 to 6.5), referred to from 01, 02, 03, 04, 05, 06 and 08"
             + ("" if good else "; heading of 07 section 6 changed") + ("" if subs == SUBSECTIONS else f"; subsections {subs}")
             + (f"; not referred to from {missing}" if missing else ""))

    def v26():
        _, rows = table(section(T["02"], 6))
        names = [x[0] for x in rows]
        weak = [x[0] for x in rows if len(x) < 2 or "ChatGPT" not in x[1] or "Rama's explicit" not in x[1]]
        r.ok("V26", names == GATES and not weak, "V26 every gate of 02 section 6, from Foundation → Pre-Phase to Live"
             " deployment, needs ChatGPT's review and Rama's explicit approval"
             + ("" if names == GATES else f"; gates {names}") + (f"; weak: {weak}" if weak else ""))

    def v27():
        s01, s06 = section(T["01"], 2), section(T["06"], 3)
        need = ("trading-system-prod-snapshot", "trading-system-v2", "trading-system-sbx-snapshot", "D-12")
        gaps = [f"{where}: {x}" for where, s in (("01 section 2", s01), ("06 section 3", s06)) for x in need if x not in s]
        if "OPEN FOR RAMA" in s06:
            gaps.append("06 section 3 still has OPEN FOR RAMA")
        r.ok("V27", not gaps, "V27 01 section 2 and 06 section 3 agree: the legacy repository is studied, and"
             " trading-system-v2, trading-system-sbx-snapshot and every other repository are ignored (D-12)"
             + (f"; missing {gaps}" if gaps else ""))

    def v28():
        allowed = {"01": section(T["01"], 5), "10": section(T["10"], 1)}
        bad = []
        for d, t in sorted(T.items()):
            n = len(re.findall(r"\bMaster Index\b", body(t)))
            k = len(re.findall(r"\bMaster Index\b", allowed[d])) if d in allowed else 0
            if n != k:
                bad.append(f"{d}: {n - k}")
        r.ok("V28", not bad, "V28 the bare name 'Master Index' appears only in 01 section 5 (the approved sequence) and"
             " in 10 section 1, which explains it; elsewhere both indexes are named in full" + (f"; found in {bad}" if bad else ""))

    def v29():
        s = section(T["05"], 11)
        part = s.split("### 11.2")[0]
        _, rows = table(part)
        names = [x[0].split(" (")[0] for x in rows]
        heading = re.search(r"^### 11\.1 .*$", part, re.M)
        good = names == REGISTER_ROWS and heading is not None and "OPEN FOR RAMA" not in heading.group(0) and "D-13" in part
        r.ok("V29", good, "V29 05 section 11.1 covers the six registers and the open items table, as Rama decided (D-13)"
             + ("" if names == REGISTER_ROWS else f"; rows {names}"))

    for cid, fn in (("V25", v25), ("V26", v26), ("V27", v27), ("V28", v28), ("V29", v29)):
        r.guard(cid, fn)


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
    r.ok("R3", "NOT the authoritative Source Inventory" in t and f"{REG}/" in t,
         "R3 the Pre-Phase source-inventory folder's README says it is not the authoritative Source Inventory and names"
         " the register folder (working notes may be added beside it)")


# ----------------------------------------------------------------------------------------------- security checks
def check_security(r):
    hits = {k: [] for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8")}
    unreadable = []
    for rel in r.tree()[1]:
        t = r.read(rel)
        if t is None:
            if (r.root / rel).exists():
                unreadable.append(rel)
            continue
        role, short = ROLE.get(rel, "record"), rel.replace("doc/", "", 1)
        for i, line in enumerate(t.split("\n"), 1):
            where = f"{short}:{i}"
            public_as_is = role == "original"  # D-08: the originals are published as they are
            if not public_as_is and any(not (m.group(0).startswith("127.") or m.group(0) == "0.0.0.0")
                                        for m in IPV4.finditer(line)):
                hits["S1"].append(where)
            if not public_as_is and any(not ACCOUNT_LIKE_ALLOWED.match(m.group(0)) for m in ACCOUNT_LIKE.finditer(line)):
                hits["S2"].append(where)
            if role not in ("old_validator", "original") and MACHINE_PATH.search(line):
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


# ------------------------------------------------------------------------------------------------------- runner
def run_all(root, baseline=False):
    r = Run(root, baseline)
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
    r.guard("V25", lambda: check_rules(r))
    r.guard("R1", lambda: check_register(r))
    r.guard("R3", lambda: check_readme(r))
    r.guard("S0", lambda: check_security(r))
    return r


def report(r):
    mode = "working tree, and the Revision 5 baseline (--baseline)" if r.baseline else "working tree"
    print(f"VALIDATION OF {r.root} (mode: {mode})")
    for _, good, msg in r.results:
        print(("PASS " if good else "FAIL ") + msg)
    for n in r.notes:
        print("NOTE " + n)
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
NOTE_TEXT = "Self-test working note.\n"
NEW_NOTE = "doc/01_PRE_PHASE/02_WHOLE_SYSTEM_OVERVIEW/WHOLE_SYSTEM_OVERVIEW_NOTES_2026-11-05.md"


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


def write(root, rel, s=NOTE_TEXT):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


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


def drop_empty_dirs(root):
    for p in sorted((Path(root) / "doc").rglob("*"), reverse=True):
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()


D18 = ("## D-18 — Self-test closure\n\n| Field | Entry |\n|---|---|\n| Decision ID | D-18 |\n| Date | 2026-11-05 |\n"
       "| Subject | Self-test |\n| Exact decision | Self-test. |\n| Rationale | Self-test. |\n| Evidence | Self-test. |\n"
       "| Rama approval | Self-test. |\n| Affected documents | 09 §2; 10 §11 (OI-06). |\n"
       "| Status | APPROVED. OI-06: CLOSED (Document 10, section 11). |\n\n**Related documents:**")

TESTS = [
    # (id, kind, description, baseline mode, mutation, check IDs that must fail; empty = the run must pass)
    ("T01", "positive", "the working tree as it stands passes", False, lambda d: None, []),
    ("T02", "revision", "a status revision with no history entry fails", False,
     lambda d: edit(d, F["05"], r"^(\*\*Status:\*\*[^\n]*? — Revision )\d+", r"\g<1>99", regex=True), ["V24"]),
    ("T03", "revision", "the next revision with its own history entry passes", False,
     lambda d: next_revision(d, F["09"]), []),
    ("T04", "revision", "one revision number with two different dates fails", False,
     lambda d: edit(d, F["02"], "Revision 5, 2026-11-04:", "Revision 5, 2026-11-05:"), ["V24"]),
    ("T05", "revision", "section 11 heading at another revision than Document 10 fails", False,
     lambda d: edit(d, F["10"], "## 11. Open items at Revision 5", "## 11. Open items at Revision 4"), ["V24"]),
    ("T06", "revision", "Date line different from the file-name date fails", False,
     lambda d: edit(d, F["07"], "**Date:** 2026-11-03", "**Date:** 2026-11-04"), ["V3"]),
    ("T07", "status", "status APPROVED is accepted", False,
     lambda d: edit(d, F["01"], r"^(\*\*Status:\*\* )[A-Z][A-Z ]*?( — Revision )", r"\g<1>APPROVED\g<2>", regex=True),
     []),
    ("T08", "status", "a status outside Document 07, section 4 fails cleanly", False,
     lambda d: edit(d, F["01"], r"^(\*\*Status:\*\* )[A-Z][A-Z ]*?( — Revision )", r"\g<1>FINAL\g<2>", regex=True),
     ["V3"]),
    ("T09", "status", "a missing status line fails cleanly, without a crash", False,
     lambda d: edit(d, F["03"], r"^\*\*Status:\*\*.*\n", "", regex=True), ["V3", "V24"]),
    ("T10", "open item", "closing OI-04 without a decision that closes it fails", False,
     lambda d: edit(d, F["10"], "| 05 §11.2 | Rama | OPEN |",
                    "| 05 §11.2 | Rama | CLOSED, 2026-11-04 (Decision Register, D-01): self-test |"), ["V20"]),
    ("T11", "open item", "reopening OI-01 while D-01 closes it fails", False,
     lambda d: edit(d, F["10"], r"\| CLOSED, 2026-11-04 \(Decision Register, D-01\)[^|]*\|", "| OPEN |", regex=True), ["V20"]),
    ("T12", "open item", "open wording for the closed OI-02 fails", False,
     lambda d: edit(d, F["06"], "## 4. Research and evidence sources", "Its status (retain as reference material, or set"
                    " aside) is OPEN FOR RAMA.\n\n## 4. Research and evidence sources"), ["V10b"]),
    ("T13", "open item", "closing OI-06 with a matching new decision passes", False,
     lambda d: (edit(d, REGISTER, "**Related documents:**", D18),
                edit(d, F["10"], "| 09 §2 | Rama | OPEN |", "| 09 §2 | Rama | CLOSED, 2026-11-05 (Decision Register, D-18): self-test |")), []),
    ("T14", "open item", "an added open item passes (no fixed number of rows)", False,
     lambda d: edit(d, F["10"], "| 07 §5 | ChatGPT proposes (Claude if ChatGPT does not); Rama | OPEN |",
                    "| 07 §5 | ChatGPT proposes (Claude if ChatGPT does not); Rama | OPEN |\n| OI-11 | Self-test item | 09 §2 | Rama | OPEN |"), []),
    ("T15", "register", "a decision without the Rationale field fails", False,
     lambda d: edit(d, REGISTER, r"^\| Rationale \| Document 02, section 2 makes.*\n", "", regex=True), ["R1"]),
    ("T16", "register", "Document 05 with an old field name fails", False,
     lambda d: edit(d, F["05"], "|Rationale|Supporting rationale|", "|Reason|Supporting rationale|"), ["R2"]),
    ("T17", "security", "an IPv4 address in a foundation document fails", False,
     lambda d: edit(d, F["08"], "## 10. Runtime evidence\n", f"## 10. Runtime evidence\n\nSelf-test address {DOC_IP}.\n"), ["S1"]),
    ("T18", "security", "an account-shaped token in the Decision Register fails", False,
     lambda d: edit(d, REGISTER, "**Related documents:**", f"{FAKE_ID}\n\n**Related documents:**"), ["S2"]),
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
    ("T25", "security", "an IPv4 address in a new working record fails", False,
     lambda d: write(d, NEW_NOTE, f"Self-test address {DOC_IP}.\n"), ["S1"]),
    ("T26", "files", "a new working record with a dated name in an approved folder passes", False,
     lambda d: write(d, NEW_NOTE), []),
    ("T27", "files", "a Phase 1 topic subfolder with a dated topic document passes", False,
     lambda d: write(d, f"{TOPICS}/T01_MARKET_DATA/T01_MARKET_DATA_STUDY_2026-11-05.md"), []),
    ("T28", "files", "a Git checkout without the empty folders passes", False, drop_empty_dirs, []),
    ("T29", "files", "a changed original fails", False,
     lambda d: append(d, f"{REC}/03A_CRON_REGISTRY_TABLE.md", "x"), ["M3"]),
    ("T30", "files", "a changed Revision 4 validator fails", False,
     lambda d: append(d, BASE_VALIDATOR, "# x\n"), ["M3"]),
    ("T31", "files", "a missing foundation document fails cleanly", False,
     lambda d: (Path(d) / F["04"]).unlink(), ["M2", "V1"]),
    ("T32", "files", "a missing original technical record fails (they are public by D-08)", False,
     lambda d: (Path(d) / ORIGINALS[0]).unlink(), ["M2", "M4"]),
    ("T33", "files", "a working record without a dated name fails", False,
     lambda d: write(d, "doc/01_PRE_PHASE/03_OPERATIONAL_WORKFLOW/notes.md"), ["M2b"]),
    ("T34", "files", "a file of a type that is not allowed fails", False,
     lambda d: write(d, f"{ARCHIVE}/OLD_RECORD_2026-11-05.bin", "x\n"), ["M2b"]),
    ("T35", "files", "a file in a folder that is not approved fails", False,
     lambda d: write(d, "doc/01_PRE_PHASE/06_EXTRA/EXTRA_NOTES_2026-11-05.md"), ["M1", "M2b"]),
    ("T36", "files", "an extra file in the foundation folder fails", False,
     lambda d: write(d, f"{FND}/11_EXTRA_2026-11-05.md"), ["M2b", "V1"]),
    ("T37", "files", "a topic document placed directly in the topic folder fails", False,
     lambda d: write(d, f"{TOPICS}/T01_MARKET_DATA_STUDY_2026-11-05.md"), ["M2b"]),
    ("T38", "files", "a file outside doc/ fails", False,
     lambda d: write(d, "NOTES_2026-11-05.txt"), ["M5"]),
    ("T39", "baseline", "the tree as it stands passes in --baseline mode", True, lambda d: None, []),
    ("T40", "baseline", "an added working record fails in --baseline mode", True,
     lambda d: write(d, NEW_NOTE), ["M6"]),
    ("T41", "rules", "a restored prior-approval sentence fails", False,
     lambda d: edit(d, F["06"], "## 4. Research and evidence sources",
                    "Files are published only after ChatGPT approval.\n\n## 4. Research and evidence sources"), ["V10c"]),
    ("T42", "rules", "a gate without ChatGPT's review and Rama's explicit approval fails", False,
     lambda d: edit(d, F["02"], "|Implementation, testing and deployment checks, ChatGPT review and Rama's explicit approval|",
                    "|Implementation, testing and deployment checks|"), ["V26"]),
    ("T43", "rules", "the bare name 'Master Index' outside Document 01, section 5 fails", False,
     lambda d: edit(d, F["04"], "its position in the Master System Investigation Index", "its position in the Master Index"), ["V28"]),
    ("T44", "rules", "a document that no longer refers to Document 07, section 6 fails", False,
     lambda d: edit(d, F["08"], "approval and commits follow Document 07, section 6", "approval and commits follow the agreed rule"), ["V25"]),
    ("T45", "rules", "register governance without the open items table fails", False,
     lambda d: edit(d, F["05"], "| Open items table (Document 10, section 11) | Claude | ChatGPT | Rama |\n", ""), ["V29"]),
    ("T46", "rules", "trading-system-v2 missing from Document 01, section 2 fails", False,
     lambda d: edit(d, F["01"], " and the earlier project's repository trading-system-v2 (Rama, 04-Nov-2026; Decision Register, D-12)", ""), ["V27"]),
    ("T47", "files", "a standalone AI instruction file in the history folder fails (retention rule)", False,
     lambda d: write(d, f"{HIS}/CLAUDE_EXAMPLE_INSTRUCTION_2026-11-05.txt"), ["M7"]),
    ("T48", "rules", "an OPEN FOR RAMA marker left on the closed OI-08 fails", False,
     lambda d: edit(d, F["02"], "modules (Decision Register, D-16).", "modules (OPEN FOR RAMA, OI-08)."), ["V10b"]),
    ("T49", "rules", "the old wording that kept every AI instruction fails", False,
     lambda d: edit(d, F["07"], "including the existing technical records in their original form;",
                    "including the existing technical records in their original form and the AI instructions, reviews and reports;"), ["V10c"]),
    ("T50", "files", "a re-added folder of redacted copies fails (removed by D-18)", False,
     lambda d: write(d, f"{REC}/PUBLICATION_REDACTED_COPIES/01_SYSTEM_OVERVIEW.md"), ["M1", "M2b"]),
    ("T51", "rules", "the old wording that kept redacted copies beside the originals fails", False,
     lambda d: edit(d, F["07"], "The existing technical records are kept in their original form, and are public (D-08).",
                    "The existing technical records are kept both in their original form and as redacted copies with identifying"
                    " values masked (D-02); both are public (D-08)."), ["V10c"]),
]


def prepare(root, dst):
    """Copy the tree without Git's own folder, then create every approved folder. Git keeps no empty folders, so a
    checkout lacks some of them; the fixtures create them and never depend on the source having them."""
    shutil.copytree(root, dst, ignore=shutil.ignore_patterns(".git"))
    for d in APPROVED_DIRS:
        (dst / d).mkdir(parents=True, exist_ok=True)


def self_test(root):
    print(f"SELF-TESTS ON TEMPORARY COPIES OF {root}")
    passed = 0
    for tid, kind, desc, baseline, mutate, must_fail in TESTS:
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "pkg"
            try:
                prepare(root, dst)
                mutate(dst)
                r = run_all(dst, baseline)
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
    mode = args.pop(0) if args and args[0] in ("--baseline", "--self-test") else ""
    if len(args) != 1 or not (Path(args[0]) / "doc").is_dir():
        print(__doc__.split("Conventions")[0].strip())
        print("\nUSAGE ERROR: give one folder that contains doc/.")
        return 2
    if mode == "--self-test":
        return self_test(Path(args[0]))
    return report(run_all(Path(args[0]), mode == "--baseline"))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
