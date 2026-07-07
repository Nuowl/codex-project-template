# Cloud Storage Installation Guide

해당 가이드는 Google Drive 같은 클라우드 스토리지 안에 `codex_project_manager`를 설치할 때 사용하는 가이드입니다.

일반 `git clone`이 클라우드 폴더에서 문제 없이 동작한다면 기본 [README](README.md)의 설치 방법을 사용해도 됩니다.  
클라우드 동기화 중 Git 파일 잠금 오류가 나거나, 여러 PC에서 같은 manager 폴더를 써야 한다면 아래 방식을 사용하세요.

---

## 1. 공통 준비

먼저 `<cloud-parent-folder>`를 `codex_project_manager`가 있거나 생성될 상위 클라우드 폴더로 바꿔 입력하세요.

예를 들어 `Google Drive/main/codex_project_manager`에 설치하려면
Windows 기준 `$CloudParent = "G:\Google Drive\main"`처럼 따옴표를 포함해 입력합니다.

Windows PowerShell:

```powershell
$CloudParent = "<cloud-parent-folder>"
```

Linux/macOS:

```bash
CLOUD_PARENT="<cloud-parent-folder>"
```

이후 필요한 절차를 선택해 단계별로 진행합니다.

---

## 2. 새 PC 설치

새 PC에서 처음 설치할 때 사용합니다.

### 2-1. Git 데이터 받기

Windows PowerShell:

```powershell
$ErrorActionPreference = "Stop"
$Repo = "https://github.com/Nuowl/codex-project-template.git"
$Manager = Join-Path $CloudParent "codex_project_manager"
$GitRoot = Join-Path $env:LOCALAPPDATA "codex-gitdirs"
$GitDir = Join-Path $GitRoot "codex_project_manager.git"
$Temp = Join-Path $env:TEMP ("codex_project_manager_bootstrap_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force $GitRoot | Out-Null
git clone --no-checkout --separate-git-dir $GitDir $Repo $Temp
```

Linux/macOS:

```bash
set -e
REPO="https://github.com/Nuowl/codex-project-template.git"
MANAGER="$CLOUD_PARENT/codex_project_manager"
GIT_DIR="$HOME/.local/share/codex-gitdirs/codex_project_manager.git"
TEMP_DIR="$(mktemp -d)"
mkdir -p "$(dirname "$GIT_DIR")"
git clone --no-checkout --separate-git-dir "$GIT_DIR" "$REPO" "$TEMP_DIR"
```

### 2-2. 클라우드 manager 폴더 만들기

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force $Manager | Out-Null
$GitDirForFile = $GitDir.Replace("\", "/")
Set-Content -NoNewline -Encoding ascii (Join-Path $Manager ".git") "gitdir: $GitDirForFile"
git --git-dir=$GitDir --work-tree=$Manager restore --source=HEAD :/
git --git-dir=$GitDir --work-tree=$Manager reset --mixed HEAD
```

Linux/macOS:

```bash
mkdir -p "$MANAGER"
printf 'gitdir: %s\n' "$GIT_DIR" > "$MANAGER/.git"
git --git-dir="$GIT_DIR" --work-tree="$MANAGER" restore --source=HEAD :/
git --git-dir="$GIT_DIR" --work-tree="$MANAGER" reset --mixed HEAD
```

### 2-3. 설치 확인 및 임시 폴더 삭제

Windows PowerShell:

```powershell
$Setup = Join-Path $Manager "setup.py"
python $Setup
python $Setup --check
Remove-Item -Recurse -Force $Temp
```

Linux/macOS:

```bash
python3 "$MANAGER/setup.py"
python3 "$MANAGER/setup.py" --check
rm -rf "$TEMP_DIR"
```

---

## 3. Version4 이전 폴더 전환

기존 `codex_projects` 폴더는 그대로 둡니다.

먼저 위의 [새 PC 설치](#2-새-pc-설치) 방식으로 `codex_project_manager`를 설치합니다.  
그 다음 아래 명령으로 최신 설정을 적용합니다.

### 3-1. 최신 설정 적용

Windows PowerShell:

```powershell
$Setup = Join-Path $CloudParent "codex_project_manager\setup.py"
$Workspace = Join-Path $CloudParent "codex_projects"
python $Setup --workspace $Workspace --adopt-legacy
```

Linux/macOS:

```bash
python3 "$CLOUD_PARENT/codex_project_manager/setup.py" --workspace "$CLOUD_PARENT/codex_projects" --adopt-legacy
```

이후 프로젝트 구조 갱신은 [Legacy Migration Guide의 프로젝트 구조 갱신 섹션](LEGACY_MIGRATION.md#4-프로젝트-구조-갱신)을 따르세요.

---

## 4. 다른 PC에서 활성화

다른 PC에서 클라우드 동기화 후 `codex_project_manager` 폴더가 이미 보이는 상태라면,  
그 PC의 로컬 Git 데이터만 새로 연결합니다.

### 4-1. 로컬 Git 데이터 받기

Windows PowerShell:

```powershell
$ErrorActionPreference = "Stop"
$Repo = "https://github.com/Nuowl/codex-project-template.git"
$Manager = Join-Path $CloudParent "codex_project_manager"
$GitRoot = Join-Path $env:LOCALAPPDATA "codex-gitdirs"
$GitDir = Join-Path $GitRoot "codex_project_manager.git"
$Temp = Join-Path $env:TEMP ("codex_project_manager_bootstrap_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force $GitRoot | Out-Null
git clone --no-checkout --separate-git-dir $GitDir $Repo $Temp
```

Linux/macOS:

```bash
set -e
REPO="https://github.com/Nuowl/codex-project-template.git"
MANAGER="$CLOUD_PARENT/codex_project_manager"
GIT_DIR="$HOME/.local/share/codex-gitdirs/codex_project_manager.git"
TEMP_DIR="$(mktemp -d)"
mkdir -p "$(dirname "$GIT_DIR")"
git clone --no-checkout --separate-git-dir "$GIT_DIR" "$REPO" "$TEMP_DIR"
```

### 4-2. 클라우드 manager 폴더 연결하기

Windows PowerShell:

```powershell
$GitDirForFile = $GitDir.Replace("\", "/")
Set-Content -NoNewline -Encoding ascii (Join-Path $Manager ".git") "gitdir: $GitDirForFile"
git --git-dir=$GitDir --work-tree=$Manager reset --mixed HEAD
```

Linux/macOS:

```bash
printf 'gitdir: %s\n' "$GIT_DIR" > "$MANAGER/.git"
git --git-dir="$GIT_DIR" --work-tree="$MANAGER" reset --mixed HEAD
```

### 4-3. 확인 및 임시 폴더 삭제

Windows PowerShell:

```powershell
$Setup = Join-Path $Manager "setup.py"
git -C $Manager status
python $Setup --check
Remove-Item -Recurse -Force $Temp
```

Linux/macOS:

```bash
git -C "$MANAGER" status
python3 "$MANAGER/setup.py" --check
rm -rf "$TEMP_DIR"
```

---

## 5. 업데이트 방법

설치가 정상적으로 완료되었다면 이후 업데이트는 README의 [도구 업데이트](README.md#도구-업데이트)를 따르세요.

---

## 확인할 점

- Git 데이터 폴더는 각 PC의 로컬 폴더입니다. 클라우드에 동기화하지 마세요.
- 다른 PC에서는 클라우드 작업 파일이 보여도 이 문서의 활성화 절차를 한 번 실행해야 합니다.
- `git status`에서 수정 파일이 표시되면 클라우드 동기화가 끝났는지 먼저 확인한 뒤 다시 실행하세요.
