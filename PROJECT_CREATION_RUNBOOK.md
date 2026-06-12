# Project Creation Runbook

Use this short runbook when the user enters exactly:

```text
새 프로젝트 생성
```

This is the execution document for creating a new Codex project.
Use `PROJECT_TEMPLATE_PROMPT.md` only for design review. Read
`PROJECT_FILE_SKELETONS.md` only after the user approves project creation.

Path convention:
- `<CODEX_PROJECTS_ROOT>` is the absolute path of the installed
  `codex_projects` folder.
- Create new project folders under `<CODEX_PROJECTS_ROOT>`.
- Use `~/codex_projects` only when the user explicitly installed this template
  in the home directory.

## Response Consistency

When the user enters `새 프로젝트 생성`, reply in Korean:

```text
새 프로젝트 생성을 준비합니다. 단계별로 필요한 정보만 확인하겠습니다.
```

For normal intake steps:

```markdown
{short transition sentence}

1. {question 1}
2. {question 2}
```

Do not repeat known information during normal intake. Summarize only for
design-reference folder approval, project brief approval, blockers, or final
creation.

## Fixed Intake Questions

Step 1:

```markdown
프로젝트명과 폴더명을 알려주세요.

1. 프로젝트명:
2. 폴더명:
```

Step 2:

```markdown
관련 코드/저장소 경로를 알려주세요. 없다면 `none`이라고 입력해 주세요.
```

Step 3:

```markdown
프로젝트 설계에 참고할 PDF, 문서, 이미지, 캡처가 있나요?

1. `있음`: `attachments/project-design/` 폴더를 먼저 생성
2. `없음`: 설계 참고 파일 없이 진행
```

Step 4:

```markdown
프로젝트 목적과 초기 요구사항을 알려주세요.

1. 프로젝트 목적:
2. 초기 요구사항 1:
3. 초기 요구사항 2:
4. 초기 요구사항 3:
```

Step 5:

```markdown
아래 생성안을 확인해 주세요.

1. `승인`: 이대로 생성
2. `수정`: 수정할 내용 전달
3. `보류`: 생성 중단
```

## Progressive Intake Flow

1. Identify the project.
   - Use Step 1.
   - If the user gives only a project name, propose a safe folder name and ask
     for confirmation.

2. Locate related code context.
   - Use Step 2.
   - If a path is provided, check whether it exists.
   - Record the path only; do not modify files in the related code path.
   - Do not read the full source tree during intake.

3. Collect design reference materials when needed.
   - Use Step 3.
   - After the project folder name is known and the user agrees, create only:
     - `<CODEX_PROJECTS_ROOT>/{project folder name}/`
     - `<CODEX_PROJECTS_ROOT>/{project folder name}/attachments/`
     - `<CODEX_PROJECTS_ROOT>/{project folder name}/attachments/project-design/`
   - Ask the user to place design reference files in
     `attachments/project-design/`.
   - Inspect the file list before proposing the project brief.
   - Inspecting the reference file list during intake does not mark Analysis
     checklist items as complete.
   - Do not create `.codex-project.json`, `plans/`, `configs/`,
     `presentations/`, `logs/`, or `NOTES.md` before project brief approval.

4. Define harness intent.
   - Use Step 4.
   - Convert requirements into stable `REQ-###` IDs and initial `AC-###` items.

5. Propose the project brief.
   - Include project name, folder name, code path, reference scope, purpose,
     requirements, output grouping, and files to be created.
   - Use this response structure:

```markdown
프로젝트 생성안

요약:
- Project:
- Folder:
- Code path:
- Reference scope:
- Output grouping:

Requirements:
- `REQ-001`:
- `REQ-002`:

생성 예정:
- `...`

선택해 주세요:
1. `승인`: 이대로 생성
2. `수정`: 수정할 내용 전달
3. `보류`: 생성 중단
```

6. Create the project only after approval.
   - Create only approved folders and project files.
   - When possible, write approved project files directly to disk.
   - Do not print full generated file contents in chat unless the user
     explicitly asks for them.
   - If the environment cannot write files directly, create content in small
     batches so output limits do not truncate the documents.
   - Read `PROJECT_FILE_SKELETONS.md` immediately before writing project files.
   - Use those skeletons exactly; fill unknown fields with `None`,
     `Not started`, `No outputs yet`, `No logs yet`, or `To be determined`.
   - Create `.codex-project.json` as valid JSON with `schema` set to
     `codex_projects`, `version` set to `1`, `project_name` set to the approved
     project name, `project_folder` set to the approved folder name, and
     `created_at` set to `{YYYY-MM-DD}`.
   - Do not omit required JSON keys, Markdown sections, or required tables.
   - Set `plans/STATUS.md` to the Intake phase and preserve the required
     resume headings: `Last Updated`, `Current State`, `Last Completed`,
     `Next Action`, and `Blocked By`.
   - Record the initial setup decision in `plans/DECISIONS.md`.

## Required Structure

Create this structure after approval:

- `<CODEX_PROJECTS_ROOT>/{project folder name}/`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/.codex-project.json`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/attachments/`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/screenshots/`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/plans/`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/configs/`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/presentations/`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/logs/`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/NOTES.md`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/plans/REQUIREMENTS.md`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/plans/WORKFLOW.md`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/plans/CHECKLIST.md`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/plans/TRACEABILITY.md`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/plans/STATUS.md`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/plans/DECISIONS.md`
- `<CODEX_PROJECTS_ROOT>/{project folder name}/logs/LOG_TEMPLATE.md`

## Creation Checks

Before creating or editing anything:

1. Check that `<CODEX_PROJECTS_ROOT>` exists.
2. Check whether the related code path exists, unless it is `none`.
3. Check whether the target project folder already exists.
4. If it already exists, do not overwrite existing files. Inspect the structure
   and add only missing folders or missing project files.
5. If `.codex-project.json` already exists, confirm it is valid JSON with
   `schema: "codex_projects"` and `project_folder` matching the target folder
   name. If it conflicts, stop and ask the user how to proceed.
6. Briefly report what will be created before making changes.

For completion, respond in this structure:

```markdown
생성 완료

생성한 항목:
- `...`

검증:
- {verification summary}

다음 작업:
- {recommended next action}
```

Report created paths and verification results, not the full contents of every
generated file.
