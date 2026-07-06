# Legacy Migration Guide

이 문서는 자동화가 적용되기 전의 `codex_projects`를 최신 구조로 옮기는
가이드입니다.

기존 `codex_projects` 폴더를 삭제하거나 프로젝트를 밖으로 옮기지 마세요.
작업 중인 프로젝트 폴더는 그대로 둡니다.

---

## 1. 기존 지침 정리

`AGENTS.md`에서 예전에 직접 붙여 넣은 `codex_projects` 프로젝트 지침만
삭제하세요.

개인적으로 작성한 지침은 따로 저장해 두거나 그대로 남겨둡니다.

---

## 2. 최신 Manager 설치

터미널을 기존 `codex_projects`의 상위 폴더로 이동한 뒤 실행합니다.

Windows PowerShell:

```powershell
git clone https://github.com/Nuowl/codex-project-template.git ".\codex_project_manager"
```

Linux/macOS:

```bash
git clone https://github.com/Nuowl/codex-project-template.git ./codex_project_manager
```

설치 후 구조는 아래처럼 됩니다.

```text
{parent}/
├─ codex_project_manager/    최신 관리 도구
└─ codex_projects/           기존 프로젝트 폴더
```

`codex_project_manager`의 `.git` 폴더는 업데이트에 필요하므로 삭제하지
마세요.

---

## 3. 최신 설정 적용

Windows PowerShell:

```powershell
python .\codex_project_manager\setup.py --workspace ".\codex_projects" --adopt-legacy
```

Linux/macOS:

```bash
python3 ./codex_project_manager/setup.py --workspace ./codex_projects --adopt-legacy
```

이 명령을 실행하면 작업 중인 프로젝트 폴더를 제외한 구버전 템플릿
구성 파일을 정리하고, 최신 Codex 관리 지침을 설치합니다.

정리된 템플릿 파일은 상위 폴더의
`codex_projects_legacy_template_backup_날짜` 폴더에 보관됩니다. 문제가
없으면 나중에 삭제해도 됩니다.

---

## 4. 프로젝트 구조 갱신

### 4-1. 변경 예정 내용 확인

먼저 변경 예정 내용만 확인합니다.

Windows PowerShell:

```powershell
python .\codex_project_manager\migrate_projects.py --all
```

Linux/macOS:

```bash
python3 ./codex_project_manager/migrate_projects.py --all
```

출력 예시는 아래와 같습니다.

```text
[legacy] alpasim: needs update, 11 changes
[unrelated] GSD
Preview: 1 project(s) would be migrated
```

- `[legacy]`: 최신 구조로 갱신할 프로젝트입니다.
- `[unrelated]`: 프로젝트가 아닌 폴더입니다. 갱신하지 않습니다.
- `changes`: 생성되거나 보완될 항목 수입니다.

### 4-2. 상세 변경 목록 확인

상세 변경 목록을 보려면 `--verbose`를 붙입니다.

Windows PowerShell:

```powershell
python .\codex_project_manager\migrate_projects.py --all --verbose
```

Linux/macOS:

```bash
python3 ./codex_project_manager/migrate_projects.py --all --verbose
```

### 4-3. 실제 적용

문제가 없으면 실제 적용합니다.

Windows PowerShell:

```powershell
python .\codex_project_manager\migrate_projects.py --all --apply
```

Linux/macOS:

```bash
python3 ./codex_project_manager/migrate_projects.py --all --apply
```

적용이 끝나면 백업 파일을 삭제할지 선택할 수 있습니다.  
`1`을 선택하면 레거시 템플릿 백업과 마이그레이션 백업을 삭제합니다.  
`2`를 선택하면 백업을 남깁니다.

---

## 5. 확인

Windows PowerShell:

```powershell
python .\codex_project_manager\setup.py --check
```

Linux/macOS:

```bash
python3 ./codex_project_manager/setup.py --check
```

설정 상태가 정상으로 나오면 새 Codex 세션을 시작하세요.
