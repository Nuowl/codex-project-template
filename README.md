# Codex Project Template

## 프로젝트 개요

Codex로 새 프로젝트 폴더, 참고 자료, 산출물, 로그, 요구사항 문서를 반복적으로 만들고 관리하기 위한 프로젝트 템플릿입니다.

프로젝트마다 첨부 자료, 분석 결과, 발표 자료, 작업 로그, 요구사항, 진행 상태, 검증 근거를 같은 구조로 정리하도록 돕습니다.

## 언제 사용하면 좋은가

사용하기 좋은 경우:

- Codex로 비슷한 프로젝트 폴더를 반복해서 만들 때
- 논문, 문서, 이미지, 코드 참고 자료와 결과물을 함께 관리할 때
- 요구사항, 진행 상태, 결정 사항, 검증 근거를 남겨야 할 때
- 발표 자료, 분석 노트, 변환 결과, 작업 로그를 프로젝트별로 정리할 때

다소 무거울 수 있는 경우:

- 단순 메모
- 1회성 질문
- 산출물이나 로그를 남길 필요가 없는 짧은 작업

## 빠른 시작

### 1단계: 저장소 설치

아래 [설치 방법](#설치-방법)에 따라 현재 터미널 위치에 `codex_projects`
폴더를 만듭니다. 설치가 끝나면 사용자의 작업 폴더에는
`codex_projects` 폴더 하나만 남고, 이 폴더는 Git 저장소가 아니라 일반
작업 폴더로 사용됩니다.

이 문서에서 `<CODEX_PROJECTS_ROOT>`는 사용자가 설치한 `codex_projects`
폴더의 실제 절대 경로를 뜻합니다. 예: `G:\GNU\codex_projects`,
`C:\Users\name\codex_projects`, `/home/name/codex_projects`

### 2단계: Codex 지침 추가

[AGENTS_REQ.md](AGENTS_REQ.md)의 내용을 Codex 전역 지시 파일 또는 프로젝트 지시 파일에 추가합니다.
[AGENTS_REQ.md](AGENTS_REQ.md) 안의 `<CODEX_PROJECTS_ROOT>`는 설치한
`codex_projects` 폴더의 실제 절대 경로로 바뀐 뒤 들어가야 합니다.

`AGENTS_REQ.md`는 전역 지침에 들어가도 부담이 작도록 최소 규칙만 담습니다.
성능 저하를 줄이기 위해 상세 절차는 평소에 읽지 않고, `새 프로젝트 생성`
같은 트리거가 있을 때 runbook을 읽는 구조입니다.

설정 화면에서 추가하는 방법:

1. Codex 클라이언트의 설정 화면을 엽니다.
2. `Custom Instructions`, `Agent Instructions`, `Project Instructions`처럼 지침을 넣는 항목을 찾습니다.
3. [AGENTS_REQ.md](AGENTS_REQ.md) 내용을 복사해 붙여넣습니다.
4. 저장 후 새 Codex 세션을 시작합니다.

주의: 설정 화면의 정확한 메뉴명은 Codex 클라이언트와 버전에 따라 달라질 수 있습니다. 지침 입력 항목이 보이지 않으면 아래 파일 방식으로 추가하세요.

파일로 추가하는 방법:

```text
~/.codex/AGENTS.md
```

Linux/macOS에서 빠르게 추가하려면:

```bash
ROOT="$(pwd)/codex_projects"
mkdir -p ~/.codex
sed "s|<CODEX_PROJECTS_ROOT>|$ROOT|g" ./codex_projects/AGENTS_REQ.md >> ~/.codex/AGENTS.md
```

Windows PowerShell에서 빠르게 추가하려면:

```powershell
$root = (Resolve-Path ".\codex_projects").Path
New-Item -ItemType Directory -Force "$HOME\.codex"
(Get-Content ".\codex_projects\AGENTS_REQ.md" -Raw).Replace("<CODEX_PROJECTS_ROOT>", $root) | Add-Content "$HOME\.codex\AGENTS.md"
```

주의: 위 명령은 현재 터미널 위치에 `codex_projects`를 설치한 상태를
기준으로 `<CODEX_PROJECTS_ROOT>`를 자동 치환합니다. 이미 같은 내용이 들어
있다면 중복으로 붙이지 말고 수동으로 확인해서 한 번만 넣는 것이 좋습니다.

### 3단계: Codex에서 새 프로젝트 생성

Codex 채팅에 아래 문장만 입력합니다.

```text
새 프로젝트 생성
```

Codex는 바로 전체 폴더를 만들지 않고, 프로젝트명, 관련 코드 경로, 참고 파일 여부, 목적과 요구사항을 단계적으로 확인한 뒤 생성안을 제안합니다. 사용자가 승인한 뒤에만 전체 프로젝트 구조를 생성합니다.

## 설치 방법

### 기본 설치: 현재 위치에 `codex_projects` 만들기

권장 설치 방식입니다.

현재 터미널 위치에 `codex_projects` 폴더를 clone한 뒤 `.git` 폴더를
제거합니다. 이렇게 하면 GitHub 템플릿 파일만 남고, 사용자의 작업 폴더에는
`codex_projects` 일반 폴더 하나만 남습니다.

Windows PowerShell 예시:

```powershell
git clone https://github.com/Nuowl/codex-project-template.git ".\codex_projects"
Remove-Item ".\codex_projects\.git" -Recurse -Force
Get-ChildItem ".\codex_projects" -Filter *.md
```

Linux/macOS 예시:

```bash
git clone https://github.com/Nuowl/codex-project-template.git ./codex_projects
rm -rf ./codex_projects/.git
ls ./codex_projects/*.md
```

### 선택 설치: 홈 디렉터리에 설치

터미널 위치와 무관하게 홈 디렉터리 아래에 두고 싶을 때만
`~/codex_projects`를 사용합니다.

Linux/macOS 예시:

```bash
git clone https://github.com/Nuowl/codex-project-template.git ~/codex_projects
rm -rf ~/codex_projects/.git
ls ~/codex_projects/*.md
```

Windows PowerShell 예시:

```powershell
git clone https://github.com/Nuowl/codex-project-template.git "$HOME\codex_projects"
Remove-Item "$HOME\codex_projects\.git" -Recurse -Force
Get-ChildItem "$HOME\codex_projects" -Filter *.md
```

### 선택 방식: 개발자/업데이트 관리용 clone

템플릿 저장소를 계속 `git pull`로 관리하려는 개발자만 별도 폴더에 clone해
사용하세요. 이 방식은 지인 공유용 기본 설치법이 아닙니다. 일반 사용자는
위의 기본 설치처럼 `codex_projects` 폴더에서 `.git`을 제거해 일반 폴더로
사용하는 편이 안전합니다.

### Git 없이 수동 설치

1. GitHub 저장소에 접속합니다.

```text
https://github.com/Nuowl/codex-project-template
```

2. `Code` 버튼을 누르고 `Download ZIP`을 선택합니다.
3. 압축을 풉니다.
4. 압축을 푼 폴더 이름을 `codex_projects`로 바꾸거나, Markdown 파일들을
   현재 작업 위치의 `codex_projects` 폴더로 복사합니다.

Linux/macOS 예시:

```bash
mkdir -p ./codex_projects
cp -R ~/Downloads/codex-project-template-main/*.md ./codex_projects/
```

Windows PowerShell 예시:

```powershell
New-Item -ItemType Directory -Force ".\codex_projects"
Copy-Item "$HOME\Downloads\codex-project-template-main\*.md" ".\codex_projects\" -Force
```

## 설치 후 확인

아래 파일들이 설치한 `codex_projects` 폴더, 즉
`<CODEX_PROJECTS_ROOT>`에 있어야 합니다.

| 파일 | 역할 |
| --- | --- |
| `PROJECT_CREATION_RUNBOOK.md` | 새 프로젝트 생성 절차 |
| `PROJECT_FILE_SKELETONS.md` | 생성할 Markdown 파일의 기본 골격 |
| `PROJECT_TEMPLATE_PROMPT.md` | 전체 설계 기준과 감사 기준 |
| `OPERATING_GUIDE.md` | 상세 운영 기준, 토큰 최적화, 다른 에이전트 응용 참고 |
| `AGENTS_REQ.md` | Codex 지시 파일에 추가할 최소 규칙 |
| `README.md` | 사용 가이드 |

실제 생성 흐름에서는 `PROJECT_CREATION_RUNBOOK.md`와
`PROJECT_FILE_SKELETONS.md`가 필요합니다. 필요한 Markdown 파일을
설치한 `codex_projects` 폴더에 두면 이 조건을 만족합니다.

## 기본 사용법

### 새 프로젝트 만들기

실행하기 전에 [AGENTS_REQ.md](AGENTS_REQ.md)의 내용이 Codex 전역 지시 파일
또는 프로젝트 지시 파일에 정상적으로 추가되었는지 확인하세요. 특히
`<CODEX_PROJECTS_ROOT>`가 실제 설치한 `codex_projects` 폴더의 절대 경로로
바뀌어 있어야 합니다. 아직 지침을 추가하지 않았다면
[2단계: Codex 지침 추가](#2단계-codex-지침-추가)를 먼저 진행하세요.

Codex에 입력:

```text
새 프로젝트 생성
```

진행 흐름:

1. 프로젝트명과 폴더명을 확인합니다.
2. 관련 코드 또는 저장소 경로가 있는지 확인합니다.
3. PDF, 문서, 이미지, 캡처 등 설계 참고 파일이 있는지 확인합니다.
4. 필요한 경우 `attachments/project-design/`만 먼저 만들고 참고 파일을 넣도록 안내합니다.
5. 프로젝트 목적과 초기 요구사항을 정리합니다.
6. 생성안을 제안합니다.
7. 사용자가 승인한 뒤 전체 폴더와 Markdown 파일을 생성합니다.

생성 후에는 원본 자료는 `attachments/`, 분석 결과는 `configs/`, 발표 자료는 `presentations/`, 작업 로그는 `logs/`, 요구사항과 진행 상태는 `plans/`에 정리됩니다.

자세한 폴더 구조와 운영 기준은 [OPERATING_GUIDE.md](OPERATING_GUIDE.md)를 참고하세요.

## 토큰 절감 방식

이 템플릿은 검증 품질을 낮추지 않는 범위에서 토큰 사용량을 줄이도록
구성되어 있습니다.

- 전역 지침에는 짧은 trigger와 context-budget 규칙만 둡니다.
- 상세 생성 절차는 `PROJECT_CREATION_RUNBOOK.md`가 필요할 때만 담당합니다.
- 필수 Markdown 골격은 파일 생성 직전에만 `PROJECT_FILE_SKELETONS.md`를 읽습니다.
- 긴 문서, PDF, 로그, 코드베이스는 파일 목록과 요약/index를 먼저 확인합니다.
- 정확도나 검증이 필요할 때는 요약만 믿지 않고 원문 또는 실제 소스 섹션을 다시 확인합니다.

자세한 기준은 [OPERATING_GUIDE.md](OPERATING_GUIDE.md)의
`토큰 사용량 최적화 기준`을 참고하세요.

## 내부 문서

| 문서 | 용도 |
| --- | --- |
| [AGENTS_REQ.md](AGENTS_REQ.md) | Codex 지시 파일에 복사할 최소 규칙 |
| [PROJECT_CREATION_RUNBOOK.md](PROJECT_CREATION_RUNBOOK.md) | 실제 생성 절차와 고정 질문 |
| [PROJECT_FILE_SKELETONS.md](PROJECT_FILE_SKELETONS.md) | 필수 Markdown 파일의 내부 구조 |
| [PROJECT_TEMPLATE_PROMPT.md](PROJECT_TEMPLATE_PROMPT.md) | 전체 설계 의도와 감사 기준 |
| [OPERATING_GUIDE.md](OPERATING_GUIDE.md) | 운영 기준, 토큰 최적화, 다른 에이전트 응용 참고 |

일반적인 `새 프로젝트 생성` 흐름에서는 `PROJECT_CREATION_RUNBOOK.md`를 먼저 읽고, Markdown 파일 생성 직전에만 `PROJECT_FILE_SKELETONS.md`를 읽도록 설계되어 있습니다.

## 트러블슈팅

### `새 프로젝트 생성`이 동작하지 않을 때

Codex가 `AGENTS_REQ.md` 규칙을 읽지 못한 상태일 가능성이 큽니다. 아래를
확인하세요.

- `AGENTS_REQ.md` 내용이 Codex 전역 지시 파일 또는 프로젝트 지시 설정에
  들어갔는지 확인합니다.
- `<CODEX_PROJECTS_ROOT>`가 실제 설치 경로로 바뀌었는지 확인합니다.
- 지시 파일을 수정한 뒤 새 Codex 세션을 시작합니다.

### 새 프로젝트가 원하지 않는 위치에 만들어질 때

전역 지시 파일에 들어간 설치 루트가 잘못되었을 가능성이 큽니다.

- `AGENTS.md` 안의 `PROJECT_CREATION_RUNBOOK.md` 경로가 실제 설치한
  `codex_projects` 폴더를 가리키는지 확인합니다.
- `<CODEX_PROJECTS_ROOT>`가 그대로 남아 있거나, 예전 `~/codex_projects`
  규칙이 중복으로 남아 있으면 실제 설치 경로로 정리합니다.
- 수정 후 새 Codex 세션을 시작합니다.

### 설치 후 폴더 상태가 예상과 다를 때

일반 사용 기준의 최종 형태는 작업 위치에 `codex_projects` 폴더 하나만
남는 것입니다. `codex-project-template` 폴더가 따로 남아 있다면 기본 설치가
아니라 개발자용 clone 방식이나 ZIP 압축 해제 폴더를 그대로 둔 상태일 수
있습니다.

또 `codex_projects/.git` 폴더가 있으면 아직 Git 저장소입니다. 일반 폴더로
쓰려면 아래 명령으로 `.git`을 제거합니다.

```powershell
Remove-Item ".\codex_projects\.git" -Recurse -Force
```

Linux/macOS:

```bash
rm -rf ./codex_projects/.git
```

### 참고 파일을 넣었는데 Codex가 못 찾을 때

프로젝트 생성 중 참고 파일을 쓰기로 했다면 Codex가 안내한 프로젝트의
아래 폴더에 파일을 넣어야 합니다.

```text
attachments/project-design/
```

파일을 넣은 뒤에는 Codex에 완료했다고 알려 주세요. Codex가 파일 목록을
확인한 다음 프로젝트 목적과 요구사항 단계로 진행합니다.

## 추가 참고

처음 설치하고 `새 프로젝트 생성`을 실행하는 데는 이 README만으로 충분합니다.

아래 상황에서는 [OPERATING_GUIDE.md](OPERATING_GUIDE.md)를 참고하세요.

- 생성된 프로젝트의 `plans/` 문서 역할을 자세히 알고 싶을 때
- 요구사항, 상태, 결정 기록, 추적표를 어떻게 관리할지 정해야 할 때
- 토큰 사용량을 줄이는 운영 방식을 확인하고 싶을 때
- 다른 에이전트에 구조를 응용할 때 주의사항을 확인하고 싶을 때
- 템플릿 구조나 생성 규칙을 수정하려고 할 때
