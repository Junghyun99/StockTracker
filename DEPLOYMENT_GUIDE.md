# GitHub Pages 배포 가이드

## 📋 현재 상태
- ✅ Flask 애플리케이션 완성
- ✅ 정적 HTML 버전 생성 (`docs/` 폴더)
- ✅ GitHub Pages 준비 완료

## 🚀 GitHub Pages 배포 단계

### 1단계: GitHub 리포지토리 생성
1. [GitHub](https://github.com)에 로그인
2. "New repository" 클릭
3. Repository name: `korean-stock-tracker`
4. Public으로 설정
5. "Create repository" 클릭

### 2단계: 파일 업로드
Replit에서 다음 파일들을 다운로드하여 GitHub에 업로드:

**필수 파일들:**
```
docs/
├── index.html          # 메인 페이지
├── stocks_data.json    # 현재 데이터
└── static/
    ├── css/style.css   # 스타일시트
    └── js/app.js       # JavaScript

README.md               # 프로젝트 설명
.gitignore             # Git 무시 파일
```

### 3단계: GitHub Pages 활성화
1. 리포지토리 페이지에서 "Settings" 탭 클릭
2. 왼쪽 메뉴에서 "Pages" 클릭
3. Source: "Deploy from a branch" 선택
4. Branch: "main" (또는 "master") 선택
5. Folder: "/docs" 선택
6. "Save" 버튼 클릭

### 4단계: 배포 확인
- 5-10분 후 `https://[USERNAME].github.io/korean-stock-tracker/` 접속
- 정적 버전 웹사이트 확인

## 📁 파일 다운로드 방법

### Replit에서 파일 다운로드:
1. 파일 탐색기에서 `docs` 폴더 우클릭
2. "Download" 선택 (ZIP 파일로 다운로드)
3. ZIP 파일 압축 해제 후 GitHub에 업로드

### 개별 파일 다운로드:
- `docs/index.html`
- `docs/stocks_data.json`  
- `docs/static/css/style.css`
- `docs/static/js/app.js`
- `README.md`
- `.gitignore`

## 🔄 데이터 업데이트 방법

정적 버전의 데이터를 업데이트하려면:

1. Replit에서 `python static_export.py` 실행
2. 새로 생성된 `docs/` 폴더 파일들을 GitHub에 재업로드
3. 자동으로 GitHub Pages가 업데이트됨

## ⚡ 빠른 배포 체크리스트

- [ ] GitHub 계정 준비
- [ ] 새 리포지토리 생성 (`korean-stock-tracker`)
- [ ] `docs/` 폴더 전체 업로드
- [ ] `README.md`, `.gitignore` 업로드
- [ ] GitHub Pages 설정 (Source: Deploy from branch, Folder: /docs)
- [ ] 5-10분 후 웹사이트 접속 확인

## 🌐 최종 결과

배포 후 다음 두 버전을 사용할 수 있습니다:

1. **동적 버전 (Replit)**: 
   - 실시간 데이터 업데이트
   - 종목 추가/삭제 기능
   - Flask 백엔드 필요

2. **정적 버전 (GitHub Pages)**:
   - 빠른 로딩
   - 무료 호스팅
   - 읽기 전용 (데이터 추가/수정 불가)

두 버전 모두 동일한 UI와 하락률 분석 기능을 제공합니다.