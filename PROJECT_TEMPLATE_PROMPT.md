# Codex Project Template Design Notes

This file records the design intent behind the Codex project template. Routine
execution must use the canonical files below instead of this document.

## Canonical Sources

| Concern | Source |
| --- | --- |
| Install, update, quick usage | `README.md` |
| Legacy workspace transition | `LEGACY_MIGRATION.md` |
| Agent instruction source | `AGENTS_REQ.md` |
| Project creation flow | `PROJECT_CREATION_RUNBOOK.md` |
| Required project file skeletons | `PROJECT_FILE_SKELETONS.md` |
| Operating and maintenance rules | `OPERATING_GUIDE.md` |
| Version history | `PATH.md` |
| Manager setup and update | `setup.py` |
| Project migration | `migrate_projects.py` |

## Design Goals

The template creates a lightweight reference project folder for:

- input materials under `attachments/` and `screenshots/`;
- generated analysis under `configs/`;
- presentation outputs under `presentations/`;
- work logs under `logs/`;
- requirements, status, traceability, checklist, workflow, and decisions under
  `plans/`.

The manager and user projects are separated:

```text
{parent}/
├─ codex_project_manager/    Git-managed tool files
└─ codex_projects/           user-owned project workspace
```

Do not hard-code a specific user's home path in generated project files unless
the user explicitly asks for it.

## Creation Principles

- Start the project creation flow only from the exact trigger
  `새 프로젝트 생성`.
- Ask for project information progressively.
- Do not create the full project structure until the user approves the project
  brief.
- If design references are needed first, create only the project root,
  `attachments/`, and `attachments/project-design/`.
- Read `PROJECT_FILE_SKELETONS.md` immediately before writing approved project
  files.

## Project Identity

Every current project has `.codex-project.json`.

Required meaning:

- `schema`: identifies the file as a Codex Projects identity file.
- `version`: project structure version.
- `project_name`: human-readable project name.
- `project_folder`: actual folder name.
- `created_at`: creation date.

`project_folder` must match the folder name. Existing legacy projects can be
identified by `NOTES.md` and `plans/STATUS.md` until migrated.

## Operating Principles

- Load small context first: `NOTES.md`, then `plans/STATUS.md`.
- Read deeper planning files only when the task needs them.
- Inspect file lists before reading large documents, screenshots, logs, or
  source trees.
- Store reusable summaries and analysis under `configs/{group}/`.
- Store presentation outputs under `presentations/{group}/`.
- Store logs under `logs/{group}/`.
- Update `plans/STATUS.md` after meaningful work.
- Update traceability, requirements, decisions, and checklist files only when
  their content actually changes.

## Traceability Principles

Use stable IDs when requirements and verification matter:

- Requirement: `REQ-###`
- Acceptance criterion: `AC-###`
- Verification item: `VER-###`
- Decision: `DEC-###`

Trace only outputs that satisfy, verify, or materially support a requirement.
Do not trace every generated file by default.

Do not mark a requirement as `Satisfied` unless supporting outputs, logs,
verification evidence, and remaining checks are recorded.

## Audit Checklist

Before publishing a template change, check:

- README stays focused on installation and usage.
- Runbook owns the creation flow.
- Skeletons own exact file contents.
- AGENTS_REQ stays short enough for global instructions.
- setup updates manager/instructions without modifying user projects.
- migrate_projects preserves existing project documents.
- Legacy transition keeps project folders in place.
- Public docs contain no personal paths or temporary test paths.
