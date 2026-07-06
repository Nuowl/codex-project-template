# Codex Project Template 운영 가이드

이 문서는 README보다 깊은 운영 기준을 다룹니다. 일반 사용자는 README만
보면 됩니다.

---

## 현재 구조

```text
{parent}/
├─ codex_project_manager/    GitHub에서 갱신하는 관리 도구
└─ codex_projects/           사용자가 만든 프로젝트 workspace
```

- manager에는 템플릿 문서, 설치 스크립트, 마이그레이션 스크립트만 둡니다.
- workspace에는 사용자가 만든 프로젝트만 둡니다.
- manager 업데이트는 workspace 안의 프로젝트 파일을 수정하지 않습니다.

---

## 문서 역할

| 파일                            | 역할                                      |
| ------------------------------- | ----------------------------------------- |
| `README.md`                   | 설치, 업데이트, 빠른 사용법               |
| `LEGACY_MIGRATION.md`         | 자동화 적용 전 설치를 최신 구조로 전환    |
| `AGENTS_REQ.md`               | `setup.py`가 Codex 지침에 설치하는 원본 |
| `PROJECT_CREATION_RUNBOOK.md` | `새 프로젝트 생성` 질문과 승인 흐름     |
| `PROJECT_FILE_SKELETONS.md`   | 새 프로젝트 필수 파일의 실제 skeleton     |
| `PROJECT_TEMPLATE_PROMPT.md`  | 구조 설계 의도와 감사 기준                |
| `PATH.md`                     | 버전별 변경 요약                          |
| `setup.py`                    | manager 설치, 업데이트, 지침 설치         |
| `migrate_projects.py`         | 기존 프로젝트 구조 점검과 갱신            |

평소 실행 흐름에서는 `PROJECT_TEMPLATE_PROMPT.md`를 읽지 않습니다.
새 프로젝트 생성은 runbook이 담당하고, 파일 내용은 skeleton이 담당합니다.

---

## 자동화 흐름

`setup.py` 최초 실행:

1. manager와 workspace 경로를 확인합니다.
2. workspace가 없으면 생성합니다.
3. `~/.codex/codex-projects.json`에 두 경로를 저장합니다.
4. `AGENTS_REQ.md`를 읽어 `~/.codex/AGENTS.md`의 managed block에
   설치합니다.

`setup.py` 재실행:

1. 기존 설정을 읽습니다.
2. manager Git 원격, branch, tracked file 변경 여부를 확인합니다.
3. fast-forward 가능한 업데이트만 적용합니다.
4. 업데이트된 `setup.py`를 다시 실행합니다.
5. 설정과 managed instructions를 갱신합니다.

`setup.py`는 프로젝트 구조 마이그레이션을 자동 실행하지 않습니다.
프로젝트 갱신은 사용자가 `migrate_projects.py`를 명시적으로 실행해야
합니다.

---

## 레거시 전환

자동화 적용 전 `codex_projects` 폴더에는 템플릿 파일과 프로젝트 폴더가
섞여 있을 수 있습니다.

`setup.py --adopt-legacy`는 workspace 루트의 구버전 템플릿 구성 파일만
별도 폴더로 정리합니다. 작업 중인 프로젝트 폴더는 그대로 둡니다.

자세한 명령은 `LEGACY_MIGRATION.md`가 기준입니다.

---

## 프로젝트 마이그레이션

`migrate_projects.py` 기본 실행은 미리보기입니다. 실제 변경은 `--apply`
옵션이 있을 때만 수행합니다.

마이그레이션 원칙:

- 기존 Markdown을 skeleton으로 덮어쓰지 않습니다.
- 누락된 폴더, 누락된 파일, 필수 heading만 추가합니다.
- 적용 중 변경 전 파일은 `.codex-project-backups/`에 임시 저장합니다.
- 성공 후 사용자가 동의하면 마이그레이션 백업과 레거시 템플릿 백업을
  삭제합니다.
- symlink project, 잘못된 `.codex-project.json`, workspace 밖 경로는
  conflict로 처리합니다.

마이그레이션 판정 종류:

| 판정 | 의미 | 처리 |
| --- | --- | --- |
| `current` | 최신 manager 기준과 일치하는 프로젝트 | 변경하지 않음 |
| `legacy` | 자동 보완 가능한 차이가 있는 프로젝트 | 변경 개수를 표시하고 `--apply`에서 필요한 항목만 추가 |
| `unrelated` | Codex 프로젝트가 아닌 폴더 | 변경하지 않음 |
| `conflicting` | 자동 보완이 위험한 폴더 | 변경하지 않고 오류 표시 |

판정 기준은 아래 순서로 적용합니다.

| 판정 | 조건 |
| --- | --- |
| `current` | 프로젝트 식별 정보, schema number, `manager_version`, 필수 폴더·파일, `STATUS.md` heading이 모두 현재 manager 기준과 일치 |
| `legacy` | 현재 manager 기준과 다른 항목이 있지만 자동 보완 가능 |
| `conflicting` | 자동 보완이 위험하거나 identity가 잘못됨 |
| `unrelated` | 프로젝트 식별 근거가 없음 |

`legacy` 예시는 다음과 같습니다.

- `.codex-project.json`은 없지만 `NOTES.md`가 있음
- 예전 identity 키 `version`이 남아 있어 `schema_version`으로 바꿔야 함
- `manager_version`이 현재 manager와 다름
- 필수 폴더, 필수 파일, `plans/STATUS.md` 필수 heading이 누락됨

`conflicting` 예시는 다음과 같습니다.

- `plans/STATUS.md`만 있고 `NOTES.md`가 없음
- symlink project
- 잘못된 identity
- 지원 schema number보다 높은 값

---

## 프로젝트 구조

| 경로                    | 역할                              |
| ----------------------- | --------------------------------- |
| `.codex-project.json` | 프로젝트 식별 파일                |
| `NOTES.md`            | 프로젝트 개요와 주요 링크         |
| `attachments/`        | 문서형 입력 자료                  |
| `screenshots/`        | 이미지형 입력 자료                |
| `configs/`            | 분석, 요약, 변환 결과             |
| `presentations/`      | 발표 자료                         |
| `logs/`               | 작업 기록                         |
| `plans/`              | 요구사항, 상태, 추적성, 결정 기록 |

`.codex-project.json`의 `project_folder`는 실제 폴더명과 일치해야 합니다.

---

## 프로젝트 작업 루프

실제 프로젝트 작업을 할 때만 상태 루프를 실행합니다. 설치, 업데이트,
템플릿 설명, 일반 브레인스토밍에는 실행하지 않습니다.

기본 읽기 순서:

1. 항상 `NOTES.md`와 `plans/STATUS.md`를 먼저 읽습니다.
2. 산출물 생성, 완료 판단, 범위 변경 전에는 `plans/REQUIREMENTS.md`를
   읽습니다.
3. 산출물, 로그, 검증 근거를 요구사항에 연결할 때는
   `plans/TRACEABILITY.md`를 읽습니다.
4. 기존 결정과 충돌할 수 있으면 `plans/DECISIONS.md`를 읽습니다.
5. 단계나 workflow를 바꾸면 `plans/WORKFLOW.md`를 읽습니다.
6. 체크리스트 진행을 바꾸면 `plans/CHECKLIST.md`를 읽습니다.
7. 새 로그 작성 직전에만 `logs/LOG_TEMPLATE.md`를 읽습니다.

의미 있는 작업 후:

- `plans/STATUS.md`를 갱신합니다.
- 산출물, 로그, 검증 근거, 요구사항 상태가 바뀌면
  `plans/TRACEABILITY.md`를 갱신합니다.
- 요구사항, 완료 기준, 범위가 바뀌면 `plans/REQUIREMENTS.md`와
  `plans/DECISIONS.md`를 갱신합니다.
- 단계나 workflow가 바뀌면 `plans/WORKFLOW.md`를 갱신합니다.
- 체크리스트 항목이 실제로 바뀐 경우에만 `plans/CHECKLIST.md`를
  갱신합니다.

`plans/STATUS.md`에는 아래 heading을 유지합니다.

- `Last Updated`
- `Current State`
- `Last Completed`
- `Next Action`
- `Blocked By`

---

## 출력 위치

| 출력                       | 위치                       |
| -------------------------- | -------------------------- |
| 일반 분석, 요약, 변환 결과 | `configs/{group}/`       |
| 발표 자료                  | `presentations/{group}/` |
| 작업 로그                  | `logs/{group}/`          |

기본 group 기준은 주제, 챕터, 모듈입니다. 기준이 애매하면
`YYYY-MM-DD-topic` 형식을 사용합니다.

---

## 토큰 절약 근거

이 템플릿은 필요한 근거를 단계적으로 좁혀 토큰 사용량을 줄입니다.

- `NOTES.md`와 `plans/STATUS.md`만 먼저 읽어 현재 목표, 마지막 작업,
  다음 행동을 복구합니다.
- 나머지 planning 파일은 산출물 생성, 완료 판단, 범위 변경, 결정 충돌
  같은 조건이 있을 때만 읽습니다.
- `attachments/`, `screenshots/`, source tree는 원문을 바로 열지 않고
  파일 목록과 검색으로 후보를 줄입니다.
- 반복해서 쓰는 큰 입력은 `configs/{group}/`의 요약, 비교표,
  `SOURCE_INDEX.md`로 재사용합니다.
- 로그에는 전체 원문을 반복하지 않고 입력, 생성 파일, 결정, 검증,
  남은 확인 사항을 기록합니다.
- 정확도, 안전, 사용자에게 보이는 산출물이 걸린 판단은 요약만 믿지
  않고 원문이나 실제 소스 섹션을 다시 확인합니다.
- 검증은 토큰 절약을 이유로 생략하지 않습니다.

---

## 다른 에이전트로 적용할 때

Codex에서는 `setup.py`가 `AGENTS_REQ.md`를 읽고 실제 지침 파일에 자동으로
managed block을 설치합니다. 다른 에이전트에는 이 자동 설치가 그대로
동작하지 않을 수 있습니다.

다른 에이전트로 옮길 때는 아래 순서로 적용합니다.

1. manager 폴더와 workspace 폴더를 먼저 분리합니다.
2. 해당 에이전트가 읽는 전역 지침 또는 프로젝트 지침 위치를 확인합니다.
3. `AGENTS_REQ.md`의 내용을 그 지침 위치에 넣습니다.
4. `<CODEX_PROJECT_MANAGER_ROOT>`를 실제 manager 절대경로로 바꿉니다.
5. `<CODEX_PROJECTS_WORKSPACE_ROOT>`를 실제 workspace 절대경로로 바꿉니다.
6. 그 에이전트가 로컬 파일 읽기와 파일 생성을 지원하는지 확인합니다.

최소 이식 규칙:

```text
When the user enters exactly "새 프로젝트 생성", read
<CODEX_PROJECT_MANAGER_ROOT>/PROJECT_CREATION_RUNBOOK.md and follow it.
Before creating project files, read
<CODEX_PROJECT_MANAGER_ROOT>/PROJECT_FILE_SKELETONS.md.
Create projects only under <CODEX_PROJECTS_WORKSPACE_ROOT>.
```

로컬 파일을 자동으로 읽지 못하는 에이전트라면 사용자가 runbook과 skeleton
내용을 직접 제공해야 합니다. 파일을 직접 생성하지 못하는 에이전트라면
생성할 내용을 제안하게 하고, 사용자가 별도로 저장해야 합니다.

다른 언어 사용자에게 배포할 때는 `AGENTS_REQ.md`,
`PROJECT_CREATION_RUNBOOK.md`, `PROJECT_FILE_SKELETONS.md`의 사용자-facing
문장을 함께 번역해야 합니다. 경로 placeholder와 파일명은 번역하지
마세요.

---

## 유지보수 체크

- 생성 질문이나 승인 흐름을 바꾸면 `PROJECT_CREATION_RUNBOOK.md`를
  갱신합니다.
- 생성 파일 구조를 바꾸면 `PROJECT_FILE_SKELETONS.md`와
  `migrate_projects.py`를 함께 확인합니다.
- 전역 지침 규칙을 바꾸면 `AGENTS_REQ.md`와 `manager_common.py`의
  설치 로직을 함께 확인합니다.
- manager/workspace 경로 규칙을 바꾸면 `setup.py`, `AGENTS_REQ.md`,
  README를 함께 확인합니다.
- 공개 버전 변경은 `PATH.md`에 짧게 기록합니다.
- 공개 문서에는 개인 경로, 테스트 경로, 계정명을 남기지 않습니다.

검증 기준:

- 문서만 바꿨으면 Markdown fence, 링크, 경로 문구를 확인합니다.
- setup/migration 코드를 바꿨으면 unit test와 ruff를 실행합니다.
- 레거시 전환을 바꿨으면 임시 HOME/workspace에서 실제 명령 흐름을
  재현합니다.
