# Required Agent Instructions for Codex Projects

Operational rules for the installed `codex_projects` folder at
`<CODEX_PROJECTS_ROOT>`.

## Performance-Safe Context Budget Discipline

Follow these rules unless a higher-priority instruction conflicts:

- Keep global instructions short and avoid duplicating rules across global,
  project, and task-specific guidance.
- Put detailed workflows in runbooks or project-local files and load them only
  when the matching trigger or task requires them.
- Before reading large files, logs, generated outputs, or broad source trees,
  use file lists and fast search such as `rg` to narrow the relevant scope.
- Prefer targeted reads over bulk loading.
- For large recurring inputs, create or reuse summary/index files before
  rereading original PDFs, logs, or source trees.
- For code changes, verify conclusions against the actual source, tests, and
  config files rather than relying only on summaries or indexes.
- Keep one session focused on one coherent unit of work. When the client
  supports it, compact or summarize long context before continuing, and start a
  new session for unrelated work.
- For commands that may produce long output, narrow output with targeted paths,
  `rg`, `find`, `head`, `tail`, or equivalent filters.
- Do not dump full logs, generated files, dependency trees, or broad test output
  when a focused excerpt is enough.
- For failures, keep the exact command, exit status, and relevant error lines.
- Do not reduce verification quality just to save context; reopen exact source
  sections when accuracy, safety, or user-visible correctness requires it.

## Codex Project Trigger

When the user enters exactly `새 프로젝트 생성`, treat it as a request to start
the progressive Codex project creation flow.

If the user uses a near-trigger such as `새 프로젝트 만들어줘`,
`프로젝트 세팅 시작`, or `새프로젝트 생성`, do not create files or start the
creation flow yet. Ask for confirmation instead:

```text
새 프로젝트 생성 흐름을 시작할까요? 시작하려면 `새 프로젝트 생성`이라고 입력해 주세요.
```

Only the exact trigger `새 프로젝트 생성` starts project creation.

Runbook path:
`<CODEX_PROJECTS_ROOT>/PROJECT_CREATION_RUNBOOK.md`.

If the runbook exists:
1. Read the runbook.
2. Follow its `Progressive Intake Flow`.
3. Follow its `Response Consistency` rules unless a concrete blocker prevents
   them, such as missing permissions, an unsafe path, a filesystem error, or a
   conflicting user instruction.
4. Reply in Korean: `새 프로젝트 생성을 준비합니다. 단계별로 필요한 정보만 확인하겠습니다.`
5. Use the runbook's fixed intake questions by default; skip questions only
   when the user already provided the information.
6. Ask only the next unresolved fixed intake step block at a time.
   Do not merge separate steps. On the initial trigger, ask only for project
   name and folder name unless those are already known. After each user
   response, ask only unresolved fields in the current step and do not repeat
   answered fields.
7. Treat this as lightweight project creation, not as a heavier planning
   framework. If the user explicitly invokes another workflow, follow that
   request instead.
8. Do not create the full project structure until the user approves the proposed
   project brief.
9. If design reference files are needed before full creation, create only the
   approved project root, `attachments/`, and `attachments/project-design/`;
   then inspect that folder's file list before proposing the project brief.
10. Immediately before creating approved project files, read
    `<CODEX_PROJECTS_ROOT>/PROJECT_FILE_SKELETONS.md` and use its skeletons
    exactly.

If the runbook does not exist, say so and ask the user for the correct runbook
path. Do not guess another location.

## Codex Project Work Loop Gate

Before running the project state loop, classify the request using only the
user's message, the current working directory, explicitly referenced paths, and
recent conversation context. Do not load project state files just to decide
whether the loop applies.

Run the project state loop only for actual work inside a specific Codex project,
including:
- continuing an existing Codex project;
- creating, changing, or reviewing project outputs;
- analyzing project inputs under `attachments/`, `screenshots/`, or related
  paths;
- updating status, requirements, traceability, decisions, logs, or
  presentations;
- judging completion, verification, acceptance criteria, or requirement
  satisfaction;
- migrating existing work into a Codex project structure.

Do not run the project state loop for:
- questions or edits about this template itself;
- installation, setup, update, or sharing guidance;
- general explanations, brainstorming, or design discussion;
- unrelated coding tasks outside a specific Codex project.

If applying the loop would require guessing the project, ask a short
clarification question before reading or updating project state files.

## Active Codex Project Root

Before reading or updating any project `plans/` file, identify the active Codex
project root under `<CODEX_PROJECTS_ROOT>`.

Prefer, in order:
1. a project folder explicitly named by the user;
2. a user-referenced file or folder inside a Codex project;
3. the current working directory, if it is inside a Codex project;
4. the project used or created in the immediately recent conversation;
5. the only Codex project folder name that exactly or unambiguously matches a
   project name in the request.

If no single project is clear, ask the user which project to use. Do not read or
update a random `plans/` file. Do not open candidate project state files just to
search for a match unless the user asks you to search. After resolution, treat
that folder as `<ACTIVE_CODEX_PROJECT_ROOT>` for the current turn.

After choosing a candidate project root, verify its identity before reading
`plans/` files:
1. Prefer a folder with `.codex-project.json`.
2. If `.codex-project.json` exists, read it and confirm it is valid JSON with
   `schema` equal to `codex_projects` and `project_folder` equal to the folder
   name. If it is invalid or conflicts, ask the user before using that project.
3. If `.codex-project.json` is missing, treat the folder as a legacy Codex
   project only when `NOTES.md` and `plans/STATUS.md` exist. Do not create or
   repair `.codex-project.json` unless the user asks or the task is
   migrating/repairing project structure. Mention the missing identity file only
   when it affects the task, causes ambiguity, or the user asks for project
   identity or loop details.

## Ongoing Codex Project Work

For actual work inside `<ACTIVE_CODEX_PROJECT_ROOT>`, use this lightweight
project loop. If the user explicitly asks for another workflow, follow that
request instead.

For ongoing work, keep context loading small:
1. Always read `<ACTIVE_CODEX_PROJECT_ROOT>/NOTES.md` and
   `<ACTIVE_CODEX_PROJECT_ROOT>/plans/STATUS.md` first.
2. Read `plans/REQUIREMENTS.md` before creating outputs, judging completion,
   changing scope, or checking requirement satisfaction.
3. Read `plans/TRACEABILITY.md` before linking outputs, logs, verification
   evidence, or requirement status.
4. Read `plans/DECISIONS.md` before changing established decisions or when a
   request may conflict with prior decisions.
5. Read `plans/WORKFLOW.md` before changing project phases or workflow
   structure.
6. Read `plans/CHECKLIST.md` before marking checklist or phase progress.
7. Read `logs/LOG_TEMPLATE.md` only before writing a new log.
8. For project inputs under `attachments/`, `screenshots/`, or related code
   paths, inspect file lists first and choose only the files or sections needed
   for the current task.
9. Prefer existing summaries under `configs/{group}/` before rereading full
   PDFs, long documents, logs, or source files.

Common project tasks:
- For document analysis, inspect `attachments/` first.
- For image or screenshot analysis, inspect `screenshots/` first.
- For code analysis, inspect the related path with fast search or file lists
  before opening source files. When code context is large, create or update a
  `configs/{group}/SOURCE_INDEX.md` before deep file reads.
- Store generated analysis/config outputs under `configs/{group}/`.
- Store presentation outputs under `presentations/{group}/`.
- Store logs under `logs/{group}/` using the project's log template.

Treat work as meaningful when it changes or establishes any project state:
- current phase or current state;
- generated outputs or latest output references;
- logs or latest log references;
- requirements, acceptance criteria, scope, or requirement status;
- traceability links or verification evidence;
- decisions, blockers, reference paths, output grouping, or next actions.

Do not treat a request as meaningful project work when it only answers a
general question, discusses this template, explains setup, inspects files
without changing project state, or makes no change to the project's status,
outputs, requirements, traceability, decisions, verification, blockers, or next
actions.

After meaningful work:
- update `plans/STATUS.md`, preserving and refreshing these required resume
  headings: `Last Updated`, `Current State`, `Last Completed`, `Next Action`,
  and `Blocked By`;
- update `plans/TRACEABILITY.md` when outputs, logs, verification evidence, or
  requirement status changed;
- update `plans/REQUIREMENTS.md` when requirements, acceptance criteria, or
  scope changed;
- update `plans/DECISIONS.md` when durable decisions changed;
- update `plans/CHECKLIST.md` only when checklist items actually changed.

Before final reporting, check whether meaningful work occurred without the
required state updates. If a state file was intentionally not updated, report
why.

## Documentation Verification

For documentation-only template or `codex_projects` project work, verification can
be limited to:
- confirming changed files exist;
- inspecting relevant JSON keys and Markdown sections;
- checking links and paths;
- confirming no unintended source/project files were modified.

Do not run code tests unless source code behavior changed.

## Reporting

For `codex_projects` project work, keep final reports focused on user-visible
results. Include:
- files created or changed;
- key project state, rule, or structure changes;
- verification performed;
- remaining usage notes or risks.

Do not include project loop internals by default. Report active project, state
files read, and state files updated only when:
- the user asks for loop, state-file, traceability, audit, or status details;
- active project resolution was ambiguous or required confirmation;
- `.codex-project.json` is missing, invalid, or conflicting and this affects the
  task;
- a required state update was skipped or intentionally not performed;
- the task judges completion, verification, acceptance criteria, or requirement
  satisfaction.
