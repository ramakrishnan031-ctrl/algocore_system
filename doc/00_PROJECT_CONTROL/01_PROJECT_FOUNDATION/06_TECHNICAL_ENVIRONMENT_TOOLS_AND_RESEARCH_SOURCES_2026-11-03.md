# 06 — Technical Environment, Tools & Research Sources

**Status:** APPROVED — Revision 5, approved by Rama on 2026-11-04 (Decision Register, D-19)
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 3, 2026-11-04: section 3 records that Rama created algocore_system; section 6 no longer lists OI-01 and OI-05, which are settled, and adds a technical reference on the Oracle Cloud user name (Decision Register, D-01 and D-04). This document did not change in Revision 2. Revision 5, 2026-11-04: section 2 states each party's part in commits, reviews and approvals (D-10 and D-11); section 3 adds trading-system-v2 to the ignored repositories and names the admitted legacy sources (D-12, which closes OI-02), and states algocore_system's commit rule and working period (D-06, D-10 and D-14); changes are listed in the Revision 5 report. This document did not change in Revision 4.

## 1. Intended technical environment

The original project proposal establishes:

| Area | Intended environment |
|---|---|
| Development | Windows local PC |
| Live execution | Oracle Ubuntu VM |
| System language | Python |
| Trading scope | Live-only |

Detailed software versions, infrastructure specifications, deployment design and technical configurations remain to be established in the appropriate project phase.

## 2. AI working environment

### ChatGPT
Used for project coordination, investigation instructions, independent review, gap identification, technical verification, and the review of commits and topic packages (Document 07, section 6).

### Claude
Used for repository inspection, technical fieldwork, study documents, audits, final file preparation and commits to algocore_system (Document 07, section 6).

### Rama
Provides access, transfers materials, clarifies requirements, and approves decisions, topic documents and phase transitions.

## 3. Repositories

GitHub is the central collaboration and documentation platform.

| Repository | Role in the project | How it is used |
|---|---|---|
| trading-system-prod-snapshot (public) | The only legacy system under investigation (Document 01, section 2). | Claude studies a local, read-only clone. Nothing is written back to the clone or to the repository; the legacy code is read, not run or deployed. Evidence cites the commit studied (Document 04, section 7). |
| algocore_system (new, public) | The project's working repository: its documents, working records and approved deliverables (Document 07, section 2). | Commits follow Document 07, section 6 (Decision Register, D-10). It is the working repository until the Phase 2 new-system design is completed and frozen (D-06 and D-14). Created by Rama on 03-Nov-2026 (D-01). |
| trading-system-v2 (the earlier project's repository), trading-system-sbx-snapshot (the testing repository), and every repository not listed above | None. | Ignored: not opened, cloned, browsed, inventoried, inspected or used, and none of their records is used as governing or historical evidence (Rama, 03-Nov-2026; trading-system-v2 added by Rama, 04-Nov-2026; Decision Register, D-12). |

The admitted legacy sources are the legacy repository above and the five existing technical records already in algocore_system (Document 08, section 9), together with any surviving external evidence that Rama supplies (section 4.2). This does not authorise Phase 1 investigation or any further legacy source discovery (D-12).

The production repository has been public for two months; Rama accepts this (03-Nov-2026). Its public exposure is not raised as an issue, and no additional security flagging is added. The credential rule of section 5 still applies to every project document.

## 4. Research and evidence sources

### 4.1 Evidence priority

For legacy-system facts, use this evidence priority:

1. Actual source code.
2. Operational/runtime/database/broker evidence.
3. Logs and reports.
4. Approved project and system documentation.
5. External documentation for API and platform context.
6. Clearly labelled interpretation where evidence is unavailable.

External documentation may explain an API, but it cannot override the actual implementation found in the repository. Project and system documentation, configuration files and comments are compared with the code, never taken in its place (Document 04, section 5).

### 4.2 Runtime evidence limitation

Both legacy VMs were terminated. There is no known backup of their databases, logs or crontab (reported by Rama on 05-Oct-2026). Therefore:

* Repository evidence can establish what the code implements.
* Runtime behaviour not supported by surviving evidence is classified UNKNOWN / NOT ESTABLISHED.
* Runtime behaviour is never invented, and the code is not assumed to have run as written. For example, a schedule in the repository does not show that the job ran on the VM, and a configured value does not show that it was the value in force on a given day.
* Any surviving external evidence (for example a broker statement, an alert message or a file Rama supplies) is recorded separately in the Source Inventory (Document 10, section 8), with its origin, and cited as external evidence, not as repository evidence.

Priorities 2 and 3 of section 4.1 therefore apply only to such surviving evidence.

## 5. Tool usage principles

- Use available connections and tools to reduce unnecessary manual work for Rama.
- Do not claim to have inspected a repository or file unless it was actually accessible.
- If a tool is unavailable, explain the limitation and use an appropriate alternative.
- Preserve source references and evidence.
- Never expose passwords, API secrets, access tokens, TOTP secrets or other credentials in project documentation.

## 6. Outstanding environment details

The following are not established in this baseline:
- Exact Windows development setup.
- Oracle Ubuntu VM specifications.
- Python and dependency versions.
- Deployment and connectivity configuration.
- Tool access permissions and account arrangements.
- The commit of trading-system-prod-snapshot to be studied (to be recorded at Pre-Phase; Document 02, section 2).

These require source verification or later decisions.

Recorded as settled on 04-Nov-2026, and no longer outstanding: who creates algocore_system, and its first folder layout (Decision Register, D-01; Document 07, sections 2 and 3); and Claude's working environment, which is a dedicated Claude Project, with ChatGPT working in a dedicated ChatGPT project (D-04).

Technical reference only: the Oracle Cloud Infrastructure documentation, [Connecting to a Linux Instance](https://docs.oracle.com/iaas/Content/Compute/Tasks/connect-to-linux-instance.htm), states that the user name for instances created from Ubuntu platform images is `ubuntu`. This is context for the VM home folder named in the existing technical records (Document 08, section 9). It does not establish how the legacy VMs were configured (section 4.2), and it does not mean that every Oracle image or configuration uses that user name.

**Related documents:** 01, 03, 04, 05, 07, 09 and 10.
