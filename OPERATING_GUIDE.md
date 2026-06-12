# Codex Project Template 운영 가이드

이 문서는 README에서 분리한 세부 운영 기준입니다. 처음 설치하거나 새 프로젝트를 만들 때 반드시 전부 읽을 필요는 없습니다.

## 템플릿 문서 역할

README는 설치, 빠른 사용법, 트러블슈팅만 다룹니다. 작동 원리, 문서 역할,
토큰 최적화, 다른 에이전트 응용 기준은 이 운영 가이드에서 관리합니다.

| 문서 | 용도 |
| --- | --- |
| `README.md` | 사람을 위한 빠른 설치, 사용법, 트러블슈팅 |
| `AGENTS_REQ.md` | 실제 Codex 지시 파일에 복사할 최소 규칙 원본 |
| `PROJECT_CREATION_RUNBOOK.md` | `새 프로젝트 생성` 실행 절차, 고정 질문, 승인 흐름 |
| `PROJECT_FILE_SKELETONS.md` | 필수 JSON/Markdown 파일의 내부 구조 |
| `PROJECT_TEMPLATE_PROMPT.md` | 전체 설계 의도, 구조 감사 기준, 장기 유지보수 기준 |
| `OPERATING_GUIDE.md` | 운영 기준, 상태 루프, 토큰 최적화, 다른 에이전트 응용 참고 |
| `PATH.md` | 공개 버전별 변경 요약과 갱신 참고 |

일반적인 `새 프로젝트 생성` 흐름에서는 `PROJECT_CREATION_RUNBOOK.md`를 먼저
읽고, 프로젝트 파일 생성 직전에만 `PROJECT_FILE_SKELETONS.md`를 읽도록
설계되어 있습니다. `PROJECT_TEMPLATE_PROMPT.md`는 구조를 변경하거나 생성
결과를 감사할 때 사용하는 설계 문서입니다.

## 생성되는 기본 구조

| 구분 | 폴더 또는 파일 | 용도 |
| --- | --- | --- |
| 첨부용 | `attachments/` | PDF, Word, 논문, 매뉴얼, 외부 문서 |
| 첨부용 | `attachments/project-design/` | 생성 전 설계 참고 자료 |
| 첨부용 | `screenshots/` | 이미지, 캡처, GIF, 도표 |
| 계획 | `plans/` | 요구사항, 진행 상태, 추적표, 결정 기록 |
| 출력물 | `configs/` | 분석 결과, 요약, 변환 결과, 설정 파일 |
| 출력물 | `presentations/` | 발표 자료, 발표 스크립트 |
| 출력물 | `logs/` | 작업 기록과 검증 결과 |
| 기준 파일 | `.codex-project.json` | 에이전트가 프로젝트 루트를 식별하는 기계용 메타데이터 |
| 기준 문서 | `NOTES.md` | 프로젝트 개요와 주요 링크 |

## `plans/` 문서의 역할

| 파일 | 용도 |
| --- | --- |
| `plans/REQUIREMENTS.md` | 프로젝트 요구사항과 완료 기준 |
| `plans/WORKFLOW.md` | 전체 진행 과정 설계와 단계별 계획 |
| `plans/TRACEABILITY.md` | 요구사항, 산출물, 로그, 검증 근거 연결 |
| `plans/CHECKLIST.md` | 단계별 체크리스트 |
| `plans/STATUS.md` | 현재 상태, 마지막 완료 작업, blocker, 다음 작업 |
| `plans/DECISIONS.md` | 중요한 결정과 그 이유 |

`NOTES.md`는 길게 작성하지 않고, 프로젝트 전체를 빠르게 파악하는 인덱스 역할만 하도록 유지합니다. 자세한 요구사항, 진행 상태, 체크리스트, 결정 기록은 `plans/` 폴더의 각 문서에 나누어 관리합니다.

## 기본 운영 기준

- 요구사항은 `REQ-001`, 완료 기준은 `AC-001`, 검증은 `VER-001`처럼 ID를 붙입니다.
- 요구사항을 만족하거나 검증하거나 실질적으로 뒷받침하는 산출물만 `plans/TRACEABILITY.md`에 연결합니다.
- 요구사항을 `Satisfied`로 바꾸려면 산출물, 로그, 검증 근거, 남은 확인 사항 상태가 모두 기록되어 있어야 합니다.
- 요구사항이나 완료 기준이 바뀌면 `REQUIREMENTS.md`, `DECISIONS.md`, `TRACEABILITY.md`, `STATUS.md`를 필요한 만큼 갱신합니다.
- `STATUS.md`에는 시작점 복구를 위한 최소 heading인 `Last Updated`,
  `Current State`, `Last Completed`, `Next Action`, `Blocked By`를 유지합니다.
- `DECISIONS.md`에는 중요한 결정만 영향 범위와 함께 기록합니다.
- `configs/`와 `logs/`는 같은 그룹 기준을 사용합니다.
- 기본 그룹 기준은 “챕터/주제 우선, 애매하거나 시간 흐름이 중요하면 날짜+주제”입니다.
- 발표 산출물은 항상 `presentations/{group}/` 아래에 저장합니다.
- 모든 로그는 `logs/LOG_TEMPLATE.md` 형식을 따르며, 영어 작업 기록과 한국어 요약을 함께 포함합니다.
- 새 프로젝트 루트에는 `.codex-project.json`을 두고, `schema`,
  `version`, `project_name`, `project_folder`, `created_at`을 기록합니다.
- `.codex-project.json`의 `project_folder`는 실제 폴더명과 일치해야 합니다.

## 프로젝트 상태 루프 기준

기존 Codex 프로젝트 작업에서는 에이전트가 모델 기억에만 의존하지 않도록
상태 루프를 사용합니다. 상태 루프는 특정 프로젝트의 실제 작업에만
적용합니다.

상태 루프를 실행하는 경우:

- 기존 Codex 프로젝트를 이어서 진행할 때
- 프로젝트 산출물을 생성, 수정, 검토할 때
- `attachments/`, `screenshots/`, 관련 경로의 입력 자료를 분석할 때
- 상태, 요구사항, 추적표, 결정, 로그, 발표 자료를 갱신할 때
- 완료 여부, 검증 결과, 요구사항 만족 여부를 판단할 때
- 기존 작업을 Codex 프로젝트 구조로 정리할 때

상태 루프를 실행하지 않는 경우:

- 템플릿 자체에 대한 질문이나 수정
- 설치, 설정, 업데이트, 공유 방법 안내
- 일반 설명, 브레인스토밍, 설계 논의
- 특정 Codex 프로젝트와 무관한 코딩 작업

상태 루프를 실행할 때는 먼저 작업 대상 프로젝트 폴더를 확정합니다. 프로젝트
이름, 사용자가 가리킨 파일/폴더, 현재 작업 위치, 최근 대화 맥락, 유일한
폴더명 매칭을 기준으로 하나의 프로젝트가 정해질 때만 진행합니다. 후보가
없거나 여러 개면 임의의 `plans/` 파일을 읽거나 수정하지 말고 사용자에게
어떤 프로젝트인지 확인합니다.

프로젝트 폴더 후보가 정해지면 `plans/`를 읽기 전에 `.codex-project.json`을
확인합니다. 이 파일이 있고 `schema`가 `codex_projects`이며
`project_folder`가 실제 폴더명과 일치하면 해당 폴더를 Codex 프로젝트로
사용합니다. 오래된 프로젝트처럼 `.codex-project.json`이 없다면
`NOTES.md`와 `plans/STATUS.md`가 있을 때만 legacy Codex 프로젝트로
취급합니다. 식별자 파일 누락은 작업에 영향을 주거나 사용자가 루프/상태
세부 정보를 요청했을 때만 보고합니다.

상태 파일 로딩 기준:

| 상황 | 확인하는 문서 |
| --- | --- |
| 모든 실제 프로젝트 작업 | `NOTES.md`, `plans/STATUS.md` |
| 산출물 생성, 완료 판단, 범위 변경, 요구사항 만족 확인 | `plans/REQUIREMENTS.md` |
| 산출물, 로그, 검증 근거, 요구사항 상태 연결 | `plans/TRACEABILITY.md` |
| 기존 결정 변경 또는 결정 충돌 가능성 | `plans/DECISIONS.md` |
| 단계나 workflow 구조 변경 | `plans/WORKFLOW.md` |
| 체크리스트나 단계 진행 표시 | `plans/CHECKLIST.md` |
| 새 로그 작성 | `logs/LOG_TEMPLATE.md` |

의미 있는 작업의 기준은 프로젝트 상태를 새로 정하거나 바꾸는 것입니다.
현재 단계, 산출물, 최신 로그, 요구사항, 추적성, 검증 근거, 결정, blocker,
reference path, output group, next action 중 하나라도 바뀌면 의미 있는
작업입니다. 단순 설명, 템플릿 논의, 설치 안내, 상태 변화 없는 파일 확인은
프로젝트 상태 갱신 대상이 아닙니다.

`plans/STATUS.md`를 갱신할 때는 아래 heading을 삭제하거나 이름을 바꾸지
않습니다. 필요한 세부 정보는 각 heading 아래에 bullet로 추가합니다.

- `Last Updated`
- `Current State`
- `Last Completed`
- `Next Action`
- `Blocked By`

## 보장 수준과 한계

이 템플릿은 Markdown 문서와 Codex 지침을 조합해 상태 재확인 루프를 만드는
lightweight harness 구조입니다. 별도 실행 프로그램이 아니므로 모든 요청에서
상태 루프를 물리적으로 강제하지는 않습니다.

보장하는 것:

- `AGENTS_REQ.md`가 실제 Codex 지침에 들어가 있으면 `새 프로젝트 생성`
  트리거와 기존 프로젝트 상태 루프 기준을 제공합니다.
- 상태 루프가 실행되면 `.codex-project.json`, `NOTES.md`,
  `plans/STATUS.md`를 기준으로 작업 대상과 시작점을 다시 확인합니다.
- 의미 있는 작업 후에는 `plans/STATUS.md`를 중심으로 다음 작업과 blocker를
  남기도록 설계되어 있습니다.

보장하지 않는 것:

- Codex 지침 파일이 설치되지 않았거나 오래된 경우에는 자동으로 동작하지
  않습니다.
- 매우 긴 대화에서 모델이 전역 지침을 약하게 따르는 문제를 Markdown만으로
  완전히 막을 수는 없습니다.
- 외부 hook, runner, CLI wrapper가 없으면 상태 루프 실행 여부를 시스템
  차원에서 강제 검증하지는 못합니다.

더 강한 강제 실행이 필요하다면 이 템플릿을 그대로 유지하되, 별도의
hook/runner에서 요청 전후로 프로젝트 루트 식별, 상태 파일 확인, 상태 파일
갱신 여부 검사를 수행하는 방식이 필요합니다.

## 최소 Handoff 기준

모든 상태 문서를 매번 강제로 갱신하기보다 `plans/STATUS.md` 중심의
최소 갱신 방식을 권장합니다. 이렇게 하면 긴 작업 뒤에 문서 간
동기화가 어긋날 가능성을 줄일 수 있습니다.

- 의미 있는 작업 후에는 최소한 `plans/STATUS.md`를 갱신합니다. 단,
  상태 변화가 없는 단순 확인이나 설명만 한 경우에는 갱신하지 않습니다.
- 산출물이나 검증 근거가 생겼을 때만 `plans/TRACEABILITY.md`를
  갱신합니다.
- 요구사항, 완료 기준, 범위가 바뀐 경우에만 `plans/REQUIREMENTS.md`와
  `plans/DECISIONS.md`를 갱신합니다.
- 체크리스트 항목이 실제로 완료되었거나 새 점검 항목이 생긴 경우에만
  `plans/CHECKLIST.md`를 갱신합니다.

작업 완료를 보고하기 전에는 최소한 아래만 확인합니다.

1. `plans/STATUS.md`: `Current State`, `Last Completed`, `Next Action`,
   `Blocked By`, `Last Updated`가 현재 작업 상태와 맞는지
2. 관련 log: 작업 내용, 입력 파일, 생성 파일, 검증 결과가 기록되었는지
3. 필요한 `plans/TRACEABILITY.md`: 산출물이나 검증 근거가 요구사항을
   만족하거나 뒷받침할 때만 연결되었는지

## 유지보수 유의사항

새 프로젝트 생성 안정성을 유지하려면 위의 문서 역할 구분을 지키고,
변경 범위에 맞는 파일을 함께 확인합니다. 일반적인 `새 프로젝트 생성`
흐름에서는 `PROJECT_TEMPLATE_PROMPT.md`를 먼저 읽을 필요가 없습니다.
이 파일은 구조를 변경하거나 생성 결과를 감사할 때 사용합니다.

구조나 생성 규칙을 바꿀 때는 한 파일만 수정하지 마세요.

- 생성 질문, 승인 흐름, 필수 폴더/파일 목록을 바꾸면 `PROJECT_CREATION_RUNBOOK.md`와 `PROJECT_TEMPLATE_PROMPT.md`를 함께 확인합니다.
- 필수 JSON/Markdown 파일의 내부 구조를 바꾸면 `PROJECT_FILE_SKELETONS.md`와 `PROJECT_TEMPLATE_PROMPT.md`의 파일 역할 설명을 함께 확인합니다.
- 트리거 경로나 읽기 순서를 바꾸면 `AGENTS_REQ.md`와 실제 사용하는 에이전트 지시 파일을 함께 갱신합니다.
- 설치 루트 표기인 `<CODEX_PROJECTS_ROOT>`를 바꾸면 README에 적힌 경로 안내도 함께 갱신합니다.
- 공개 배포 기준의 패치 내용을 바꾸면 `PATH.md`에 버전별 변경 요약을
  남기고, README 상단의 현재 패치 버전 안내도 함께 확인합니다.

이 분리는 토큰 사용량을 줄이기 위한 것입니다. 전역 지침에는 짧은
트리거와 안전 규칙만 두고, 실행 중에는 짧은 runbook과 필요 시 skeleton만
읽으며, 긴 설계 문서는 평소에 읽지 않는 구조를 유지하는 것이 좋습니다.

수정 후에는 아래 항목을 확인합니다.

- README가 설치, 지침 추가, 기본 사용법, 트러블슈팅 중심으로 유지되는지
- `AGENTS_REQ.md`가 실제 에이전트 지침으로 쓰기에 과하게 길어지지 않았는지
- `PROJECT_CREATION_RUNBOOK.md`의 생성 절차와
  `PROJECT_FILE_SKELETONS.md`의 필수 파일 구조가 충돌하지 않는지
- `.codex-project.json` 필수 key와 `plans/STATUS.md` 필수 heading이
  runbook, skeleton, 운영 가이드에 같은 기준으로 적혀 있는지
- `PROJECT_TEMPLATE_PROMPT.md`는 설계 의도와 감사 기준을 담고,
  `OPERATING_GUIDE.md`는 운영 기준과 응용 기준을 담는 역할이 유지되는지
- `PATH.md`에 현재 공개 버전과 새 패치 버전의 차이가 간단히 기록되어
  있는지
- 공개 문서에 개인 경로, 개인 계정명, 임시 테스트 경로가 남아 있지 않은지

## 토큰 사용량 최적화 기준

이 구조는 논문 분석이나 코드 분석 자체의 입력량을 없애지는 않습니다.
대신 검증 품질을 낮추지 않는 범위에서 반복 문맥 로딩과 불필요한 재탐색을
줄이는 것을 목표로 합니다.

우선순위는 다음과 같습니다.

1. 전역 지침은 짧게 유지하고, 상세 절차는 runbook이나 프로젝트 문서로
   분리합니다.
2. 기존 프로젝트 작업은 `NOTES.md`와 `plans/STATUS.md`부터 시작하고,
   추가 문서는 상태 파일 로딩 기준에 따라 필요한 경우에만 읽습니다.
3. 큰 자료는 먼저 파일 목록, 목차, 요약, index로 범위를 좁힙니다.
4. 이미 검증된 요약이나 분석 노트가 있으면 먼저 재사용합니다.
5. 정확도, 안전, 사용자에게 보이는 산출물이 걸린 판단은 원문이나 실제
   소스 섹션을 다시 확인합니다.
6. 테스트, 검증, 근거 확인을 생략하는 방식으로 토큰을 줄이지 않습니다.

- 큰 PDF, 문서, 이미지, 코드 파일을 바로 읽기 전에 먼저 파일 목록을 확인합니다.
- 기존에 `configs/{group}/` 아래 요약, 비교표, 분석 노트가 있으면 원문보다 그 산출물을 먼저 읽습니다.
- 논문 프로젝트는 초록, 목차, 결론, 핵심 섹션을 먼저 보고 필요한 섹션만 깊게 읽습니다.
- 코드 프로젝트는 `rg` 같은 빠른 검색과 파일 목록으로 후보를 좁힌 뒤 관련 파일만 읽습니다.
- 분석이 끝나면 다음 작업에서 재사용할 수 있도록 요약과 근거를 `configs/{group}/`에 남깁니다.
- 로그는 전체 원문을 반복하지 않고 입력 파일, 생성 파일, 결정, 검증, 남은 확인 사항 중심으로 작성합니다.
- 긴 작업 후에는 클라이언트가 지원하는 경우 context를 compact하거나 요약합니다.
- 완전히 다른 작업은 새 세션에서 시작하는 것이 좋습니다.
- 한 세션은 하나의 명확한 작업 단위 중심으로 유지합니다.
- 관련 없는 IDE open tabs나 큰 선택 영역은 새 작업 전에 닫거나 줄이는 것이 좋습니다.

Codex CLI를 사용하는 경우, 클라이언트에서 지원하는 slash command로 세션 상태를 관리할 수 있습니다. 이 명령들은 프로젝트 파일 생성 규칙이 아니라 사용자 세션 관리용입니다.

| 명령 | 용도 |
| --- | --- |
| `/status` | 현재 모델, 승인 정책, token/context 상태 확인 |
| `/statusline` | 상태 표시줄에 context 통계나 token counter 표시 |
| `/compact` | 긴 대화 뒤 이전 내용을 요약해 context 확보 |
| `/new` | 완전히 다른 작업을 새 대화로 시작 |
| `/fork` | 같은 작업에서 실험 방향을 분기 |

코드 기반 프로젝트에서 관련 코드 경로가 크면, 전체 파일을 바로 읽지 말고 먼저 `configs/{group}/SOURCE_INDEX.md`를 만들어 핵심 폴더, 후보 파일, 제외 대상을 정리합니다. 이후 작업에서는 이 index를 먼저 읽고 필요한 파일만 선택적으로 확인합니다.

## 다른 에이전트에서 응용할 때

이 템플릿은 Codex 중심으로 설계되었습니다. 폴더 구조와 문서 흐름은 Claude, Cursor, Antigravity 등 다른 에이전트에서도 응용 가능할 것으로 예상되지만, 이 저장소에서는 실제 동작을 테스트하지 않았습니다.

따라서 다른 에이전트에서 사용할 때는 아래 내용을 해당 도구의 지시 파일, 권한 모델, 파일 접근 방식에 맞게 조정해야 합니다. `새 프로젝트 생성`만 입력했을 때 자동으로 템플릿을 읽고 파일을 만드는 동작은 도구별 설정과 권한이 갖춰져 있을 때만 가능합니다.

### 트리거 규칙 위치

[AGENTS_REQ.md](AGENTS_REQ.md)에는 실제 에이전트 지시 파일에 복사할
`새 프로젝트 생성` 트리거와 생성 이후 운영에 필요한 최소 지침 원본이
정리되어 있습니다.

Codex에서는 `.codex/AGENTS.md`에 이 지침을 넣을 수 있습니다.

다른 에이전트에서 비슷한 자동 트리거를 쓰려면 해당 도구가 읽는 전역 지시 파일이나 프로젝트 지시 파일에 유사한 규칙을 추가해야 합니다. 전역 지시 파일을 지원하지 않는 도구라면, 매번 템플릿 파일을 읽으라고 직접 요청해야 합니다.

예시:

```text
When the user enters exactly "새 프로젝트 생성", read
<CODEX_PROJECTS_ROOT>/PROJECT_CREATION_RUNBOOK.md and follow its Progressive Intake Flow.
Before creating project files, read
<CODEX_PROJECTS_ROOT>/PROJECT_FILE_SKELETONS.md and use its skeletons exactly.
```

도구별로 수정할 가능성이 높은 위치는 다음과 같습니다.

| 도구 | 수정할 가능성이 높은 위치 |
| --- | --- |
| Claude | 프로젝트 지침, custom instructions, 또는 `CLAUDE.md` |
| Cursor | `.cursorrules`, project rules, 또는 custom instructions |
| Antigravity | 해당 도구의 agent instructions 또는 workspace rules |
| 기타 에이전트 | 시스템/프로젝트 지시 파일 또는 사용자 정의 프롬프트 |

### 에이전트 이름

프롬프트 안의 `Codex`라는 표현이 어색하다면 사용하는 도구 이름으로 바꿀 수 있습니다.

예:

```text
Codex project
```

를 아래처럼 바꿀 수 있습니다.

```text
AI agent reference project
```

또는

```text
Claude reference project
```

### 경로 규칙

공개용 기본 설치는 현재 터미널 위치에 `codex_projects` 폴더를 만들고 `.git`
폴더를 제거해 일반 작업 폴더로 쓰는 방식입니다.

문서와 에이전트 지시에서는 설치 루트를 `<CODEX_PROJECTS_ROOT>`로 표기합니다.
이는 사용자가 설치한 `codex_projects` 폴더의 실제 절대 경로입니다.

예:

- `G:\Projects\codex_projects`
- `C:\Users\name\codex_projects`
- `/home/name/codex_projects`

홈 디렉터리에 설치하기로 선택한 경우에만 `~/codex_projects`를 사용할 수
있습니다. 이 경우에도 AGENTS_REQ.md를 실제 지시 파일에 복사할 때는
`<CODEX_PROJECTS_ROOT>`를 실제 절대 경로로 바꾸는 것이 명확합니다.

### 파일 읽기와 생성 권한

일부 에이전트는 로컬 파일을 자동으로 읽거나 폴더와 파일을 직접 생성하지 못할 수 있습니다. 그런 경우에는 다음을 명시적으로 요청하거나, 필요한 파일 내용을 직접 붙여 넣어야 합니다.

```text
PROJECT_CREATION_RUNBOOK.md를 먼저 읽고, Progressive Intake Flow에 따라 질문해줘.
```

또는

```text
아직 파일을 생성하지 말고, 프로젝트 설계안부터 제안해줘.
```

### 로그 언어

기본 로그는 영어 작업 기록과 한국어 사용자 요약을 함께 작성하도록 설계되어 있습니다. 다른 사용자가 한국어를 사용하지 않는다면 `logs/LOG_TEMPLATE.md`의 `Korean User Summary` 부분을 원하는 언어로 바꾸면 됩니다.
