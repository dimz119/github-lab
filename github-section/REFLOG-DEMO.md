# 연습 리포
mkdir reflog-practice
cd reflog-practice
git init -b main
echo "# demo" > README.md
git add README.md
git commit -m "init"

# 커밋 3개 만들기
echo "step 1" >> notes.txt
git add notes.txt
git commit -m "커밋 1"
echo "step 2" >> notes.txt
git commit -am "커밋 2"
echo "step 3" >> notes.txt
git commit -am "커밋 3"
git log --oneline
```
cdf417d (HEAD -> main) 커밋 3
2d85f37 커밋 2
2275929 커밋 1
2f06d3b init
```

# 사고: 커밋 3개를 날린다
git reset --hard HEAD~3
# init만 남아 있다
git log --oneline
```
2f06d3b (HEAD -> main) init
```

# 복구: 날리기 직전 위치를 찾는다
git reflog
```
2f06d3b (HEAD -> main) HEAD@{0}: reset: moving to HEAD~3
cdf417d HEAD@{1}: commit: 커밋 3
2d85f37 HEAD@{2}: commit: 커밋 2
2275929 HEAD@{3}: commit: 커밋 1
2f06d3b (HEAD -> main) HEAD@{4}: commit (initial): init
```

git reset --hard HEAD@{1}
# 커밋 1~3이 돌아왔다
git log --oneline
```
cdf417d (HEAD -> main) 커밋 3
2d85f37 커밋 2
2275929 커밋 1
2f06d3b init
```

# 사고: 가짜 키가 든 .env를 커밋한다
echo "PAYMENT_API_KEY=fake-key-for-practice" > .env
git add .env
git commit -m "실수: .env 커밋"
git log --oneline
```
3d17c83 (HEAD -> main) 실수: .env 커밋
cdf417d 커밋 3
2d85f37 커밋 2
2275929 커밋 1
2f06d3b init
```

# .gitignore에 적어도 이미 추적 중이라 그대로다
echo ".env" >> .gitignore
git ls-files

# 추적에서 빼기 (내 컴퓨터의 파일은 남는다)
git rm --cached .env
git add .gitignore
git commit -m "chore: .env 추적 중지"

# .env가 목록에서 빠졌는지, 파일은 그대로 있는지
git ls-files
ls -a

# 이전 커밋에는 여전히 남아 있다 (슬라이드 8의 이유)
git show HEAD~1:.env


# 로그인 상태 확인 (안 돼 있으면 gh auth login)
gh auth status
# 지금 폴더로 GitHub에 public 리포를 만들고, origin 연결과 main 푸시까지 한 번에
gh repo create reflog-practice --public --source=. --remote=origin --push
# origin이 연결됐는지
git remote -v

git switch main
git pull
git switch -c chore-env-example

# 값은 비우고 이름만
printf 'PAYMENT_API_KEY=\nDATABASE_URL=\n' > .env.example
git add .env.example
git commit -m "chore: .env.example 추가"
git push -u origin chore-env-example
gh pr create --title "chore: .env.example 추가"
