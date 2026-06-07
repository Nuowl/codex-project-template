# Project File Skeletons

Use these skeletons when creating a new project. They are mandatory for initial
project creation. Keep headings and required tables even when some values are
not known yet.

## `NOTES.md`

```markdown
# {Project Name} Codex Project Notes

This directory is a lightweight project workspace for {project purpose}.

## Current Goal

{current goal}

## Related Code Path

- {related code path or `none`}

## External Reference Info

- {external reference summary or `None`}

## Known Context

- {known context item 1}
- {known context item 2}

## Context Loading Policy

- Start ongoing work by reading only `NOTES.md` and `plans/STATUS.md`.
- Before large document or code analysis, inspect file lists first.
- Prefer existing summaries under `configs/{group}/` before rereading full
  source documents or large code files.

## Context Reuse Policy

- Do not read previous full logs by default.
- Check `plans/STATUS.md` for `Latest Log` first.
- Read only the specific log needed for the current task.
- If a long log is repeatedly needed, summarize it under
  `configs/{group}/summary.md`.

## Planning Files

- `plans/REQUIREMENTS.md`: requirements and acceptance criteria
- `plans/WORKFLOW.md`: workflow phases and expected outputs
- `plans/CHECKLIST.md`: setup, analysis, output, verification, and handoff checks
- `plans/TRACEABILITY.md`: requirement-to-output and verification mapping
- `plans/STATUS.md`: current state and next action
- `plans/DECISIONS.md`: significant decisions

## Reference File Layout

- `attachments/`: source papers, documents, manuals, and uploaded references.
- `screenshots/`: screenshots, diagrams, GIFs, UI captures, and visual references.
- `configs/`: analysis notes, summaries, converted files, extracted data, and configuration-like outputs.
- `presentations/`: slide decks, scripts, speaker notes, and presentation assets.
- `logs/`: dated work logs, verification notes, and user-facing summaries.

## Checks Done

- Project structure initialized.
- Required planning documents created.
- Reference inputs inspected: {yes/no and short detail}

## Remaining Checks

- {remaining check or `None`}
```

## `plans/REQUIREMENTS.md`

```markdown
# Requirements

## Scope

{scope summary}

## Requirements

### REQ-001: {requirement title}

{requirement description}

Acceptance criteria:
- `AC-001`: {acceptance criterion}
- `AC-002`: {acceptance criterion}

## Out Of Scope

- {out-of-scope item or `None identified`}
```

## `plans/WORKFLOW.md`

```markdown
# Workflow

| Phase | Status | Expected Inputs | Expected Outputs |
| --- | --- | --- | --- |
| Intake | In progress | User intake answers, reference file list | Initialized project structure |
| Analysis | Not started | `attachments/`, `screenshots/`, relevant plan files | `configs/{group}/...` |
| Review | Not started | Analysis outputs, user feedback | Updated requirements/status/checklist |
| Output Generation | Not started | Approved analysis and requirements | `presentations/{group}/...` or other requested outputs |
| Handoff | Not started | Generated outputs and verification notes | Final summary and updated logs |

## Phase Notes

### Intake

- Confirm project purpose, source materials, related paths, and output grouping.

### Analysis

- Inspect relevant inputs before detailed analysis.
- Create structured notes under `configs/{group}/`.

### Review

- Review analysis with the user before producing downstream deliverables.

### Output Generation

- Create only approved outputs in the appropriate output folder.

### Handoff

- Update status, checklist, traceability, and logs before reporting completion.
```

## `plans/CHECKLIST.md`

```markdown
# Checklist

## Intake

- [x] Project name confirmed.
- [x] Folder name confirmed.
- [x] Related code path checked or marked as `none`.
- [x] Reference material handling confirmed.
- [x] Initial requirements captured.
- [x] Project initialization completed.

## Analysis

- [ ] Analysis input scope confirmed.
- [ ] Required context documents read.
- [ ] Analysis outputs created under `configs/{group}/`.
- [ ] Requirement coverage checked.

## Output Generation

- [ ] Output group selected.
- [ ] Deliverables created under the correct folder.
- [ ] Generated outputs linked in `plans/TRACEABILITY.md`.

## Verification And Handoff

- [ ] Verification evidence recorded.
- [ ] Log created from `logs/LOG_TEMPLATE.md`.
- [ ] `plans/STATUS.md` updated.
- [ ] Remaining risks or checks reported.
```

## `plans/TRACEABILITY.md`

```markdown
# Traceability

| Requirement ID | Acceptance Criteria | Output Files | Log Files | Verification Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| `REQ-001` | `AC-001`, `AC-002` | Not created yet | Not created yet | Not recorded yet | Not started |

## Source References

| Source | Purpose |
| --- | --- |
| {source path or `None`} | {purpose or `None`} |
```

## `plans/STATUS.md`

```markdown
# Status

Last reviewed: {YYYY-MM-DD}

## Current Phase

Intake

## Active Output Group

Not selected yet

## Latest Generated Output

No outputs yet

## Latest Log

No logs yet

## Current State

- Project reference structure has been initialized.
- Related code path: {related code path or `none`}
- Reference inputs: {reference input summary}

## Blockers

- {blocker or `None`}

## Next Action

{next action}
```

## `plans/DECISIONS.md`

```markdown
# Decisions

| Date | Decision ID | Decision | Rationale | Impact |
| --- | --- | --- | --- | --- |
| {YYYY-MM-DD} | `DEC-001` | Initialize `{Project Name}` project workspace. | User approved the project brief. | Creates the baseline folder structure, planning documents, and output rules. |
```

## `logs/LOG_TEMPLATE.md`

```markdown
# {YYYY-MM-DD} {Task Title}

## English Working Record

### User Request

### Requirement IDs

### Context

### Input Files Used

### Generated Files

### Updated Planning Files

### Work Performed

### Verification

### Remaining Checks

## Korean User Summary

### 요청 요약

### 관련 요구사항 ID

### 사용한 입력 파일

### 생성한 결과물

### 갱신한 계획 문서

### 작업 요약

### 검증 결과

### 남은 확인 사항
```

## Optional `configs/{group}/SOURCE_INDEX.md`

Use this optional template before deep code analysis when the related code path
is large or likely to be reused.

```markdown
# Source Index

## Related Code Path

- `{path}`

## Purpose

- {why this code path matters}

## Important Folders

- `{folder}`: {role}

## Likely Relevant Files

- `{file}`: {reason}

## Excluded By Default

- `.git/`
- `node_modules/`
- `dist/`
- `build/`
- large binary files
- generated files

## Next Read Candidates

- `{file or folder}`: {reason}
```
