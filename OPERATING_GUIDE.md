# Codex Project Template 운영 가이드

이 문서는 README에서 분리한 세부 운영 기준입니다. 처음 설치하거나 새 프로젝트를 만들 때 반드시 전부 읽을 필요는 없습니다.

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
| 기준 문서 | `NOTES.md` | 프로젝트 개요와 주요 링크 |

## `plans/` 문서의 역할

| 파일 | 용도 |
| --- | --- |
| `plans/REQUIREMENTS.md` | 프로젝트 요구사항과 완료 기준 |
| `plans/WORKFLOW.md` | 전체 진행 과정 설계와 단계별 계획 |
| `plans/TRACEABILITY.md` | 요구사항, 산출물, 로그, 검증 근거 연결 |
| `plans/CHECKLIST.md` | 단계별 체크리스트 |
| `plans/STATUS.md` | 현재 단계, 최신 산출물, 다음 작업 |
| `plans/DECISIONS.md` | 중요한 결정과 그 이유 |

`NOTES.md`는 길게 작성하지 않고, 프로젝트 전체를 빠르게 파악하는 인덱스 역할만 하도록 유지합니다. 자세한 요구사항, 진행 상태, 체크리스트, 결정 기록은 `plans/` 폴더의 각 문서에 나누어 관리합니다.

## 기본 운영 기준

- 요구사항은 `REQ-001`, 완료 기준은 `AC-001`, 검증은 `VER-001`처럼 ID를 붙입니다.
- 요구사항을 만족하거나 검증하거나 실질적으로 뒷받침하는 산출물만 `plans/TRACEABILITY.md`에 연결합니다.
- 요구사항을 `Satisfied`로 바꾸려면 산출물, 로그, 검증 근거, 남은 확인 사항 상태가 모두 기록되어 있어야 합니다.
- 요구사항이나 완료 기준이 바뀌면 `REQUIREMENTS.md`, `DECISIONS.md`, `TRACEABILITY.md`, `STATUS.md`를 필요한 만큼 갱신합니다.
- `STATUS.md`에는 `Last reviewed` 날짜를 유지합니다.
- `DECISIONS.md`에는 중요한 결정만 영향 범위와 함께 기록합니다.
- `configs/`와 `logs/`는 같은 그룹 기준을 사용합니다.
- 기본 그룹 기준은 “챕터/주제 우선, 애매하거나 시간 흐름이 중요하면 날짜+주제”입니다.
- 발표 산출물은 항상 `presentations/{group}/` 아래에 저장합니다.
- 모든 로그는 `logs/LOG_TEMPLATE.md` 형식을 따르며, 영어 작업 기록과 한국어 요약을 함께 포함합니다.

## 최소 Handoff 기준

모든 상태 문서를 매번 강제로 갱신하기보다 `plans/STATUS.md` 중심의
최소 갱신 방식을 권장합니다. 이렇게 하면 긴 작업 뒤에 문서 간
동기화가 어긋날 가능성을 줄일 수 있습니다.

- 의미 있는 작업 후에는 최소한 `plans/STATUS.md`를 갱신합니다.
- 산출물이나 검증 근거가 생겼을 때만 `plans/TRACEABILITY.md`를
  갱신합니다.
- 요구사항, 완료 기준, 범위가 바뀐 경우에만 `plans/REQUIREMENTS.md`와
  `plans/DECISIONS.md`를 갱신합니다.
- 체크리스트 항목이 실제로 완료되었거나 새 점검 항목이 생긴 경우에만
  `plans/CHECKLIST.md`를 갱신합니다.

작업 완료를 보고하기 전에는 최소한 아래만 확인합니다.

1. `plans/STATUS.md`: 현재 단계, 최신 산출물, 최신 로그, 다음 작업이 맞는지
2. 관련 log: 작업 내용, 입력 파일, 생성 파일, 검증 결과가 기록되었는지
3. 필요한 `plans/TRACEABILITY.md`: 산출물이나 검증 근거가 요구사항을
   만족하거나 뒷받침할 때만 연결되었는지

## 유지보수 유의사항

새 프로젝트 생성 안정성을 유지하려면 아래 역할 구분을 지켜 주세요.

| 파일 | 역할 | 일반 생성 시 읽기 |
| --- | --- | --- |
| `PROJECT_CREATION_RUNBOOK.md` | 실제 생성 절차, 고정 질문, 승인 흐름, 필수 구조 | 예 |
| `PROJECT_FILE_SKELETONS.md` | 필수 Markdown 파일의 내부 골격 | 파일 생성 직전만 |
| `PROJECT_TEMPLATE_PROMPT.md` | 전체 설계 의도, 운영 기준, 감사 기준 | 아니요 |
| `README.md` | 사람을 위한 빠른 사용법 | 아니요 |
| `AGENTS_REQ.md` | 에이전트 지시 파일에 복사할 최소 규칙 | 설정할 때만 |

`PROJECT_TEMPLATE_PROMPT.md`는 상위 설계 문서입니다. 일반적인 `새 프로젝트 생성` 흐름에서는 먼저 읽을 필요가 없고, 구조를 변경하거나 생성 결과를 감사할 때 사용합니다.

구조나 생성 규칙을 바꿀 때는 한 파일만 수정하지 마세요.

- 생성 질문, 승인 흐름, 필수 폴더/파일 목록을 바꾸면 `PROJECT_CREATION_RUNBOOK.md`와 `PROJECT_TEMPLATE_PROMPT.md`를 함께 확인합니다.
- 필수 Markdown 문서의 내부 구조를 바꾸면 `PROJECT_FILE_SKELETONS.md`와 `PROJECT_TEMPLATE_PROMPT.md`의 문서 역할 설명을 함께 확인합니다.
- 트리거 경로나 읽기 순서를 바꾸면 `AGENTS_REQ.md`와 실제 사용하는 에이전트 지시 파일을 함께 갱신합니다.
- 설치 루트 표기인 `<CODEX_PROJECTS_ROOT>`를 바꾸면 README에 적힌 경로 안내도 함께 갱신합니다.

이 분리는 토큰 사용량을 줄이기 위한 것입니다. 전역 지침에는 짧은
트리거와 안전 규칙만 두고, 실행 중에는 짧은 runbook과 필요 시 skeleton만
읽으며, 긴 설계 문서는 평소에 읽지 않는 구조를 유지하는 것이 좋습니다.

## 에이전트가 참고하는 문서 기준

토큰 사용량을 줄이기 위해 에이전트는 기본적으로 아래 두 파일만 먼저 확인합니다.

- `NOTES.md`
- `plans/STATUS.md`

다음과 같은 상황에서는 추가 문서를 확인합니다.

| 상황 | 추가로 확인하는 문서 |
| --- | --- |
| 산출물 생성, 완료 판단, 요구사항 확인 | `plans/REQUIREMENTS.md`, `plans/TRACEABILITY.md` |
| 단계 변경 또는 큰 설계 변경 | `plans/WORKFLOW.md` |
| 완료 전 점검 | `plans/CHECKLIST.md` |
| 기존 결정과 충돌 가능성이 있는 변경 | `plans/DECISIONS.md` |
| 새 로그 작성 | `logs/LOG_TEMPLATE.md` |

## 토큰 사용량 최적화 기준

이 구조는 논문 분석이나 코드 분석 자체의 입력량을 없애지는 않습니다.
대신 검증 품질을 낮추지 않는 범위에서 반복 문맥 로딩과 불필요한 재탐색을
줄이는 것을 목표로 합니다.

우선순위는 다음과 같습니다.

1. 전역 지침은 짧게 유지하고, 상세 절차는 runbook이나 프로젝트 문서로
   분리합니다.
2. 큰 자료는 먼저 파일 목록, 목차, 요약, index로 범위를 좁힙니다.
3. 이미 검증된 요약이나 분석 노트가 있으면 먼저 재사용합니다.
4. 정확도, 안전, 사용자에게 보이는 산출물이 걸린 판단은 원문이나 실제
   소스 섹션을 다시 확인합니다.
5. 테스트, 검증, 근거 확인을 생략하는 방식으로 토큰을 줄이지 않습니다.

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

[AGENTS_REQ.md](AGENTS_REQ.md)에는 `새 프로젝트 생성` 트리거와 생성 이후 운영에 필요한 최소 지침이 정리되어 있습니다.

Codex에서는 `.codex/AGENTS.md`에 이 지침을 넣을 수 있습니다.

다른 에이전트에서 비슷한 자동 트리거를 쓰려면 해당 도구가 읽는 전역 지시 파일이나 프로젝트 지시 파일에 유사한 규칙을 추가해야 합니다. 전역 지시 파일을 지원하지 않는 도구라면, 매번 템플릿 파일을 읽으라고 직접 요청해야 합니다.

예시:

```text
When the user enters exactly "새 프로젝트 생성", read
<CODEX_PROJECTS_ROOT>/PROJECT_CREATION_RUNBOOK.md and follow its Progressive Intake Flow.
Before creating Markdown files, read
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

- `G:\GNU\codex_projects`
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
