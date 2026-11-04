# 01 — Project Foundation & Scope

**Project:** Trading System — Legacy Manual & V2 Redesign
**Status:** DRAFT — Revision 2, for ChatGPT review
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 2, 2026-11-03: the audit rule widened to the entire system, every area and flow, not only configuration settings (Rama, 03-Nov-2026); changes are listed in the Revision 2 report.

## 1. Project purpose

Create a completely new Python-based automated trading system through a controlled process: understand the existing legacy system, document its actual behaviour, audit it, and then design the new system from an agreed foundation.

The objective is to prevent the historical problems of inconsistent logic, duplicated functionality, uncoordinated modules, undocumented changes and inadequate governance from recurring.

## 2. The legacy system under investigation

There is only one legacy system under investigation: the production repository trading-system-prod-snapshot (https://github.com/ramakrishnan031-ctrl/trading-system-prod-snapshot).

The testing repository trading-system-sbx-snapshot and all other repositories are ignored (Rama, 03-Nov-2026).

How the repository is studied (a local, read-only clone) is set out in Document 06, section 3.

## 3. Legacy-system status

The existing legacy trading system is DEAD / REFERENCE ONLY.

It is retained as historical evidence for investigation and documentation.

The legacy system must not be:

* Repaired or operationally revived.
* Modified as part of the documentation exercise.
* Treated as the automatic architecture for the new system.
* Used as justification for retaining its calculations, strategies, modules or database design without a separate future decision.

## 4. New-system scope

The new system is a completely new system.

The project is Live-only. Paper-mode investigation, development and operational workflows are excluded. Shared code may be examined only when necessary to establish actual Live behaviour.

## 5. Approved overall sequence

Existing system study → technical audit → reconciliation of study and audit → repeated topic by topic until the Master Index is complete → new-system proposal → discussion topic by topic → decide what to retain, change, modify, replace or reject → resolve ambiguities → revise until agreed and approved → freeze the new system design → code and develop.

Document 02 maps this sequence onto the project phases. Legacy documentation and new-system design are kept separate and are never merged (Document 07, section 3).

## 6. Fundamental principles

* Evidence before conclusions.
* No assumptions presented as facts.
* What the system actually does is established from its code and compared with what it was intended to do, across the entire system: every area and flow, not only configuration settings, with every kind of issue looked for (Document 04, section 5).
* Every issue found is raised and discussed with Rama, and its agreed treatment, or its open status, is recorded (Document 04, section 5.5).
* No automatic carry-forward of legacy behaviour.
* No undocumented decisions or changes.
* Permanent project records are the authoritative continuity source.
* Rama retains final decision authority.
* AI tools support the project but do not replace approval and governance.

## 7. Intended environment

The original project proposal specifies:

* Development: Windows local PC.
* Live execution: Oracle Ubuntu VM.

Detailed engineering decisions remain subject to the later design phase.

## 8. Project repository

The project's documents and approved deliverables are kept in a new public GitHub repository, algocore_system (Rama, 03-Nov-2026). Files are published there only after ChatGPT approval (Document 07, section 6).

## 9. Project outcome

The final outcome is an agreed, documented and governed production design for a new trading system, followed by controlled development and deployment.

**Related documents:** 02, 03, 04, 05, 06, 07 and 09.
