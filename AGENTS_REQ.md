# Required Agent Instructions for Codex Projects

Manager root: `<CODEX_PROJECT_MANAGER_ROOT>`
Workspace root: `<CODEX_PROJECTS_WORKSPACE_ROOT>`

Keep context small. Use file lists and fast search before opening large files,
logs, generated outputs, PDFs, screenshots, or broad source trees. Prefer
existing summaries under `configs/{group}/` before rereading full sources. Do
not skip verification only to save context.

## Project Creation Trigger

Only the exact user message `새 프로젝트 생성` starts the Codex project creation
flow.

For near-triggers such as `새 프로젝트 만들어줘`, `프로젝트 세팅 시작`, or
`새프로젝트 생성`, ask:

```text
새 프로젝트 생성 흐름을 시작할까요? 시작하려면 `새 프로젝트 생성`이라고 입력해 주세요.
```

On the exact trigger:

1. Read `<CODEX_PROJECT_MANAGER_ROOT>/PROJECT_CREATION_RUNBOOK.md`.
2. Reply in Korean:
   `새 프로젝트 생성을 준비합니다. 단계별로 필요한 정보만 확인하겠습니다.`
3. Follow the runbook's `Progressive Intake Flow` and `Response Consistency`
   rules unless a concrete blocker or explicit user instruction conflicts.
4. Use fixed intake questions by default. Ask only the next unresolved step
   block; do not merge separate steps.
5. On the initial trigger, ask only for project name and folder name unless
   already known.
6. Treat this as lightweight project creation, not another planning framework,
   unless the user explicitly invokes one.
7. Do not create the full project structure until the user approves the
   proposed project brief.
8. If design references are needed first, create only the approved project
   root, `attachments/`, and `attachments/project-design/`, then inspect that
   folder list before proposing the brief.
9. Immediately before creating approved project files, read
   `<CODEX_PROJECT_MANAGER_ROOT>/PROJECT_FILE_SKELETONS.md` and use its
   skeletons exactly.

If the runbook is missing, say so and ask for the correct path. Do not guess.

## When To Run The Project Loop

Run the project loop only for actual work inside one specific Codex project:

- continuing project work;
- creating, changing, or reviewing project outputs;
- analyzing project inputs under `attachments/`, `screenshots/`, or related
  paths;
- updating status, requirements, traceability, decisions, checklist, logs, or
  presentations;
- judging completion, verification, acceptance criteria, or requirement
  satisfaction;
- migrating or repairing project structure.

Do not run the loop for template setup/update questions, general explanations,
brainstorming, or unrelated coding tasks.

If the target project is unclear, ask which project to use before reading or
updating `plans/` files. Do not read random candidate `plans/` files just to
find a match unless the user asks you to search.

## Active Project Root

Before reading or updating project `plans/` files, identify one active project
under `<CODEX_PROJECTS_WORKSPACE_ROOT>`.

Prefer:

1. a project folder explicitly named by the user;
2. a referenced file/folder inside a project;
3. the current working directory if it is inside a project;
4. the project used or created in the recent conversation;
5. the only folder that unambiguously matches the request.

After choosing a candidate:

- Prefer `.codex-project.json`.
- If it exists, read it and confirm JSON `schema == "codex_projects"` and
  `project_folder` matches the folder name.
- If it is missing, treat the folder as legacy only when `NOTES.md` and
  `plans/STATUS.md` both exist.
- If identity is invalid or ambiguous, ask before using the project.
- Do not create or repair `.codex-project.json` unless the user asks or the
  task is migration/repair.

## Ongoing Project Work

For actual work inside `<ACTIVE_CODEX_PROJECT_ROOT>`:

1. Read `NOTES.md` and `plans/STATUS.md` first.
2. Read `plans/REQUIREMENTS.md` before creating outputs, judging completion,
   changing scope, or checking requirement satisfaction.
3. Read `plans/TRACEABILITY.md` before linking outputs, logs, verification
   evidence, or requirement status.
4. Read `plans/DECISIONS.md` before changing established decisions or when a
   request may conflict with them.
5. Read `plans/WORKFLOW.md` before changing phases or workflow structure.
6. Read `plans/CHECKLIST.md` before marking checklist or phase progress.
7. Read `logs/LOG_TEMPLATE.md` only before writing a new log.
8. Inspect input file lists before opening files under `attachments/`,
   `screenshots/`, or related source paths.

Default output locations:

- analysis/config outputs: `configs/{group}/`
- presentation outputs: `presentations/{group}/`
- logs: `logs/{group}/`, using `logs/LOG_TEMPLATE.md`

Common routing:

- document analysis starts from `attachments/`
- image or screenshot analysis starts from `screenshots/`
- code analysis starts with fast search and file lists

For large code context, create or update `configs/{group}/SOURCE_INDEX.md`
before deep source reads.

## State Updates

Meaningful work is any change to project state, outputs, logs, requirements,
traceability, decisions, blockers, reference paths, output grouping, or next
actions.

After meaningful work:

- update `plans/STATUS.md`, preserving `Last Updated`, `Current State`,
  `Last Completed`, `Next Action`, and `Blocked By`;
- update `plans/TRACEABILITY.md` when outputs, logs, verification evidence, or
  requirement status changed;
- update `plans/REQUIREMENTS.md` when requirements, acceptance criteria, or
  scope changed;
- update `plans/DECISIONS.md` when durable decisions changed;
- update `plans/WORKFLOW.md` when phase or workflow structure changed;
- update `plans/CHECKLIST.md` only when checklist items changed.

Do not update project state for pure setup guidance, template discussion, or
file inspection that changes nothing.

Before final reporting, check whether meaningful work occurred without the
required state updates. If skipped intentionally, report why.

## Documentation-Only Template Work

For documentation-only changes to this template, verification can be limited to
changed-file inspection, Markdown structure, links, paths, and checking that no
unintended project/source files changed. Run code tests only when code behavior
changed.

## Reporting

For Codex project work, report only user-visible results by default: files
changed, key state/rule changes, verification, and remaining risks. Include
loop internals only when identity was ambiguous, a required state update was
skipped, or the user asks for state, traceability, audit, or completion details.
