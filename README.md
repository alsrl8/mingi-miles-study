# mingi-miles-study

Miles가 여러 기기에서 배운 내용을 수집하고, 다시 설명할 수 있는 지식으로
정리하기 위한 공개 학습 저장소입니다. 이 저장소 자체가 정본이며 어느
기기에서든 clone한 뒤 같은 방식으로 기록할 수 있습니다.

## Mastery learning loop

1. 선수 개념부터 짜인 `curriculum/` track에서 다음 개념을 고릅니다.
2. `lessons/`에서 짧은 설명과 풀이 예제를 학습합니다.
3. `assignments/`에서 guided 과제 후 independent 과제를 풉니다.
4. `assessments/`에서 자료 없이 설명·적용·진단 능력을 확인합니다.
5. 오답 원인에 맞는 다른 문제로 교정하고, 며칠 뒤 다시 회상합니다.
6. `maps/progress.md`에 중단 지점과 다음 행동을 남기고 sync합니다.

한 번 읽거나 즉시 시험을 통과한 상태를 장기 기억으로 간주하지 않습니다.
학습 상태는 `locked → learning → practiced → provisional → review_due →
retained` 순서로, 실제 과제와 지연 회상 근거가 있을 때만 바뀝니다.

## Content map

- `topics/`: 대화 없이 이해할 수 있는 개념의 정본
- `curriculum/`: 목표, 선수 관계, 학습 순서, 통과 근거
- `lessons/`: 설명, 풀이 예제, 오개념, 짧은 회상 질문
- `assignments/`: guided, faded, independent, transfer 과제
- `assessments/`: 문제, rubric, 변형 문제, 교정 경로
- `inbox/`: 시간순 관찰과 공개 가능한 학습 로그
- `reviews/`: 회상 질문과 주간 회고
- `maps/progress.md`: 다른 기기와 agent가 읽는 현재 checkpoint

작성 예제는 `templates/`에 있습니다. 정의와 학습 콘텐츠는 Git에 두고,
개인별 답안·점수·힌트 사용·복습 예정일 같은 상세 기록은 Web UI의 progress
store에 둡니다.

## Continue with an agent

Codex-compatible agent는
`.agents/skills/continue-study/SKILL.md`를 사용해 현재 checkpoint 확인,
개념 설명, 과제, 시험, 오답 교정, 복습 예약, sync를 같은 규칙으로 수행할
수 있습니다. 다른 runtime도 `REAMDE_FOR_AGENTS.md`의 계약을 구현하면
됩니다.

학습을 재개할 때는 다음처럼 요청합니다.

```text
$continue-study Git 학습을 이전 checkpoint부터 이어서 진행해줘.
```

## Web UI template

`.agents/skills/continue-study/assets/web-ui-template/`에는 dashboard와 하나의
완전한 학습 cycle을 보여주는 Astro 예제가 있습니다. 설치, 로컬 실행,
GitHub Pages 배포, Supabase 기반 기기 간 progress 동기화 방법은
`.agents/skills/continue-study/references/web-ui.md`를 따릅니다.

개발용 local progress는 현재 브라우저에만 남으므로 기기 간 동기화가
아닙니다. 그 표현은 인증된 저장소와 사용자별 접근 제어가 연결된 뒤에만
사용합니다.

## Setup

```bash
gh repo clone alsrl8/mingi-miles-study
cd mingi-miles-study
scripts/learn status
```

## Commands

새 학습 기록을 만듭니다. 본문을 생략하면 제목을 본문으로 사용합니다.

```bash
scripts/learn capture "Pull 전에 push하지 않기" \
  "여러 기기에서 편집할 때는 pull --rebase를 먼저 실행한다."
```

원격 변경을 받고, 로컬 변경을 검사·커밋·push합니다.

```bash
scripts/learn sync
```

정리할 inbox 기록을 topic 브랜치와 문서로 전환합니다.

```bash
scripts/learn distill inbox/2026/07/<note>.md "Reliable Git Sync"
```

repo가 없는 환경에서는 GitHub Issue로 기록합니다.

```bash
scripts/learn issue "새로 배운 내용" "관찰과 다시 확인할 질문"
```

현재 branch, 변경 파일, 최근 commit과 remote를 확인합니다.

```bash
scripts/learn status
```

## Public repository boundary

이 저장소에는 공개해도 되는 일반화된 학습만 기록합니다. 고객·회사 자료의
원문, 메시지 전문, 내부 주소, 계정 정보, 자격증명, 비공개 첨부파일은
저장하지 않습니다. 구체적인 업무 경험은 재사용 가능한 원칙으로 정리한 뒤
기록합니다. 공개 여부가 불분명하면 작성하거나 push하지 않습니다.

## Verification

```bash
python3 scripts/validate.py
bash tests/test_learn.sh
git diff --check
```
