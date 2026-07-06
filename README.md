# Codex Project Manager

현재 패치 버전은 `Version4_260706`입니다. 자세한 변경사항은
[PATH.md](PATH.md)를 확인하세요.

V4부터 GitHub에서 갱신하는 관리 도구와 사용자가 생성한 프로젝트를
별도 폴더에 보관합니다.  
도구를 업데이트해도 프로젝트 보관 폴더는
수정되지 않습니다.

```text
{parent}/
├─ codex_project_manager/    GitHub에서 갱신하는 도구
└─ codex_projects/           사용자 프로젝트 보관 폴더
```

- Version4 이전 버전을 사용 중이라면 기존 프로젝트를 그대로 두고
  [Legacy Migration Guide](LEGACY_MIGRATION.md)를 따르세요.

---

## 설치 전 확인

- 처음 설치 시, [신규 사용자 빠른 시작](#신규-사용자-빠른-시작)을 따르세요.
- V4 이상의 manager가 이미 있다면 [도구 업데이트](#도구-업데이트)를 따르세요.

---

## 신규 사용자 빠른 시작

### Windows PowerShell

```powershell
git clone https://github.com/Nuowl/codex-project-template.git ".\codex_project_manager"
python .\codex_project_manager\setup.py
```

### Linux/macOS

```bash
git clone https://github.com/Nuowl/codex-project-template.git ./codex_project_manager
python3 ./codex_project_manager/setup.py
```

- `setup.py`는 `codex_projects` workspace와 Codex 지침을 자동으로
  설정합니다.

설치가 끝나면 새 Codex 세션에서 다음을 입력하세요.

```text
새 프로젝트 생성
```

---

## 설치 경로 지정

workspace를 다른 위치에 두려면 최초 실행 시 `--workspace`를 지정하세요.

Windows PowerShell:

```powershell
python .\codex_project_manager\setup.py --workspace "(설치할 경로)"
```

Linux/macOS:

```bash
python3 ./codex_project_manager/setup.py --workspace "(설치할 경로)"
```

- 이때, manager와 workspace는 같은 폴더이거나 서로의 하위 폴더로 설치할 수 없습니다.

---

## 도구 업데이트

### Manager 업데이트

최초 설치 후에는 같은 `setup.py` 명령만 다시 실행하세요.

Windows PowerShell:

```powershell
python .\codex_project_manager\setup.py
```

Linux/macOS:

```bash
python3 ./codex_project_manager/setup.py
```

이 명령은 manager 도구와 Codex 관리 지침만 갱신합니다. 사용자가 만든
프로젝트 파일은 수정하지 않습니다.

변경 없이 설치 상태만 확인하려면:

Windows PowerShell:

```powershell
python .\codex_project_manager\setup.py --check
```

Linux/macOS:

```bash
python3 ./codex_project_manager/setup.py --check
```

### 기존 프로젝트 구조 갱신

도구 업데이트와 프로젝트 구조 갱신은 분리됩니다.

#### 1. 변경 예정 내용 확인

Windows PowerShell:

```powershell
python .\codex_project_manager\migrate_projects.py --all
```

Linux/macOS:

```bash
python3 ./codex_project_manager/migrate_projects.py --all
```

#### 2. 실제 적용

미리보기 결과를 확인한 뒤 실제 변경을 적용합니다.

Windows PowerShell:

```powershell
python .\codex_project_manager\migrate_projects.py --all --apply
```

Linux/macOS:

```bash
python3 ./codex_project_manager/migrate_projects.py --all --apply
```

적용이 끝나면 백업 파일을 삭제할지 선택할 수 있습니다.  
`1`을 선택하면 마이그레이션 백업을 삭제합니다.  
`2`를 선택하면 백업을 남깁니다.

#### 3. 특정 프로젝트만 확인

특정 프로젝트만 확인하려면:

Windows PowerShell:

```powershell
python .\codex_project_manager\migrate_projects.py --project "Project_A"
```

Linux/macOS:

```bash
python3 ./codex_project_manager/migrate_projects.py --project "Project_A"
```

---

## 개인 에이전트 지침

개인 지침은 `~/.codex/AGENTS.md`의 다음 관리 마커 **밖**에 작성하세요.

```text
<!-- BEGIN CODEX_PROJECTS MANAGED INSTRUCTIONS -->
<!-- manager가 관리하는 영역 -->
<!-- END CODEX_PROJECTS MANAGED INSTRUCTIONS -->
```

- `setup.py`를 반복 실행해도 마커 밖의 개인 지침은 보존됩니다.
- 마커 안에 작성한 내용은 다음 갱신 때 삭제됩니다.

---

## 생성되는 프로젝트 구조

```text
{project}/
├─ .codex-project.json (프로젝트 식별 파일 / 수정 불필요)
├─ NOTES.md (프로젝트 개요 및 링크)
├─ attachments/ (문서형 첨부파일)
├─ screenshots/ (이미지형 첨부파일)
├─ configs/ (결과물 출력)
├─ presentations/ (발표 관련 자료)
├─ logs/ (작업 기록)
└─ plans/ (프로젝트 구성안)
```

- 작업 결과는 `configs` 폴더에, 발표 자료는 `presentations` 폴더에 보관됩니다.
- 프로젝트 정보는 `NOTES.md`와 `plans` 폴더에서 확인할 수 있으며, 작업 기록은 `logs` 폴더에서 확인할 수 있습니다.

---

## 트러블슈팅

### `setup.py`를 찾지 못할 때

현재 터미널이 `codex_project_manager` 상위 폴더인지 확인하세요.  
Windows PowerShell에서는 `Get-Location`, Linux/macOS에서는 `pwd`를
사용해 확인할 수 있습니다.

### manager 업데이트가 `Tracked manager files have uncommitted changes`로 중단될 때

`codex_project_manager` 안의 파일을 직접 수정한 상태에서는 `setup.py`가 업데이트를 중단합니다.  
GitHub 최신 파일로 덮어쓰면 로컬 수정 내용이 사라질 수 있기 때문입니다.

수정 내용을 버리고 최신 manager로 맞추려면:

Windows PowerShell:

```powershell
cd .\codex_project_manager
git restore .
cd ..
python .\codex_project_manager\setup.py
```

Linux/macOS:

```bash
cd ./codex_project_manager
git restore .
cd ..
python3 ./codex_project_manager/setup.py
```

### `Legacy workspace not found`가 나올 때

레거시 전환 명령은 기존 `codex_projects` 폴더 안이 아니라, 그 바깥의
상위 폴더에서 실행해야 합니다.

```text
{parent}/
├─ codex_project_manager/    GitHub에서 갱신하는 도구
└─ codex_projects/           사용자 프로젝트 보관 폴더
```

### manager 업데이트가 거부될 때

manager의 Git 추적 파일에 로컬 변경이 있거나, `origin`이 공식 GitHub
저장소가 아니거나, fast-forward가 불가능하면 업데이트를 중단합니다.  
오류 내용을 확인하고 수동 변경을 백업한 뒤 다시 실행하세요.

### workspace 경로를 바꾸고 싶을 때

`~/.codex/codex-projects.json`의 경로를 직접 수정하지 마세요.  
기존
workspace를 다른 위치로 옮기는 절차는 아직 자동화되어 있지 않습니다.  
프로젝트 폴더를 백업한 뒤 새 위치에 다시 설정해야 합니다.

### 한글 인코딩 오류가 날 때

manager는 설정과 지침을 UTF-8로 명시적으로 읽고 씁니다.  
기존 `AGENTS.md`가 CP949 또는 UTF-16이면 안전을 위해 덮어쓰지 않고 오류를
발생시킵니다.  
기존 파일을 UTF-8로 변환한 뒤 다시 실행하세요.

---

<big></big><strong>자세한 문서 요소, 운영 규칙, 유지보수 기준, 다른 에이전트로컬라이징 관련 정보는 를확인하세요.</big>
