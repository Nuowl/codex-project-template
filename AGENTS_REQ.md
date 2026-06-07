# Required Agent Instructions for Codex Projects

Copy these instructions into the agent's global or project instruction file if
you want the `codex_projects` project flow to work from the short trigger.

These instructions are intentionally minimal. They assume the project creation
runbook exists at `~/codex_projects/PROJECT_CREATION_RUNBOOK.md` and the required
file skeletons exist at `~/codex_projects/PROJECT_FILE_SKELETONS.md`.

## General Context Budget Discipline

Add these rules to the agent's global or project instruction file if they are
not already present:

- Before reading large files, logs, generated outputs, or broad source trees,
  use file lists and fast search such as `rg` to narrow the relevant scope.
- Prefer targeted reads over bulk loading.
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

First, locate the runbook at `~/codex_projects/PROJECT_CREATION_RUNBOOK.md`.
Expand `~` to the current user's home directory before checking or creating
paths.

If the runbook exists:
1. Read `~/codex_projects/PROJECT_CREATION_RUNBOOK.md`.
2. Follow its `Progressive Intake Flow`.
3. Follow its `Response Consistency` rules unless there is a blocking issue or
   the user explicitly asks for a different style.
4. Reply in Korean: `새 프로젝트 생성을 준비합니다. 단계별로 필요한 정보만 확인하겠습니다.`
5. Use the runbook's fixed intake questions by default; skip questions only
   when the user already provided the information.
6. Ask only the next 2-3 necessary intake questions at a time.
7. Treat this as lightweight project work, not as a heavier planning
   framework, unless the user explicitly invokes another workflow.
8. Do not create the full project structure until the user approves the proposed
   project brief.
9. If design reference files are needed before full creation, create only the
   approved project root, `attachments/`, and `attachments/project-design/`;
   then inspect that folder's file list before proposing the project brief.
10. Immediately before creating approved Markdown files, read
    `~/codex_projects/PROJECT_FILE_SKELETONS.md` and use its skeletons exactly.

If the runbook does not exist, say so and ask the user for the correct runbook
path. Do not guess another location.

## Ongoing Codex Project Work

When the user asks to continue or work inside a project under `~/codex_projects`,
treat it as lightweight project work unless the user explicitly asks
for another workflow.

For ongoing work, keep context loading small:
1. Read the project's `NOTES.md` and `plans/STATUS.md` first.
2. Read `plans/REQUIREMENTS.md` and `plans/TRACEABILITY.md` only before creating
   outputs, judging completion, changing scope, or checking requirements.
3. Read `logs/LOG_TEMPLATE.md` only before writing a new log.
4. For project inputs under `attachments/`, `screenshots/`, or related code
   paths, inspect file lists first and choose only the files or sections needed
   for the current task.
5. Prefer existing summaries under `configs/{group}/` before rereading full
   PDFs, long documents, or large code files.

Common project tasks:
- For document analysis, inspect `attachments/` first.
- For image or screenshot analysis, inspect `screenshots/` first.
- For code analysis, inspect the related path with fast search or file lists
  before opening source files. When code context is large, create or update a
  `configs/{group}/SOURCE_INDEX.md` before deep file reads.
- Store generated analysis/config outputs under `configs/{group}/`.
- Store presentation outputs under `presentations/{group}/`.
- Store logs under `logs/{group}/` using the project's log template.
- After meaningful work, update `plans/STATUS.md`; update other `plans/` files
  only when their contents actually changed.

## Documentation Verification

For documentation-only or `codex_projects` project work, verification can
be limited to:
- confirming changed files exist;
- inspecting relevant Markdown sections;
- checking links and paths;
- confirming no unintended source/project files were modified.

Do not run code tests unless source code behavior changed.

## Reporting

For `codex_projects` project work, final reports should include:
- changed reference files;
- key rule or structure changes;
- verification performed;
- remaining usage notes or risks.
