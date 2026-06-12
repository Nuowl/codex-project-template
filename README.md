# Codex Project Template

현재 패치 버전은 `Version2_260612`입니다. 자세한 패치 내역은
[PATH.md](PATH.md)를 참고하십시오.

템플릿을 업데이트할 때는 기존 하위 프로젝트 폴더는 유지하고, 템플릿
Markdown 파일만 최신 파일로 덮어쓴 뒤, Codex 설정이나
`~/.codex/AGENTS.md`에 들어간 기존 `codex_projects` 지침을 제거하고 최신
[AGENTS_REQ.md](AGENTS_REQ.md) 내용을 다시 추가하세요. 기존에 따로
진행하던 프로젝트를 이 템플릿으로 관리하려면
[기존 프로젝트를 Codex 프로젝트로 이전하기](#기존-프로젝트를-codex-프로젝트로-이전하기)를
참고하세요.

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

1. [설치 방법](#설치-방법)에 따라 현재 터미널 위치에 `codex_projects`
   폴더를 만듭니다.
2. [Codex 지침 추가](#codex-지침-추가)에 따라 `AGENTS_REQ.md` 내용을
   Codex 지침에 추가합니다.
3. Codex 채팅에 `새 프로젝트 생성`을 입력합니다.

이 문서에서 `<CODEX_PROJECTS_ROOT>`는 사용자가 설치한 `codex_projects`
폴더의 실제 절대 경로를 뜻합니다. 예: `G:\Projects\codex_projects`,
`C:\Users\name\codex_projects`, `/home/name/codex_projects`

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

설치한 `codex_projects` 폴더, 즉 `<CODEX_PROJECTS_ROOT>`에 아래 파일들이
있어야 합니다.

- `README.md`
- `AGENTS_REQ.md`
- `PROJECT_CREATION_RUNBOOK.md`
- `PROJECT_FILE_SKELETONS.md`
- `PROJECT_TEMPLATE_PROMPT.md`
- `OPERATING_GUIDE.md`
- `PATH.md`

각 파일의 자세한 역할은 [OPERATING_GUIDE.md](OPERATING_GUIDE.md)의
`템플릿 문서 역할`을 참고하세요.

## Codex 지침 추가

`새 프로젝트 생성` 트리거를 쓰려면 [AGENTS_REQ.md](AGENTS_REQ.md)의 내용을
Codex 지침에 한 번 추가해야 합니다. 가장 쉬운 방법은 터미널에서 자동으로
추가하는 것입니다.

`AGENTS_REQ.md` 안의 `<CODEX_PROJECTS_ROOT>`는 설치한 `codex_projects`
폴더의 실제 절대 경로로 바뀐 뒤 들어가야 합니다. 예:
`G:\Projects\codex_projects`, `C:\Users\name\codex_projects`,
`/home/name/codex_projects`

`AGENTS_REQ.md`는 실제 Codex 지침 파일에 복사해 넣는 원본입니다. 전역
지침에 들어가도 부담이 작도록 최소 규칙만 담습니다. 성능 저하를 줄이기
위해 상세 절차는 평소에 읽지 않고, `새 프로젝트 생성` 같은 트리거가 있을
때 runbook을 읽는 구조입니다.

### 방법 A: 터미널로 자동 추가

권장 방식입니다. 아래 명령은 현재 터미널 위치에 `codex_projects` 폴더가
있다고 가정합니다. 다른 위치에 설치했다면 먼저 그 위치로 이동한 뒤
실행하세요.

Windows PowerShell:

```powershell
$root = (Resolve-Path ".\codex_projects").Path
$agentsDir = Join-Path $HOME ".codex"
$agentsFile = Join-Path $agentsDir "AGENTS.md"
New-Item -ItemType Directory -Force $agentsDir | Out-Null
(Get-Content ".\codex_projects\AGENTS_REQ.md" -Raw -Encoding UTF8).Replace("<CODEX_PROJECTS_ROOT>", $root) | Add-Content $agentsFile -Encoding UTF8
```

Linux/macOS:

```bash
ROOT="$(pwd)/codex_projects"
mkdir -p ~/.codex
sed "s|<CODEX_PROJECTS_ROOT>|$ROOT|g" ./codex_projects/AGENTS_REQ.md >> ~/.codex/AGENTS.md
```

주의: 위 명령은 `<CODEX_PROJECTS_ROOT>`를 자동으로 실제 설치 경로로
치환한 뒤 `~/.codex/AGENTS.md`에 내용을 덧붙입니다. 이미 같은 내용이
들어 있다면 중복으로 붙이지 말고 한 번만 넣으세요.

Windows PowerShell에서 `-Encoding UTF8`을 빼면 시스템 로캘에 따라 한글이
`?`로 저장될 수 있습니다. 이미 깨진 내용은 해당 블록을 삭제한 뒤 위
명령으로 다시 추가하세요.

### 방법 B: Codex 설정 화면에서 수동 추가

현재 Codex 앱 기준으로는 아래 순서로 추가할 수 있습니다.

1. [AGENTS_REQ.md](AGENTS_REQ.md)를 엽니다.
2. 파일 안의 모든 `<CODEX_PROJECTS_ROOT>`를 설치한 `codex_projects`
   폴더의 실제 절대 경로로 바꿉니다.
3. Codex 에이전트 채팅창 우측 위의 톱니바퀴 아이콘을 클릭합니다.
4. `Codex 설정`을 클릭합니다.
5. `개인 맞춤 설정`으로 이동합니다.
6. `맞춤형 지침`에 경로를 수정한 `AGENTS_REQ.md` 내용을 복사해 붙여넣습니다.
7. 저장 후 새 Codex 세션을 시작합니다.

설정 화면에서 지침 입력 항목이 보이지 않으면 아래 파일 방식으로 직접
추가하세요.

### 방법 C: 파일로 수동 추가

`~/.codex/AGENTS.md` 파일을 열거나 새로 만든 뒤, 경로를 수정한
`AGENTS_REQ.md` 내용을 붙여넣습니다.

```text
~/.codex/AGENTS.md
```

중요: 붙여넣기 전에 `<CODEX_PROJECTS_ROOT>`를 그대로 두지 말고 실제
`codex_projects` 폴더 경로로 바꿔야 합니다. 예를 들어 `codex_projects`를
`C:\Projects\codex_projects`에 설치했다면 `AGENTS_REQ.md` 안의 모든
`<CODEX_PROJECTS_ROOT>`를 `C:\Projects\codex_projects`로 바꾼 뒤
붙여넣으세요. 그러면 runbook 경로가 실제 `codex_projects` 폴더를
가리키게 됩니다.

### 지침 갱신 시 주의사항

Codex 지침을 추가하거나 갱신할 때는 같은 `codex_projects` 지침이 이미
들어 있는지 먼저 확인하세요. 확인 위치는 Codex 설정 화면의 `맞춤형 지침`
또는 `~/.codex/AGENTS.md`입니다.

이미 같은 지침이 있다면 기존 내용을 먼저 삭제한 뒤 터미널 자동 추가 명령을
다시 실행하거나, 경로를 수정한 새 `AGENTS_REQ.md` 내용을 다시 붙여넣으세요.
같은 지침을 여러 번 추가하면 Codex가 중복 규칙을 반복해서 읽어 context를
낭비하고, 나중에 예전 규칙과 새 규칙이 함께 남아 동작이 헷갈릴 수 있습니다.

## 기본 사용법

### 새 프로젝트 만들기

실행하기 전에 [AGENTS_REQ.md](AGENTS_REQ.md)의 내용이 Codex 전역 지시 파일
또는 프로젝트 지시 파일에 정상적으로 추가되었는지 확인하세요. 특히
`<CODEX_PROJECTS_ROOT>`가 실제 설치한 `codex_projects` 폴더의 절대 경로로
바뀌어 있어야 합니다. 아직 지침을 추가하지 않았다면
[Codex 지침 추가](#codex-지침-추가)를 먼저 진행하세요.

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
7. 사용자가 승인한 뒤 전체 폴더, `.codex-project.json`, Markdown 파일을 생성합니다.

생성 후 프로젝트 폴더는 아래처럼 정리됩니다.

```text
{project folder}/
├─ .codex-project.json     프로젝트 식별자
├─ NOTES.md                프로젝트 개요와 주요 경로
├─ attachments/            원본 PDF, 문서, 참고 자료
├─ screenshots/            이미지, 캡처, 도표
├─ configs/                분석 결과, 요약, 변환 결과
├─ presentations/          발표 자료와 발표 스크립트
├─ logs/                   작업 로그와 검증 기록
└─ plans/                  요구사항, 진행 상태, 결정, 추적표
```

자세한 폴더 구조와 운영 기준은 [OPERATING_GUIDE.md](OPERATING_GUIDE.md)를 참고하세요.

### 기존 프로젝트를 Codex 프로젝트로 이전하기

이미 따로 진행하던 프로젝트가 있다면 원본 폴더를 `codex_projects` 안으로
옮기기보다, `codex_projects` 아래에 관리용 프로젝트 폴더를 새로 만들고
기존 프로젝트 경로를 `관련 코드/저장소 경로`로 연결하는 방식을 권장합니다.
이렇게 하면 원본 코드, 자료, Git 기록을 건드리지 않고 요구사항, 상태,
로그, 산출물만 Codex 프로젝트 형식으로 정리할 수 있습니다.

진행 방법:

1. 먼저 [Codex 지침 추가](#codex-지침-추가)가 완료되었는지 확인합니다.
2. Codex 채팅에 `새 프로젝트 생성`을 입력합니다.
3. 프로젝트명과 폴더명은 기존 프로젝트를 알아보기 쉬운 이름으로 입력합니다.
4. `관련 코드/저장소 경로` 질문에는 기존 프로젝트나 자료 폴더의 절대 경로를 입력합니다.
5. 기존 기획서, PDF, 이미지, 캡처 같은 참고 파일을 같이 정리하려면 `있음`을 선택하고, 안내받은 `attachments/project-design/` 폴더에 파일을 넣습니다.
6. 프로젝트 목적과 현재까지의 진행 상태를 초기 요구사항에 적습니다.
7. Codex가 제안한 생성안을 확인한 뒤 승인합니다.

이전 후에는 Codex에 아래처럼 요청하면 기존 상태를 프로젝트 문서에 정리할
수 있습니다.

```text
기존 프로젝트 경로를 기준으로 현재 상태를 파악해서 NOTES.md와 plans/ 문서를 업데이트해줘.
```

주의: 기존 프로젝트의 전체 파일을 무작정 복사하지 마세요. `.git`,
`node_modules`, 빌드 산출물, 대용량 원본 자료는 원본 위치에 두고, 필요한
경로와 요약만 Codex 프로젝트 문서에 기록하는 편이 안전합니다.

## 트러블슈팅

### `새 프로젝트 생성`이 동작하지 않을 때

Codex가 `AGENTS_REQ.md`에서 복사한 규칙을 실제 지침에서 읽지 못한 상태일
가능성이 큽니다. 아래를 확인하세요.

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

### 기존 프로젝트가 Codex 프로젝트로 인식되지 않을 때

새로 생성한 프로젝트라면 프로젝트 루트에 `.codex-project.json`이 있는지
확인하세요. 이 파일의 `schema`는 `codex_projects`, `project_folder`는 실제
프로젝트 폴더명과 같아야 합니다.

오래전에 만든 프로젝트라 `.codex-project.json`이 없다면 `NOTES.md`와
`plans/STATUS.md`가 있는 경우 legacy Codex 프로젝트로 이어갈 수 있습니다.
필요하다면 Codex에 아래처럼 요청하세요.

```text
이 프로젝트에 .codex-project.json 식별자 파일을 추가해줘.
```

### 패치 후 기존 프로젝트 운영이 이상할 때

이전 패치 버전으로 만든 프로젝트에는 `.codex-project.json` 같은 프로젝트
식별자나 최신 템플릿에서 추가된 문서 항목이 없을 수 있습니다. 이 경우
기존 프로젝트를 직접 고치기보다, 해당 프로젝트를 기준으로 새 Codex
프로젝트를 생성하는 방식을 권장합니다.

자세한 방법은
[기존 프로젝트를 Codex 프로젝트로 이전하기](#기존-프로젝트를-codex-프로젝트로-이전하기)를
참고하십시오.

### 설치 후 폴더 상태가 예상과 다를 때

일반 사용 기준의 최종 형태는 작업 위치에 `codex_projects` 폴더 하나만
남는 것입니다. `codex-project-template` 폴더가 따로 남아 있다면 ZIP 압축
해제 폴더를 그대로 둔 상태일 수 있습니다.

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
