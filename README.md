# github-lab — Git·GitHub 협업 실습 리포

좌석 예매 서비스(TicketDrop)를 소재로 Git 내부 구조부터 PR, 코드 리뷰, GitHub Actions CI, Secret까지
GitHub 섹션의 실습을 한 리포에서 진행한다. 코드는 일부러 작게 유지하고, 실습의 대상은 **커밋·브랜치·PR·워크플로**다.

> 리포 이름은 `ticketdrop`에서 `github-lab`으로 바뀌었다. 예전 주소(`dimz119/ticketdrop`)는 GitHub이 새 주소로 자동 연결한다.
> 예전 주소로 clone한 경우 `git remote set-url origin git@github.com:dimz119/github-lab.git`으로 바꿔 둔다.

## 실습 구성

| 주제 | 무엇을 배우나 | 실습 파일 · PR |
| --- | --- | --- |
| Git 내부 구조 | 커밋 그래프, 브랜치는 해시를 가리키는 이름표, `HEAD` | [`github-section/LOOP-DEMO.md`](github-section/LOOP-DEMO.md) |
| 첫 PR | 브랜치 → push → PR → merge | PR #1 `day06-seat-hold` |
| PR 템플릿 | 무엇을·왜·어떻게 확인했나, 셀프 리뷰 체크리스트 | [`.github/pull_request_template.md`](.github/pull_request_template.md), PR #2, #3 |
| PR CI | PR마다 pytest를 돌려 체크로 표시 | [`.github/workflows/ci.yml`](.github/workflows/ci.yml), PR #4 |
| CI 실패 시연 | 테스트를 깨는 PR이 빨간 체크로 막히는 모습 | PR #5, #6 (닫힘) |
| Secret과 배포 | Actions secret 등록, 로그 마스킹, main에서만 배포 | [`deploy.py`](deploy.py), PR #7 |
| rebase `--onto` | squash merge 뒤 쌓인 브랜치를 main 위로 옮기기 | [`github-section/REBASE-DEMO.md`](github-section/REBASE-DEMO.md) |
| reflog와 사고 복구 | `reset --hard` 되돌리기, 커밋한 `.env` 추적 중지, `gh repo create`·`gh pr create` | [`github-section/REFLOG-DEMO.md`](github-section/REFLOG-DEMO.md) |

`github-section/`의 데모는 이 리포가 아니라 **새 연습용 폴더**(`rebase-onto-practice`, `reflog-practice`)를 만들어 따라 하는 스크립트다.
이 리포 안에서 실행하지 않는다.

## 실습 대상 코드

| 파일 | 내용 |
| --- | --- |
| `models.py` | `Seat`, `Event` 데이터클래스 |
| `seat_service.py` | 좌석 홀드(`hold`), 해제(`release`), 남은 좌석 조회 |
| `test_seat_service.py` | pytest 테스트 5개 |
| `deploy.py` | 배포 시뮬레이션. `FLY_API_TOKEN`이 있는지만 확인하고 값은 출력하지 않는다 |

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

## 리포 설정

실습 흐름이 아래 설정을 전제로 한다. 리포를 fork하거나 새로 만들었다면 같은 값으로 맞춘다.

| 설정 | 값 | 위치 |
| --- | --- | --- |
| merge 방식 | **squash merge만** 허용 (merge commit, rebase merge 끔) | Settings → General → Pull Requests |
| merge 후 브랜치 삭제 | 켬 | Settings → General → Automatically delete head branches |
| Actions secret | `FLY_API_TOKEN` (아무 가짜 값) | Settings → Secrets and variables → Actions |

squash merge만 쓰기 때문에 PR 제목이 그대로 main의 커밋 메시지가 된다. 그래서 PR 템플릿이 제목 형식(`타입: 무엇을 했나`)을 안내한다.

### 브랜치 보호 (main)

CI의 `test` 체크가 실패한 PR을 merge할 수 없게 하려면 Settings → Rules → Rulesets에서 `main`에
"Require a pull request before merging"과 "Require status checks to pass"(`test`)를 켠다.

> 이 리포는 현재 **private**이라 무료 플랜에서는 Rulesets와 Branch protection을 쓸 수 없다(API가 403을 돌려준다).
> 실습하려면 리포를 public으로 바꾸거나 GitHub Pro 이상이 필요하다.

## CI 워크플로

`.github/workflows/ci.yml` 하나에 job `test`가 있다. 이 job 이름이 PR 화면의 체크 이름이 된다.

| 트리거 | 실행되는 step |
| --- | --- |
| `pull_request` | 의존성 설치 → `pytest` (Secret 데모·Deploy는 skipped) |
| `push` to `main` (PR merge) | `pytest` → Secret 마스킹 데모 → Deploy |
| `workflow_dispatch` (Actions 탭에서 수동 실행) | main에서 실행하면 위와 같음 |

- Secret 마스킹 데모는 로그에 찍힌 secret 값이 `***`로 가려지는 것을 보여 주기 위한 것이다. 실제 프로젝트에서는 secret을 `echo`하지 않는다.
- `deploy.py`가 `FLY_API_TOKEN이 없습니다`로 실패하면 secret을 등록하지 않았거나 step의 `env:`로 넘기지 않은 것이다.

## 작업 규칙

1. main에서 직접 커밋하지 않는다. `git switch -c <타입>/<설명>`으로 브랜치를 만든다.
2. push 후 `gh pr create`로 PR을 열고 템플릿을 채운다.
3. CI `test` 체크가 초록색인지 확인하고 squash merge한다.
4. merge 후 `git switch main && git pull`로 로컬 main을 맞춘다.
