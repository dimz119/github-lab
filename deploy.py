"""배포 시뮬레이션. 실제 flyctl deploy 대신 환경 변수로 받은 토큰을 확인만 한다."""
import os
import sys

token = os.environ.get("FLY_API_TOKEN")
if not token:
    # CI에서만 실패한다면 가장 흔한 원인: secret을 env로 넘기지 않음
    sys.exit("FLY_API_TOKEN이 없습니다. Settings → Secrets and variables → Actions에 등록했는지 확인하세요.")

# 토큰 값은 절대 출력하지 않는다. 받았다는 사실만 알린다.
print("FLY_API_TOKEN을 받았습니다. 배포를 시작합니다 (시뮬레이션).")
print("배포 완료")
