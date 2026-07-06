# Legacy Migration Guide

이 문서는 자동화가 적용되기 전의 `codex_projects`를 최신 구조로 옮기는
가이드입니다.

기존 `codex_projects` 폴더를 삭제하거나 프로젝트를 밖으로 옮기지 마세요.
작업 중인 프로젝트 폴더는 그대로 둡니다.

## 1. 기존 지침 정리

`AGENTS.md`에서 예전에 직접 붙여 넣은 `codex_projects` 프로젝트 지침만
삭제하세요.

개인적으로 작성한 지침은 따로 저장해 두거나 그대로 남겨둡니다.

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

## 4. 프로젝트 구조 갱신

먼저 변경 예정 내용만 확인합니다.

Windows PowerShell:

```powershell
python .\codex_project_manager\migrate_projects.py --all
```

Linux/macOS:

```bash
python3 ./codex_project_manager/migrate_projects.py --all
```

문제가 없으면 실제 적용합니다.

Windows PowerShell:

```powershell
python .\codex_project_manager\migrate_projects.py --all --apply
```

Linux/macOS:

```bash
python3 ./codex_project_manager/migrate_projects.py --all --apply
```

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
