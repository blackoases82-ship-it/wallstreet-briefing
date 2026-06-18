# 배포 & 자동화 가이드 — 나만의 월스트리트

목표 세 가지를 끝까지 연결합니다.
① 아이폰에서 어디서나 열리는 진짜 주소 만들기 (Vercel 배포)
② 매일 아침 6:30 데이터 자동 갱신 (예약 작업 → git push → Vercel 재배포)
③ 매일 아침 메일 받기 (Gmail 초안)

먼저 솔직한 전제부터.

- **메일은 "초안"까지 자동**입니다. 연결된 Gmail 도구가 자동 발송을 지원하지 않아, 매일 아침 Gmail **초안함**에 브리핑이 만들어집니다. 보내기만 누르면 됩니다(또는 그냥 초안함에서 읽어도 됩니다).
- **예약 작업은 이 앱(Claude)이 켜져 있을 때 실행**됩니다. 6:30에 맥/앱이 꺼져 있으면, 다음에 앱을 열 때 실행됩니다.
- **자동 갱신은 git push로 동작**합니다. 아래 1단계에서 GitHub를 한 번 연결해두면, 매일 아침 작업이 자동으로 push → Vercel이 자동 재배포합니다.

---

## 0단계 (먼저, 1분): 아이폰에서 지금 당장 보기 — 임시 방법

배포 전에 같은 와이파이에서 바로 확인하고 싶다면, 맥 터미널에서:

```bash
cd "~/Claude/Projects/투자 브리핑/wallstreet-briefing"
npm install
npm run dev -- -H 0.0.0.0
```

터미널에 뜨는 `Network: http://192.168.x.x:3000` 주소를 아이폰 Safari에 입력.
(맥이 켜져 있고 같은 와이파이일 때만 됩니다. 영구 주소는 아래 배포로.)

---

## 1단계: GitHub에 올리기 (비개발자용 — GitHub Desktop 권장)

GitHub Desktop을 쓰면 명령어 없이 됩니다. 그리고 이렇게 하면 매일 아침 자동 push도
별도 토큰 세팅 없이 macOS 키체인 인증으로 동작합니다.

1. https://desktop.github.com 에서 GitHub Desktop 설치 → GitHub 계정 로그인
   (계정 없으면 https://github.com 에서 무료 가입)
2. File → Add Local Repository → 폴더 선택:
   `~/Claude/Projects/투자 브리핑/wallstreet-briefing`
3. "Publish repository" 클릭 → 이름 `wallstreet-briefing`, **Private 체크** → Publish

> ⚠️ 혹시 git이 "lock" 오류를 내면, 터미널에서 한 번만:
> ```bash
> cd "~/Claude/Projects/투자 브리핑/wallstreet-briefing"
> rm -f .git/*.lock .git/refs/heads/*.lock .git/objects/*.lock
> ```
> 그래도 이상하면 `.git` 폴더를 삭제하고 GitHub Desktop에서 새로 init 해도 됩니다.

명령어가 더 편하면:

```bash
cd "~/Claude/Projects/투자 브리핑/wallstreet-briefing"
git branch -M main
# GitHub에서 빈 repo를 먼저 만든 뒤:
git remote add origin https://github.com/<your-id>/wallstreet-briefing.git
git push -u origin main
```

---

## 2단계: Vercel 배포 (무료, 영구 주소)

1. https://vercel.com 접속 → "Continue with GitHub"로 로그인
2. **Add New… → Project** → 방금 만든 `wallstreet-briefing` repo를 **Import**
3. 프레임워크가 **Next.js**로 자동 인식됨 → 그대로 **Deploy**
4. 1~2분 뒤 `https://wallstreet-briefing-xxxx.vercel.app` 같은 주소가 나옵니다

이 주소는 어디서나 열립니다. 아이폰 Safari에서 열고
**공유 → 홈 화면에 추가**하면 앱 아이콘처럼 설치됩니다 (PWA).

> 앞으로 GitHub에 push될 때마다 Vercel이 자동으로 새로 배포합니다.
> 즉, 매일 아침 예약 작업이 데이터를 push하면 사이트가 자동으로 최신이 됩니다.

---

## 3단계: 매일 아침 자동 갱신 + 메일 (이미 예약됨)

예약 작업 **wallstreet-morning-briefing** 이 매일 약 06:30(한국시간)에 실행되도록
이미 등록돼 있습니다. 사이드바 **Scheduled** 에서 확인/수정/즉시실행 가능합니다.

매일 작업이 하는 일:
1. 연결된 도구로 미국·한국 종목 실시세/목표가/뉴스 수집
2. `src/data/briefing.json` 을 실데이터로 갱신
3. `git push` → Vercel 자동 재배포 (1단계 GitHub 연결이 돼 있어야 함)
4. `blackoases82@gmail.com` 로 브리핑 요약 **Gmail 초안** 생성

### 지금 한 번 테스트하기 (권장)
Scheduled → wallstreet-morning-briefing → **Run now**.
첫 실행 때 도구 사용 권한을 물어보면 허용해 주세요. 한 번 허용하면
다음부터는 자동 실행됩니다. (시세/뉴스 도구 + Gmail + git 사용)

---

## 자주 묻는 것

**Q. 6:30에 맥이 꺼져 있으면?**
그 시각엔 안 돌고, 다음에 Claude 앱을 열 때 한 번 실행됩니다.

**Q. 메일이 안 와요.**
자동 "발송"이 아니라 Gmail **초안함**에 생깁니다. 초안함을 확인하세요.
완전 자동 발송이 필요하면, 발송 가능한 메일 연동을 추가로 붙여야 합니다(다음 단계).

**Q. 데이터가 일부만 실데이터예요.**
초기 파일은 NVDA만 실데이터, 나머지는 샘플입니다. 예약 작업이 한 번 돌면
관심종목 전체가 실데이터로 채워집니다. (지금 Run now 하면 바로 채워집니다.)

**Q. 한국 종목 목표가가 비어요.**
해외 데이터 소스가 한국 종목 목표가를 항상 주지는 않습니다. 없으면 "-"로
표시되고 안전마진은 "계산 제외"로 처리됩니다(설계된 동작).

---

## 다음 단계 후보
실데이터 전체 자동화는 이미 됩니다. 추가로 원하면:
- 메일 **자동 발송**(초안 아님) 연동
- 텔레그램/푸시 알림
- 종목 상세 페이지, 안전마진 히스토리 차트
- 관심종목 앱에서 직접 편집
