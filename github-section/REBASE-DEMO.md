#!/usr/bin/env bash
set -e

# 연습용 리포 만들기
mkdir rebase-onto-practice
cd rebase-onto-practice
git init -b main

# main: 첫 커밋
printf 'class SeatService:\n    pass\n' > seat.py
git add seat.py
git commit -m "init: SeatService 뼈대"

# day06: 좌석 홀드 (커밋 2개)
git switch -c day06-seat-hold
printf 'class SeatService:\n    def hold(self, seat_id):\n        return True\n' > seat.py
git commit -am "좌석 홀드 추가"
printf 'class SeatService:\n    def hold(self, seat_id, user_id):\n        return True\n' > seat.py
git commit -am "홀드에 user_id 추가"

# day07: day06 위에서 홀드 만료 작업
git switch -c day07-hold-expiry
printf 'def expire_holds():\n    pass\n' > expiry.py
git add expiry.py
git commit -m "홀드 만료 함수 추가"

# 리뷰 반영: day06에 수정 커밋 하나 더
git switch day06-seat-hold
printf 'class SeatService:\n    def hold(self, seat_id: int, user_id: int) -> bool:\n        return True\n' > seat.py
git commit -am "리뷰 반영: 타입 힌트"

# GitHub의 squash merge 흉내: day06 전체를 커밋 하나로 main에
git switch main
git merge --squash day06-seat-hold
git commit -m "feat: 좌석 홀드 (#6)"

# 오늘 작업 브랜치로 돌아와서 그래프 보기
git switch day07-hold-expiry
git log --oneline --graph --all

```
* a552527 (main) feat: 좌석 홀드 (#6)
| * 4df99e8 (day06-seat-hold) 리뷰 반영: 타입 힌트
| | * 825cad4 (HEAD -> day07-hold-expiry) 홀드 만료 함수 추가
| |/
| * 816d276 홀드에 user_id 추가
| * e952765 좌석 홀드 추가
|/
* def3dcd init: SeatService 뼈대
```

# 일부러 평소처럼 rebase → seat.py 충돌이 난다
git rebase main
# 충돌 파일 확인 (마커를 보고 싶으면 cat seat.py)
git status
# 반드시 빠져나온다
git rebase --abort
# 오늘 커밋만 main 위로
git rebase --onto main day06-seat-hold day07-hold-expiry
# 결과 확인
git log --oneline --graph --all
```
* fb25a9d (HEAD -> day07-hold-expiry) 홀드 만료 함수 추가
* 78964b0 (main) feat: 좌석 홀드 (#6)
| * 9ee3445 (day06-seat-hold) 리뷰 반영: 타입 힌트
| * 078e39d 홀드에 user_id 추가
| * cb773b0 좌석 홀드 추가
|/
* 70c5d10 init: SeatService 뼈대
```