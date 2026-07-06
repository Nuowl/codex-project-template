# Version Path

이 파일은 버전별 주요 변경사항을 정리한 내역입니다.

## V1_260608

초기 공개 버전입니다.

- `새 프로젝트 생성` 트리거 추가
- 단계별 프로젝트 생성 runbook 제공
- `NOTES.md`, `plans/`, `logs/` 기본 skeleton 제공
- 설치, 사용, 폴더 구조, 운영 규칙 문서 제공

## V2_260612

프로젝트 식별과 상태 관리를 개선한 버전입니다.

- README를 설치, 사용, 트러블슈팅 중심으로 재정리
- Windows/Linux 지침 설치 방법과 UTF-8 한글 깨짐 방지 안내 추가
- 기존 프로젝트 이전 절차 추가
- `.codex-project.json` 프로젝트 식별자 추가
- 활성 프로젝트 선택·검증 규칙 개선
- `plans/STATUS.md` 상태 갱신 기준과 필수 항목 고정
- `새 프로젝트 생성` 단계별 질문 흐름 개선
- 운영 규칙과 유지보수 안내 보강

## V3_260622

Codex 지침 설치와 갱신을 개선한 버전입니다.

- `install_agents.py` 자동 설치·갱신 기능 추가
- 설치 경로 자동 인식 및 지침 경로 자동 설정
- 반복 갱신 시 기존 지침 자동 교체 및 중복 방지
- 갱신 전 `AGENTS.md.bak` 자동 백업
- 개인 에이전트 지침 보존
- UTF-8 한글 깨짐 방지
- 설치 명령 및 트러블슈팅 안내 갱신

## V4_260706

관리 도구와 사용자 프로젝트 보관 영역을 분리한 버전입니다.

- `codex_project_manager` 도구 폴더와 `codex_projects` workspace 분리
- `setup.py`로 최초 설치, manager 업데이트, Codex 지침 갱신 통합
- `~/.codex/codex-projects.json` 기반 manager/workspace 경로 설정 추가
- `--adopt-legacy`로 자동화 적용 전 혼합 폴더를 프로젝트 이동 없이 전환
- `migrate_projects.py`로 기존 프로젝트 구조 미리보기, 백업, 갱신 지원
- README, 레거시 전환 가이드, 운영 가이드, 설계 참고 문서 역할 정리
- 설치되는 에이전트 지침을 축소하고 토큰 절약·상태 루프 규칙 유지
