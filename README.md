# 한국 주식 추적기

한국 및 해외 주식의 고점 대비 하락률을 추적하고 분석하는 웹 애플리케이션입니다.

## 🚀 GitHub Pages 데모

**정적 버전:** [여기를 클릭하여 GitHub Pages에서 확인하세요](https://username.github.io/korean-stock-tracker/)

> GitHub Pages 버전은 정적 HTML로, 실시간 데이터 업데이트나 종목 추가/삭제 기능은 제공되지 않습니다.

## ✨ 주요 기능

### 📊 하락률 분류 시스템
- **주의권 (10% 이하)**: 상대적으로 안정한 구간
- **경고권 (10-30%)**: 주의 깊게 관찰해야 할 구간  
- **발동권 (30% 이상)**: 손절매를 고려해야 할 구간

### 🌏 다중 시장 지원
- **한국 주식**: KRX (코스피, 코스닥)
- **미국 주식**: NASDAQ, NYSE
- **일본 주식**: 도쿄증권거래소
- **중국 주식**: 상하이, 선전증권거래소

### 📈 실시간 분석
- 최근 3개월 내 최고가 기준 하락률 계산
- 실시간 주가 데이터 연동
- 자동 상태 분류 및 색상 구분

## 🛠️ 기술 스택

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Source**: yfinance API
- **Styling**: Bootstrap Dark Theme

## 📁 프로젝트 구조

```
korean-stock-tracker/
├── app.py                 # Flask 메인 애플리케이션
├── stock_tracker.py       # 주식 추적 로직
├── stock_search.py        # 종목 검색 기능
├── static_export.py       # GitHub Pages용 정적 파일 생성
├── templates/
│   ├── base.html
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── data/
│   └── stocks.json        # 추적 종목 데이터
└── docs/                  # GitHub Pages 정적 파일
    ├── index.html
    ├── stocks_data.json
    └── static/
```

## 🚀 로컬 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/username/korean-stock-tracker.git
cd korean-stock-tracker
```

### 2. 의존성 설치
```bash
pip install flask yfinance requests
```

### 3. 애플리케이션 실행
```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

## 📤 GitHub Pages 배포 방법

### 1. GitHub 리포지토리 생성
1. GitHub에서 새 리포지토리 생성 (`korean-stock-tracker`)
2. 로컬 파일들을 리포지토리에 업로드

### 2. GitHub Pages 설정
1. 리포지토리 → Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main` 또는 `master`
4. Folder: `/docs`
5. Save 클릭

### 3. 정적 파일 생성
```bash
python static_export.py
```

이 명령어로 `docs/` 디렉토리에 GitHub Pages용 정적 HTML 파일이 생성됩니다.

### 4. 변경사항 커밋 및 푸시
```bash
git add .
git commit -m "Add static GitHub Pages version"
git push origin main
```

몇 분 후 `https://username.github.io/korean-stock-tracker/`에서 사이트를 확인할 수 있습니다.

## 📋 사용 가이드

### 종목 추가
1. 종목 검색창에 종목명 입력 (예: "삼성전자")
2. 검색 결과에서 원하는 종목 선택
3. "종목 추가" 버튼 클릭

### 하락률 분석
- 각 종목의 최근 3개월 최고가 대비 현재가 하락률을 자동 계산
- 색상으로 위험도 구분:
  - 회색: 주의권 (10% 이하)
  - 노란색: 경고권 (10-30%)
  - 빨간색: 발동권 (30% 이상)

### 데이터 새로고침
- "전체 새로고침" 버튼으로 모든 종목 데이터 업데이트
- 종목 추가 시 자동으로 초기 데이터 로드

## 🔧 설정

### 환경 변수
```bash
export SESSION_SECRET="your-secret-key-here"
```

### 데이터 저장
- 추적 종목 정보는 `data/stocks.json`에 저장
- JSON 형태로 종목 코드, 이름, 가격 정보 등 포함

## 📊 API 엔드포인트

- `GET /`: 메인 페이지
- `POST /add_stock`: 종목 추가
- `GET /remove_stock/<code>`: 종목 삭제
- `GET /refresh`: 전체 데이터 새로고침
- `GET /api/search_stock`: 종목 검색
- `GET /api/popular_stocks`: 인기 종목 목록

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## ⚠️ 주의사항

- yfinance API는 교육 목적으로만 사용하세요
- 실제 투자 결정시에는 전문가와 상담하세요
- 데이터는 실시간이 아닐 수 있습니다
- GitHub Pages 버전은 정적 데이터만 표시됩니다

## 📧 연락처

프로젝트 관련 문의: [your-email@example.com](mailto:your-email@example.com)

프로젝트 링크: [https://github.com/username/korean-stock-tracker](https://github.com/username/korean-stock-tracker)

---

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!**