# Codex Project Template

## 프로젝트 개요

Codex로 새 프로젝트 폴더, 참고 자료, 산출물, 로그, 요구사항 문서를 반복적으로 만들고 관리하기 위한 프로젝트 템플릿입니다.

이 템플릿은 단순 파일 보관용이 아니라, 프로젝트마다 첨부 자료, 분석 결과, 발표 자료, 작업 로그, 요구사항, 진행 상태, 검증 근거를 같은 구조로 정리하도록 돕습니다.

Codex 중심으로 설계되었습니다. 다른 에이전트에서도 구조상 응용 가능할 것으로 예상되지만, 이 저장소에서는 별도 테스트하지 않았습니다.

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

아래 [설치 방법](#설치-방법) 중 하나를 선택해 저장소 파일을 `~/codex_projects`에 배치합니다.

`~`는 현재 사용자 홈 디렉터리입니다. 예를 들어 Linux에서는 `/home/username`, Windows PowerShell에서는 보통 `C:\Users\username`에 해당합니다.

### 2단계: Codex 지침 추가

[AGENTS_REQ.md](AGENTS_REQ.md)의 내용을 Codex 전역 지시 파일 또는 프로젝트 지시 파일에 추가합니다.

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
mkdir -p ~/.codex
cat ~/codex_projects/AGENTS_REQ.md >> ~/.codex/AGENTS.md
```

Windows PowerShell에서 빠르게 추가하려면:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex"
Get-Content "$HOME\codex_projects\AGENTS_REQ.md" | Add-Content "$HOME\.codex\AGENTS.md"
```

주의: 이미 같은 내용이 들어 있다면 중복으로 붙이지 말고 수동으로 확인해서 한 번만 넣는 것이 좋습니다. 전역 지침에 넣으면 모든 Codex 작업에 적용되고, 프로젝트 지침에 넣으면 해당 프로젝트에서만 적용됩니다.

### 3단계: Codex에서 새 프로젝트 생성

Codex 채팅에 아래 문장만 입력합니다.

```text
새 프로젝트 생성
```

Codex는 바로 전체 폴더를 만들지 않고, 프로젝트명, 관련 코드 경로, 참고 파일 여부, 목적과 요구사항을 단계적으로 확인한 뒤 생성안을 제안합니다. 사용자가 승인한 뒤에만 전체 프로젝트 구조를 생성합니다.

## 설치 방법

### Git으로 설치

권장 설치 방식입니다.

템플릿 저장소는 `~/codex-project-template`에 clone하고, 실제 프로젝트들이
생성될 `~/codex_projects`에는 필요한 Markdown 파일만 복사합니다.
`~/codex_projects` 자체를 Git 저장소로 만들면 이후 생성되는 실제 프로젝트
폴더가 템플릿 저장소의 untracked 파일로 섞일 수 있습니다.

```bash
git clone https://github.com/Nuowl/codex-project-template.git ~/codex-project-template
mkdir -p ~/codex_projects
cp ~/codex-project-template/*.md ~/codex_projects/
```

Windows PowerShell 예시:

```powershell
git clone https://github.com/Nuowl/codex-project-template.git "$HOME\codex-project-template"
New-Item -ItemType Directory -Force "$HOME\codex_projects"
Copy-Item "$HOME\codex-project-template\*.md" "$HOME\codex_projects\" -Force
```

보조 방식: `~/codex_projects`를 템플릿 전용 Git 저장소로만 쓸 계획이라면
직접 clone할 수도 있습니다. 이후 같은 폴더 아래에 실제 프로젝트를 생성하면
untracked 파일이 섞일 수 있으므로 일반 사용에는 권장하지 않습니다.

```bash
git clone https://github.com/Nuowl/codex-project-template.git ~/codex_projects
```

### Git 없이 수동 설치

1. GitHub 저장소에 접속합니다.

```text
https://github.com/Nuowl/codex-project-template
```

2. `Code` 버튼을 누르고 `Download ZIP`을 선택합니다.
3. 압축을 풉니다.
4. 압축을 푼 폴더 안의 Markdown 파일을 `~/codex_projects`에 복사합니다.

Linux/macOS 예시:

```bash
mkdir -p ~/codex_projects
cp -R ~/Downloads/codex-project-template-main/*.md ~/codex_projects/
```

Windows PowerShell 예시:

```powershell
New-Item -ItemType Directory -Force "$HOME\codex_projects"
Copy-Item "$HOME\Downloads\codex-project-template-main\*.md" "$HOME\codex_projects\" -Force
```

## 설치 후 확인

아래 파일들이 `~/codex_projects`에 있어야 합니다.

| 파일 | 역할 |
| --- | --- |
| `PROJECT_CREATION_RUNBOOK.md` | 새 프로젝트 생성 절차 |
| `PROJECT_FILE_SKELETONS.md` | 생성할 Markdown 파일의 기본 골격 |
| `PROJECT_TEMPLATE_PROMPT.md` | 전체 설계 기준과 감사 기준 |
| `OPERATING_GUIDE.md` | 상세 운영 기준, 토큰 최적화, 다른 에이전트 응용 참고 |
| `AGENTS_REQ.md` | Codex 지시 파일에 추가할 최소 규칙 |
| `README.md` | 사용 가이드 |

설계 검토 문서인 `PROJECT_TEMPLATE_PROMPT.md`는 아래 경로에 배치됩니다.

```text
~/codex_projects/PROJECT_TEMPLATE_PROMPT.md
```

실제 생성 흐름에서는 `PROJECT_CREATION_RUNBOOK.md`와
`PROJECT_FILE_SKELETONS.md`가 필요합니다. 필요한 Markdown 파일을
`~/codex_projects`에 복사하면 이 조건을 만족합니다.

## 기본 사용법

### 새 프로젝트 만들기

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

## 내부 문서

| 문서 | 용도 |
| --- | --- |
| [AGENTS_REQ.md](AGENTS_REQ.md) | Codex 지시 파일에 복사할 최소 규칙 |
| [PROJECT_CREATION_RUNBOOK.md](PROJECT_CREATION_RUNBOOK.md) | 실제 생성 절차와 고정 질문 |
| [PROJECT_FILE_SKELETONS.md](PROJECT_FILE_SKELETONS.md) | 필수 Markdown 파일의 내부 구조 |
| [PROJECT_TEMPLATE_PROMPT.md](PROJECT_TEMPLATE_PROMPT.md) | 전체 설계 의도와 감사 기준 |
| [OPERATING_GUIDE.md](OPERATING_GUIDE.md) | 운영 기준, 토큰 최적화, 다른 에이전트 응용 참고 |

일반적인 `새 프로젝트 생성` 흐름에서는 `PROJECT_CREATION_RUNBOOK.md`를 먼저 읽고, Markdown 파일 생성 직전에만 `PROJECT_FILE_SKELETONS.md`를 읽도록 설계되어 있습니다. 긴 설계 문서는 구조 변경이나 감사가 필요할 때 확인합니다.

## 추가 참고

처음 설치하고 `새 프로젝트 생성`을 실행하는 데는 이 README만으로 충분합니다.

아래 상황에서는 [OPERATING_GUIDE.md](OPERATING_GUIDE.md)를 참고하세요.

- 생성된 프로젝트의 `plans/` 문서 역할을 자세히 알고 싶을 때
- 요구사항, 상태, 결정 기록, 추적표를 어떻게 관리할지 정해야 할 때
- 토큰 사용량을 줄이는 운영 방식을 확인하고 싶을 때
- 다른 에이전트에 구조를 응용할 때 주의사항을 확인하고 싶을 때
- 템플릿 구조나 생성 규칙을 수정하려고 할 때
