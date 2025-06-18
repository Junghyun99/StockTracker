# GitHub Actions 자동화 설정 가이드

## 🤖 구현된 자동화 기능

### 1. 자동 데이터 업데이트 (`update-stock-data.yml`)
- **실행 시점:**
  - 평일 한국시간 오전 9시 (장 시작 전)
  - 평일 한국시간 오후 3시 30분 (장 마감 후)
  - 매일 오후 6시 (전체 점검)
  - 수동 실행 가능
  - `data/stocks.json` 파일 변경 시

- **수행 작업:**
  - 모든 추적 종목의 주가 데이터 새로고침
  - 하락률 재계산
  - 정적 HTML 페이지 자동 생성
  - GitHub Pages 자동 배포

### 2. 수동 업데이트 (`manual-update.yml`)
- **실행 방법:** GitHub 웹사이트에서 Actions 탭 → "Manual Stock Data Update" → "Run workflow"
- **업데이트 옵션:**
  - `all`: 모든 종목 업데이트
  - `korean_only`: 한국 주식만 업데이트
  - `us_only`: 미국 주식만 업데이트

### 3. GitHub Pages 자동 배포 (`deploy-pages.yml`)
- `docs/` 폴더 변경 시 자동 배포
- 데이터 업데이트 완료 후 자동 배포

## 🚀 설정 방법

### 1단계: 리포지토리 생성 및 파일 업로드
```bash
# 필수 업로드 파일들
.github/workflows/
├── update-stock-data.yml
├── manual-update.yml
└── deploy-pages.yml

# 애플리케이션 파일들
app.py
stock_tracker.py
stock_search.py
static_export.py
data/stocks.json
docs/ (정적 파일들)
```

### 2단계: GitHub Pages 설정
1. 리포지토리 → Settings → Pages
2. Source: "GitHub Actions" 선택
3. 자동으로 `deploy-pages.yml` 워크플로우가 활성화됨

### 3단계: Actions 권한 설정
1. 리포지토리 → Settings → Actions → General
2. "Workflow permissions" 섹션에서:
   - ✅ "Read and write permissions" 선택
   - ✅ "Allow GitHub Actions to create and approve pull requests" 체크

### 4단계: 초기 실행
1. Actions 탭 → "Manual Stock Data Update"
2. "Run workflow" 클릭 → "all" 선택 → "Run workflow"
3. 첫 실행으로 데이터 업데이트 및 정적 페이지 생성

## 📊 모니터링 및 관리

### 실행 로그 확인
- Actions 탭에서 각 워크플로우 실행 결과 확인
- 실패 시 상세 로그로 문제 진단 가능

### 업데이트 결과 확인
각 실행 후 다음 정보를 Summary에서 확인:
- 총 추적 종목 수
- 주의권/경고권/발동권 분류 현황
- 종목별 상세 하락률 테이블

### 수동 업데이트 시나리오
- **장중 실시간 확인**: `korean_only` 또는 `us_only` 사용
- **전체 점검**: `all` 사용
- **긴급 상황**: 언제든 수동 실행 가능

## ⚙️ 커스터마이징

### 실행 시간 변경
`update-stock-data.yml`의 cron 스케줄 수정:
```yaml
schedule:
  - cron: '0 0 * * 1-5'  # 평일 한국시간 09:00
  - cron: '30 6 * * 1-5' # 평일 한국시간 15:30
  - cron: '0 9 * * *'    # 매일 18:00
```

### 에러 처리
- 네트워크 오류나 API 제한 시 워크플로우는 계속 진행
- 부분적 업데이트 실패해도 전체 프로세스 중단되지 않음
- 변경사항 없을 시 불필요한 커밋 생성하지 않음

## 🔍 트러블슈팅

### 워크플로우가 실행되지 않는 경우
1. Actions 권한 설정 확인
2. 브랜치명이 `main` 또는 `master`인지 확인
3. YAML 문법 오류 확인

### 데이터가 업데이트되지 않는 경우
1. `data/stocks.json` 파일 존재 확인
2. yfinance API 응답 상태 확인 (Actions 로그)
3. 종목 코드 형식 확인

### GitHub Pages 배포 실패
1. Pages 설정에서 "GitHub Actions" 소스 선택 확인
2. `docs/` 폴더에 `index.html` 존재 확인
3. 배포 권한 설정 확인

## 📈 예상 효과

### 자동화 이전
- 수동으로 데이터 새로고침 버튼 클릭
- 정적 페이지 수동 생성 및 업로드
- 불규칙한 업데이트 주기

### 자동화 이후
- 장 시간에 맞춘 정기 자동 업데이트
- 실시간 GitHub Pages 반영
- 일관된 데이터 품질 유지
- 24/7 모니터링 가능

이제 GitHub에 리포지토리를 생성하고 이 파일들을 업로드하면 완전 자동화된 주식 추적 시스템이 구축됩니다.