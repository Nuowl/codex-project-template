# Version Path

이 파일은 GitHub에 공개된 이전 버전과 현재 작업 버전의 차이를 빠르게
확인하기 위한 간단한 변경 이력입니다.

## V1_260608

현재 GitHub에 올라가 있는 초기 공개 기준입니다.

- `새 프로젝트 생성` 트리거와 기본 project creation runbook 제공
- `README.md`에 설치, Codex 지침 추가, 기본 사용법, 토큰 절감 방식,
  내부 문서 설명을 함께 안내
- `PROJECT_CREATION_RUNBOOK.md`로 단계적 intake, 생성안 승인, 파일 생성
  절차 제공
- `PROJECT_FILE_SKELETONS.md`로 `NOTES.md`, `plans/`, `logs/` Markdown
  skeleton 제공
- `OPERATING_GUIDE.md`에 폴더 역할, `plans/` 문서 역할, 최소 handoff,
  토큰 최적화, 다른 에이전트 응용 기준 제공
- 프로젝트 식별은 주로 폴더 구조와 `NOTES.md`, `plans/STATUS.md`에 의존

## V2_260612

상태 루프 안정성, 공개 배포 문서 가독성, 프로젝트 식별 정확도를 개선한
버전입니다.

- README를 일반 사용자용 설치/사용/트러블슈팅 중심으로 재정리
- README의 내부 원리, 토큰 절감 설명, 상태 루프 설명을
  `OPERATING_GUIDE.md`로 이동
- README에서 개발자용 clone 안내를 제거하고, 생성 후 프로젝트 구조를
  파일 탐색기 형태로 표시
- Codex 설정 안내를 Windows/Linux 자동 추가, Codex 설정 화면 수동 추가,
  파일 수동 추가 방식으로 정리
- Windows PowerShell 자동 추가 명령에 UTF-8 인코딩을 명시해 한글 깨짐 방지
- 지침 갱신 시 기존 `codex_projects` 지침 중복 여부를 확인하도록 안내
- 기존 프로젝트를 Codex 프로젝트로 이전하는 사용 흐름 추가
- 새 프로젝트 루트에 `.codex-project.json` 식별자 파일을 생성하도록 추가
- active project root 판단 기준과 `.codex-project.json` 검증 기준 추가
- 상태 루프 실행/비실행 기준을 명확히 분리
- 의미 있는 작업의 기준과 `plans/STATUS.md` 갱신 조건을 명시
- `plans/STATUS.md`의 필수 resume heading을 고정:
  `Last Updated`, `Current State`, `Last Completed`, `Next Action`,
  `Blocked By`
- 기본 보고에서는 active project, 읽은 상태 파일, 갱신한 상태 파일 같은
  loop 내부 정보를 숨기고, 사용자가 요청하거나 문제가 있을 때만 보고하도록
  조정
- `OPERATING_GUIDE.md`에 템플릿 문서 역할, 보장 수준과 한계, 유지보수
  점검 기준을 추가
- 공개 문서의 개인 경로 예시를 일반 경로 예시로 정리
- `새 프로젝트 생성` 질문이 단계 사이에서 섞이거나 반복되지 않도록 각
  intake step을 한 턴에 하나의 고정 블록으로 진행하도록 명시
