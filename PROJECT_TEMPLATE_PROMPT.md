# Codex Project and Harness Engineering Template

This file is the global design document for creating and operating project
reference folders under the installed `codex_projects` folder. For routine
project creation, use `PROJECT_CREATION_RUNBOOK.md`; for required Markdown file
skeletons, use `PROJECT_FILE_SKELETONS.md`.

Path convention:
- Use `<CODEX_PROJECTS_ROOT>` for the installed `codex_projects` folder's
  absolute path.
- The public default install creates `codex_projects` in the current terminal
  location and removes its `.git` folder so it is a normal workspace folder.
- Use `~/codex_projects` only for the optional home-directory install.
- Do not hard-code a specific user's home path in generated project files unless
  the user explicitly asks for it.

It has two jobs:
1. Create a clean reference folder for attachments, outputs, presentations, and
   logs.
2. Initialize lightweight harness-engineering documents for requirements,
   workflow planning, traceability, status tracking, decisions, and repeatable
   logging.

## Canonical Source Map

Use one canonical source for each concern so execution rules do not drift across
documents.

| Concern | Canonical source |
| --- | --- |
| Execution flow, fixed intake questions, approval gates, and completion reporting | `PROJECT_CREATION_RUNBOOK.md` |
| Required Markdown document skeletons | `PROJECT_FILE_SKELETONS.md` |
| Detailed operating rules, token optimization, and other-agent adaptation | `OPERATING_GUIDE.md` |
| High-level design intent, document roles, audit criteria, and structure principles | `PROJECT_TEMPLATE_PROMPT.md` |
| Minimal instructions to copy into an agent | `AGENTS_REQ.md` |

## Progressive Project Creation Prompt

Routine project creation is executed through `PROJECT_CREATION_RUNBOOK.md`.
That runbook owns the trigger, fixed intake questions, approval flow, write
safety rules, and completion report format.

```text
새 프로젝트 생성
```

This template only defines the design intent behind that flow: collect project
information progressively, avoid creating the full structure before approval,
and keep generated project folders consistent.

## Response Consistency Rules

Keep creation responses predictable and concise, but do not duplicate the fixed
questions or response templates here. Use the canonical wording in
`PROJECT_CREATION_RUNBOOK.md` for:

- normal intake responses;
- design-reference folder approval;
- project brief approval;
- creation completion reports;
- blocker or permission handling.

## Progressive Intake Flow

The intake flow is deliberately progressive: identify the project, record any
related code path, handle design references, capture purpose and initial
requirements, present a project brief, and create files only after approval.

Do not maintain step-by-step execution details here. Follow
`PROJECT_CREATION_RUNBOOK.md` for the exact step order, fixed questions,
path checks, approval gates, overwrite protection, and creation rules.

## One-Shot Project Creation

One-shot creation is an advanced, discouraged shortcut. Routine project
creation should use `PROJECT_CREATION_RUNBOOK.md`.

Use a one-shot request only when all project information is already known and
the user explicitly asks to skip the normal intake conversation. Even then, the
agent must still follow the runbook's path checks, approval requirement,
overwrite protection, direct file-writing safety rules, and
`PROJECT_FILE_SKELETONS.md` skeleton requirements.

## Folder Roles

| Folder/File | Role |
| --- | --- |
| `attachments/` | Input folder for PDFs, Word files, papers, manuals, copied docs, and external source text. |
| `attachments/project-design/` | Optional intake folder for files needed to design the project before full project creation. |
| `screenshots/` | Input folder for images, screenshots, diagrams, GIFs, UI captures, terminal captures, and visual references. |
| `plans/` | Harness-engineering folder for requirements, workflow, traceability, checklist, status, and decisions. |
| `configs/` | Generated-output folder for analysis, summaries, extracted notes, converted files, configs, and environment material. |
| `presentations/` | Generated-output folder for slide decks, presentation scripts, chapter outputs, and presentation assets. |
| `logs/` | Generated-output folder for work logs, request summaries, verification notes, and remaining checks. |
| `NOTES.md` | Short project index with purpose, key paths, folder rules, and links to `plans/` documents. |

## Required Document Roles

Create these Markdown files for every new project.

| File | Required Content |
| --- | --- |
| `NOTES.md` | Project purpose, related code path, external reference info, current goal, known context, folder layout, planning file links, checks done, remaining checks. |
| `plans/REQUIREMENTS.md` | User requirements with stable IDs, acceptance criteria with stable IDs, out-of-scope items if any. |
| `plans/WORKFLOW.md` | End-to-end workflow plan, phases, expected inputs, expected outputs, phase status. |
| `plans/CHECKLIST.md` | Project checklist from setup through source review, output generation, verification, and handoff. |
| `plans/TRACEABILITY.md` | Lightweight mapping from requirement IDs to requirement-supporting outputs, logs, verification evidence, and status. |
| `plans/STATUS.md` | Overall status, last reviewed date, current phase, active output group, latest generated output, latest log, next action. |
| `plans/DECISIONS.md` | Date, decision ID, decision, rationale, and impact for important project choices. |
| `logs/LOG_TEMPLATE.md` | Bilingual log template with an English working record and Korean user summary. |

Keep `NOTES.md` short. Put detailed requirements, planning, checklist, status,
and decision history in `plans/`.

## Initial Document Skeletons

The canonical skeletons for required Markdown files live in
`PROJECT_FILE_SKELETONS.md`. This template describes why those documents exist;
it does not duplicate their required headings, tables, or placeholder rules.

When creating a new project, use `PROJECT_CREATION_RUNBOOK.md` for execution and
read `PROJECT_FILE_SKELETONS.md` immediately before writing Markdown files.

## Agent Re-Read Rules

The design uses progressive context loading. Agents should start with the
smallest project index, then read deeper planning, input, or log files only when
the current task needs them.

Principles:
- Begin ongoing project work from `NOTES.md` and `plans/STATUS.md`.
- Inspect file lists before reading large PDFs, screenshots, logs, or source
  trees.
- Prefer durable summaries under `configs/{group}/` before rereading full
  source material.
- Keep `plans/STATUS.md` current after meaningful work, and update other
  planning files only when their contents actually change.
- Keep one session focused on one coherent unit of work.

For detailed operating rules, use `OPERATING_GUIDE.md`. For minimal agent
instructions that can be copied into a tool configuration, use `AGENTS_REQ.md`.

## Output Grouping Rules

Use the same grouping rule for `configs/` and `logs/`.

| Situation | Rule | Example |
| --- | --- | --- |
| Chapter, section, module, topic, or presentation unit is clear | Use chapter/topic grouping | `configs/Ch_5/`, `logs/Ch_5/` |
| Project has stable content units | Use those units | `configs/user-manual/`, `logs/user-manual/` |
| Work is chronological, experimental, debugging-oriented, or session-based | Use date+topic grouping | `configs/2026-06-07-load-test/`, `logs/2026-06-07-load-test/` |
| Unclear grouping | Use date+topic and explain the choice in the log | `configs/2026-06-07-initial-review/` |

Presentation outputs must always use a subfolder:
- `presentations/Ch_5/`
- `presentations/project-overview/`
- `presentations/final-report/`

Do not save generated presentation files directly under `presentations/`.

## Lightweight Harness Rules

Use stable IDs so requirements, outputs, and verification can be traced without
creating a heavy process.

| Item | ID Format | Example |
| --- | --- | --- |
| Requirement | `REQ-###` | `REQ-001` |
| Acceptance criterion | `AC-###` | `AC-001` |
| Decision | `DEC-###` | `DEC-001` |
| Verification item | `VER-###` | `VER-001` |

Recommended `plans/TRACEABILITY.md` columns:

| Requirement ID | Acceptance Criteria | Output Files | Log Files | Verification Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| `REQ-001` | `AC-001` | `configs/...` | `logs/...` | `VER-001` | Not started |

Trace only outputs that satisfy, verify, or materially support a requirement.
Do not trace every generated file by default.

Status values:
- `Not started`
- `In progress`
- `Blocked`
- `Satisfied`

Do not mark a requirement as `Satisfied` unless all of these are true:
- Linked output files exist.
- Linked log files exist.
- Verification evidence is recorded.
- Remaining checks are empty, resolved, or explicitly accepted by the user.

When requirements or acceptance criteria change:
- Update `plans/REQUIREMENTS.md`.
- Add a short decision entry to `plans/DECISIONS.md`.
- Update `plans/TRACEABILITY.md` if existing outputs, logs, or verification
  evidence are affected.
- Update `plans/STATUS.md` with the current impact and next action.

Record decisions only when they affect requirements, output grouping, folder
rules, verification, project scope, or user-visible deliverables.

Recommended `plans/DECISIONS.md` columns:

| Date | Decision ID | Decision | Rationale | Impact |
| --- | --- | --- | --- | --- |

Do not add heavyweight harness artifacts by default, such as separate issue
trackers, release plans, risk registers, or formal review boards. Add them only
when the user explicitly asks or the project clearly needs them.

## Log Template Requirements

Every generated log must follow the `logs/LOG_TEMPLATE.md` skeleton defined in
`PROJECT_FILE_SKELETONS.md`.

Use English in `English Working Record` so future Codex sessions can reuse the
technical context efficiently. Use Korean in `Korean User Summary` so the user
can quickly verify what happened.

## Operating Rules

Detailed operating rules live in `OPERATING_GUIDE.md`. Keep these high-level
principles aligned with that guide:

1. Inspect input file lists before deep analysis.
2. Store normal generated outputs under `configs/{group}/`.
3. Store presentation outputs under `presentations/{group}/`.
4. Store logs under `logs/{group}/`, matching the related `configs/` group when
   possible.
5. Link outputs to `plans/TRACEABILITY.md` only when they satisfy, verify, or
   materially support a requirement.
6. Keep `plans/STATUS.md` current after meaningful work.
7. Do not leave temporary files, unclear duplicates, debug artifacts, or dummy
   files unless explicitly requested.

## Recommended File Names

- `attachments/{source-title}.pdf`
- `screenshots/{topic-or-screen}.png`
- `configs/{chapter-or-topic}/summary.md`
- `configs/{YYYY-MM-DD}-{short-topic}/summary.md`
- `presentations/{topic}/slides.pptx`
- `presentations/{topic}/script.md`
- `plans/TRACEABILITY.md`
- `logs/{chapter-or-topic}/{YYYY-MM-DD}-{short-task-name}.md`
- `logs/{YYYY-MM-DD}-{short-topic}/{YYYY-MM-DD}-{short-task-name}.md`
- `logs/{YYYY-MM-DD}-{short-task-name}.md`

## User Guide

For Korean usage instructions, see [README.md](README.md).
