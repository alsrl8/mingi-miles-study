# mingi-miles-study

Miles가 여러 기기에서 배운 내용을 수집하고, 다시 설명할 수 있는 지식으로
정리하기 위한 공개 학습 저장소입니다. 이 저장소 자체가 정본이며 어느
기기에서든 clone한 뒤 같은 방식으로 기록할 수 있습니다.

## Learning loop

1. `inbox/`에 경험과 질문을 짧게 기록합니다.
2. 반복해서 쓸 가치가 있는 기록을 `topics/` 문서로 정리합니다.
3. 기존 topic과 연결하고, 다시 답해볼 질문을 `reviews/questions/`에 둡니다.
4. 주간 회고를 `reviews/weekly/`에 기록합니다.
5. `maps/`에서 주제별 학습 흐름을 관리합니다.

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
기록합니다.

## Verification

```bash
python3 scripts/validate.py
bash tests/test_learn.sh
git diff --check
```
