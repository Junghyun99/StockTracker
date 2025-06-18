#!/usr/bin/env python3
"""
Flask 애플리케이션의 정적 HTML 버전 생성 스크립트
GitHub Pages 배포용
"""

import os
import json
import shutil
from datetime import datetime
from stock_tracker import StockTracker
from stock_search import StockSearcher

def create_static_html():
    """정적 HTML 파일 생성"""
    
    # 정적 파일 디렉토리 생성
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.makedirs('docs', exist_ok=True)
    os.makedirs('docs/static/css', exist_ok=True)
    os.makedirs('docs/static/js', exist_ok=True)
    
    # CSS, JS 파일 복사
    shutil.copy('static/css/style.css', 'docs/static/css/')
    shutil.copy('static/js/app.js', 'docs/static/js/')
    
    # 데이터 로드
    tracker = StockTracker()
    stocks = tracker.get_tracked_stocks()
    
    # HTML 템플릿 생성
    html_content = f"""<!DOCTYPE html>
<html lang="ko" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한국 주식 추적기</title>
    <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link href="static/css/style.css" rel="stylesheet">
</head>
<body>
    <!-- 네비게이션 바 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-chart-line me-2"></i>
                한국 주식 추적기
            </a>
            <span class="navbar-text">
                <i class="fas fa-clock me-1"></i>
                <span id="current_time">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            </span>
        </div>
    </nav>

    <div class="container mt-4 pb-4">
        <!-- 정적 버전 알림 -->
        <div class="alert alert-info mb-4">
            <i class="fas fa-info-circle me-2"></i>
            <strong>정적 버전:</strong> 이 페이지는 GitHub Pages용 정적 버전입니다. 
            실시간 데이터 업데이트나 종목 추가/삭제 기능은 제공되지 않습니다.
            <br><small>마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>
        </div>

        <!-- 통계 카드 섹션 -->
        <div class="row mb-3">
            <div class="col-12">
                <div class="card">
                    <div class="card-body py-2">
                        <div class="row text-center">
                            <div class="col-3">
                                <div class="d-flex align-items-center justify-content-center">
                                    <i class="fas fa-list text-primary me-2"></i>
                                    <div>
                                        <strong class="h5 mb-0">{len(stocks)}</strong>
                                        <small class="text-muted d-block">추적종목</small>
                                    </div>
                                </div>
                            </div>
                            <div class="col-3">
                                <div class="d-flex align-items-center justify-content-center">
                                    <i class="fas fa-shield text-secondary me-2"></i>
                                    <div>
                                        <strong class="h5 mb-0 text-secondary">{len([s for s in stocks if s.get('decline_status') == 'low'])}</strong>
                                        <small class="text-muted d-block">주의권 (10% 이하)</small>
                                    </div>
                                </div>
                            </div>
                            <div class="col-3">
                                <div class="d-flex align-items-center justify-content-center">
                                    <i class="fas fa-exclamation-triangle text-warning me-2"></i>
                                    <div>
                                        <strong class="h5 mb-0 text-warning">{len([s for s in stocks if s.get('decline_status') == 'medium'])}</strong>
                                        <small class="text-muted d-block">경고권 (10-30%)</small>
                                    </div>
                                </div>
                            </div>
                            <div class="col-3">
                                <div class="d-flex align-items-center justify-content-center">
                                    <i class="fas fa-fire text-danger me-2"></i>
                                    <div>
                                        <strong class="h5 mb-0 text-danger">{len([s for s in stocks if s.get('decline_status') == 'high'])}</strong>
                                        <small class="text-muted d-block">발동권 (30% 이상)</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 추적 종목 목록 -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="fas fa-list me-2"></i>
                            추적 종목 목록
                        </h5>
                    </div>
                    <div class="card-body">
"""

    if stocks:
        html_content += """
                        <div class="table-responsive">
                            <table class="table table-sm table-hover">
                                <thead class="table-dark">
                                    <tr>
                                        <th style="width: 20%;">종목명</th>
                                        <th style="width: 8%;" class="text-center">시장</th>
                                        <th style="width: 12%;" class="text-center">현재가</th>
                                        <th style="width: 12%;" class="text-center">고점</th>
                                        <th style="width: 10%;" class="text-center">하락률</th>
                                        <th style="width: 12%;" class="text-center">고점일</th>
                                        <th style="width: 10%;" class="text-center">상태</th>
                                        <th style="width: 16%;" class="text-center">최종업데이트</th>
                                    </tr>
                                </thead>
                                <tbody>
"""
        
        for stock in stocks:
            status_class = "table-danger" if stock.get('status') == 'error' else ""
            market_color = {
                'KRX': 'primary',
                'US': 'success', 
                'TSE': 'warning'
            }.get(stock.get('market_type', 'KRX'), 'secondary')
            
            decline_color = {
                'low': 'secondary',
                'medium': 'warning',
                'high': 'danger'
            }.get(stock.get('decline_status', 'low'), 'secondary')
            
            status_info = {
                'error': ('bg-danger', 'fas fa-exclamation-triangle', '오류'),
                'no_data': ('bg-warning', 'fas fa-question-circle', '데이터없음'),
                'outdated': ('bg-secondary', 'fas fa-clock', '업데이트필요'),
            }.get(stock.get('status', 'normal'), ('bg-success', 'fas fa-check', '정상'))
            
            html_content += f"""
                                    <tr class="{status_class}">
                                        <td>
                                            <div class="d-flex flex-column">
                                                <strong class="text-truncate" style="max-width: 150px;">{stock.get('name', '')}</strong>
                                                <small class="text-muted">{stock.get('original_code', stock.get('code', ''))}</small>
                                            </div>
                                        </td>
                                        <td class="text-center">
                                            <span class="badge badge-sm bg-{market_color}">
                                                {stock.get('market_display', 'KRX')}
                                            </span>
                                        </td>
                                        <td class="text-center">
                                            <strong>{stock.get('current_price_formatted', '-')}</strong>
                                        </td>
                                        <td class="text-center">
                                            {stock.get('recent_high_formatted', '-')}
                                        </td>
                                        <td class="text-center">
                                            <span class="badge bg-{decline_color}">
                                                {stock.get('decline_rate_formatted', '-')}
                                            </span>
                                        </td>
                                        <td class="text-center">
                                            <div class="d-flex flex-column align-items-center">
                                                <small>{stock.get('recent_high_date', '-')}</small>
                                            </div>
                                        </td>
                                        <td class="text-center">
                                            <span class="badge {status_info[0]}">{status_info[2]}</span>
                                        </td>
                                        <td class="text-center">
                                            <small class="text-muted">{stock.get('last_updated_formatted', '-')}</small>
                                        </td>
                                    </tr>
"""
        
        html_content += """
                                </tbody>
                            </table>
                        </div>
"""
    else:
        html_content += """
                        <div class="text-center py-5">
                            <i class="fas fa-chart-line fa-3x text-muted mb-3"></i>
                            <h4 class="text-muted">추적 중인 종목이 없습니다</h4>
                            <p class="text-muted">동적 버전에서 종목을 추가할 수 있습니다.</p>
                        </div>
"""

    html_content += """
                    </div>
                </div>
            </div>
        </div>

        <!-- 도움말 카드 -->
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-question-circle me-2"></i>
                            사용 가이드
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6><i class="fas fa-info me-2 text-primary"></i>정적 버전 안내</h6>
                                <ul class="list-unstyled">
                                    <li><i class="fas fa-check me-2 text-success"></i>GitHub Pages에서 호스팅</li>
                                    <li><i class="fas fa-check me-2 text-success"></i>빠른 로딩 속도</li>
                                    <li><i class="fas fa-info me-2 text-info"></i>실시간 업데이트 불가</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6><i class="fas fa-chart-line me-2 text-info"></i>하락률 분류 기준</h6>
                                <ul class="list-unstyled">
                                    <li><i class="fas fa-shield me-2 text-secondary"></i><strong>주의권:</strong> 10% 이하 (상대적으로 안정)</li>
                                    <li><i class="fas fa-exclamation-triangle me-2 text-warning"></i><strong>경고권:</strong> 10-30% (주의 깊게 관찰)</li>
                                    <li><i class="fas fa-fire me-2 text-danger"></i><strong>발동권:</strong> 30% 이상 (손절매 고려)</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="mt-5 py-4 bg-dark text-center">
        <div class="container">
            <p class="text-muted mb-0">
                <i class="fas fa-chart-line me-2"></i>
                한국 주식 추적기 - 정적 버전
                <br><small>GitHub Pages 배포용 | 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>
            </p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- 시간 업데이트 스크립트 -->
    <script>
        function updateClock() {{
            const now = new Date();
            const timeString = now.getFullYear() + '-' + 
                             String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                             String(now.getDate()).padStart(2, '0') + ' ' + 
                             String(now.getHours()).padStart(2, '0') + ':' + 
                             String(now.getMinutes()).padStart(2, '0') + ':' + 
                             String(now.getSeconds()).padStart(2, '0');
            document.getElementById('current_time').textContent = timeString;
        }}
        
        // 1초마다 시간 업데이트
        setInterval(updateClock, 1000);
        updateClock(); // 초기 실행
        
        console.log('한국 주식 추적기 정적 버전 로드 완료');
    </script>
</body>
</html>"""

    # HTML 파일 생성
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 데이터 JSON 파일도 생성 (참고용)
    with open('docs/stocks_data.json', 'w', encoding='utf-8') as f:
        json.dump({
            'last_updated': datetime.now().isoformat(),
            'stocks': stocks,
            'total_count': len(stocks),
            'category_counts': {
                'low': len([s for s in stocks if s.get('decline_status') == 'low']),
                'medium': len([s for s in stocks if s.get('decline_status') == 'medium']),
                'high': len([s for s in stocks if s.get('decline_status') == 'high'])
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"정적 HTML 파일이 생성되었습니다: docs/index.html")
    print(f"총 {len(stocks)}개 종목 포함")
    
    return True

if __name__ == '__main__':
    create_static_html()