// 한국 주식 추적 애플리케이션 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('한국 주식 추적기 초기화됨');
    
    // 자동 알림 닫기
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        });
    }, 5000); // 5초 후 자동 닫기
    
    // 종목 검색 기능 초기화
    initStockSearch();
    
    // 폼 검증
    const addStockForm = document.querySelector('form[action="/add_stock"]');
    if (addStockForm) {
        addStockForm.addEventListener('submit', function(e) {
            const stockCode = document.getElementById('stock_code').value.trim();
            const stockName = document.getElementById('stock_name').value.trim();
            
            if (!stockCode || !stockName) {
                e.preventDefault();
                showAlert('종목 코드와 종목명을 모두 입력해주세요.', 'danger');
                return;
            }
            
            // 종목 코드 검증 (한국 주식: 6자리 숫자, 해외 주식: 영문 포함)
            const isKoreanStock = /^\d{6}$/.test(stockCode);
            const isOverseaStock = /^[A-Z]{1,5}(\.[A-Z])?$/.test(stockCode) || /^\d{4}\.[A-Z]$/.test(stockCode);
            
            if (!isKoreanStock && !isOverseaStock) {
                e.preventDefault();
                showAlert('올바른 종목 코드를 입력해주세요. (한국: 005930, 미국: AAPL, 일본: 7203.T)', 'danger');
                return;
            }
            
            // 로딩 상태 표시
            const submitBtn = addStockForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading me-2"></span>추가 중...';
            submitBtn.disabled = true;
            
            // 폼 제출 후 원래 상태로 복원 (페이지 리로드 시)
            setTimeout(function() {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 3000);
        });
    }
    
    // 새로고침 버튼 로딩 효과
    const refreshLinks = document.querySelectorAll('a[href="/refresh_data"]');
    refreshLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading me-2"></span>새로고침 중...';
            this.classList.add('disabled');
            
            // 타임아웃으로 복원 (실제로는 페이지가 리로드됨)
            setTimeout(function() {
                link.innerHTML = originalText;
                link.classList.remove('disabled');
            }, 5000);
        });
    });
    
    // 삭제 확인 대화상자 개선
    const deleteLinks = document.querySelectorAll('a[onclick*="confirm"]');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const stockName = this.closest('tr').querySelector('td:first-child strong').textContent;
            
            if (confirm(`정말로 "${stockName}" 종목을 삭제하시겠습니까?\n\n이 작업은 되돌릴 수 없습니다.`)) {
                window.location.href = this.href;
            }
        });
    });
    
    // 테이블 정렬 기능
    addTableSorting();
    
    // 실시간 시계 표시
    updateClock();
    setInterval(updateClock, 1000);
    
    // 키보드 단축키
    document.addEventListener('keydown', function(e) {
        // Ctrl + R: 새로고침
        if (e.ctrlKey && e.key === 'r') {
            e.preventDefault();
            window.location.href = '/refresh_data';
        }
        
        // Ctrl + A: 종목 추가 폼으로 포커스
        if (e.ctrlKey && e.key === 'a') {
            e.preventDefault();
            const stockCodeInput = document.getElementById('stock_code');
            if (stockCodeInput) {
                stockCodeInput.focus();
            }
        }
    });
});

// 알림 표시 함수
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show mt-3`;
    alert.innerHTML = `
        <i class="fas fa-${type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // 기존 알림 아래에 추가
    const existingAlerts = alertContainer.querySelectorAll('.alert');
    if (existingAlerts.length > 0) {
        existingAlerts[existingAlerts.length - 1].after(alert);
    } else {
        alertContainer.insertBefore(alert, alertContainer.firstChild);
    }
    
    // 5초 후 자동 제거
    setTimeout(function() {
        alert.remove();
    }, 5000);
}

// 테이블 정렬 기능
function addTableSorting() {
    const table = document.querySelector('.table');
    if (!table) return;
    
    const headers = table.querySelectorAll('th');
    headers.forEach(function(header, index) {
        // 특정 컬럼만 정렬 가능하게 설정
        if (index === 0 || index === 2 || index === 3 || index === 5) { // 종목명, 현재가, 최근고점, 하락률
            header.style.cursor = 'pointer';
            header.title = '클릭하여 정렬';
            
            header.addEventListener('click', function() {
                sortTable(table, index);
            });
        }
    });
}

// 테이블 정렬 실행
function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // 현재 정렬 방향 확인
    const currentDirection = table.dataset.sortDirection || 'asc';
    const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
    table.dataset.sortDirection = newDirection;
    
    rows.sort(function(a, b) {
        let aValue = a.cells[columnIndex].textContent.trim();
        let bValue = b.cells[columnIndex].textContent.trim();
        
        // 숫자 값 처리 (가격, 하락률)
        if (columnIndex === 2 || columnIndex === 3 || columnIndex === 5) {
            aValue = parseFloat(aValue.replace(/[^\d.-]/g, '')) || 0;
            bValue = parseFloat(bValue.replace(/[^\d.-]/g, '')) || 0;
        }
        
        if (newDirection === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });
    
    // 정렬된 행들을 다시 추가
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
    
    // 정렬 표시 업데이트
    updateSortIndicators(table, columnIndex, newDirection);
}

// 정렬 표시기 업데이트
function updateSortIndicators(table, sortedColumnIndex, direction) {
    const headers = table.querySelectorAll('th');
    
    headers.forEach(function(header, index) {
        // 기존 정렬 표시 제거
        header.innerHTML = header.innerHTML.replace(/ <i class="fas fa-sort.*?"><\/i>/g, '');
        
        // 정렬된 컬럼에 표시 추가
        if (index === sortedColumnIndex) {
            const icon = direction === 'asc' ? 'fa-sort-up' : 'fa-sort-down';
            header.innerHTML += ` <i class="fas ${icon}"></i>`;
        }
    });
}

// 실시간 시계
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    // 시계 표시할 위치가 있다면 업데이트
    const clockElement = document.getElementById('current-time');
    if (clockElement) {
        clockElement.textContent = timeString;
    }
}

// 숫자 포맷팅 함수
function formatNumber(num) {
    return new Intl.NumberFormat('ko-KR').format(num);
}

// 가격 포맷팅 함수
function formatPrice(price) {
    return formatNumber(price) + '원';
}

// 백분율 포맷팅 함수
function formatPercentage(value, decimals = 2) {
    return value.toFixed(decimals) + '%';
}

// 로컬 스토리지에 사용자 설정 저장
function saveUserSettings() {
    const settings = {
        autoRefresh: document.getElementById('auto-refresh')?.checked || false,
        sortColumn: document.querySelector('.table')?.dataset.sortColumn || 0,
        sortDirection: document.querySelector('.table')?.dataset.sortDirection || 'asc'
    };
    
    localStorage.setItem('stockTrackerSettings', JSON.stringify(settings));
}

// 사용자 설정 로드
function loadUserSettings() {
    const settingsStr = localStorage.getItem('stockTrackerSettings');
    if (settingsStr) {
        try {
            const settings = JSON.parse(settingsStr);
            
            // 자동 새로고침 설정 적용
            const autoRefreshCheckbox = document.getElementById('auto-refresh');
            if (autoRefreshCheckbox) {
                autoRefreshCheckbox.checked = settings.autoRefresh;
            }
            
            return settings;
        } catch (e) {
            console.error('설정 로드 실패:', e);
        }
    }
    
    return {};
}

// 페이지 언로드 시 설정 저장
window.addEventListener('beforeunload', saveUserSettings);

// 오류 처리
window.addEventListener('error', function(e) {
    console.error('JavaScript 오류:', e.error);
    showAlert('페이지에서 오류가 발생했습니다. 페이지를 새로고침해주세요.', 'danger');
});

// 네트워크 상태 모니터링
window.addEventListener('online', function() {
    showAlert('인터넷 연결이 복구되었습니다.', 'success');
});

window.addEventListener('offline', function() {
    showAlert('인터넷 연결이 끊어졌습니다. 연결을 확인해주세요.', 'warning');
});

// 종목 검색 기능 초기화
function initStockSearch() {
    const searchInput = document.getElementById('stock_search');
    const searchBtn = document.getElementById('search_btn');
    const searchResults = document.getElementById('search_results');
    const searchResultsList = document.getElementById('search_results_list');
    const stockCodeInput = document.getElementById('stock_code');
    const stockNameInput = document.getElementById('stock_name');
    const addStockBtn = document.getElementById('add_stock_btn');
    
    // 인기 종목 버튼 클릭 이벤트
    const popularStockBtns = document.querySelectorAll('#popular_stocks button');
    popularStockBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const code = this.getAttribute('data-code');
            const name = this.getAttribute('data-name');
            selectStock(code, name);
        });
    });
    
    // 검색 입력 이벤트
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                hideSearchResults();
                return;
            }
            
            // 디바운스 적용 (500ms 후 검색)
            searchTimeout = setTimeout(function() {
                searchStocks(query);
            }, 500);
        });
        
        // 엔터키 검색
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const query = this.value.trim();
                if (query.length >= 2) {
                    searchStocks(query);
                }
            }
        });
    }
    
    // 검색 버튼 클릭
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const query = searchInput.value.trim();
            if (query.length >= 2) {
                searchStocks(query);
            } else {
                showAlert('검색어는 2글자 이상 입력해주세요.', 'warning');
            }
        });
    }
    
    // 검색 결과 숨기기 (외부 클릭 시)
    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && !searchInput.contains(e.target)) {
            hideSearchResults();
        }
    });
}

// 종목 검색 실행
function searchStocks(query) {
    const searchBtn = document.getElementById('search_btn');
    const originalText = searchBtn.innerHTML;
    
    // 로딩 상태 표시
    searchBtn.innerHTML = '<span class="loading"></span>';
    searchBtn.disabled = true;
    
    fetch(`/api/search_stock?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displaySearchResults(data.results);
            } else {
                showAlert(data.error || '검색 중 오류가 발생했습니다.', 'danger');
                hideSearchResults();
            }
        })
        .catch(error => {
            console.error('검색 오류:', error);
            showAlert('검색 중 오류가 발생했습니다.', 'danger');
            hideSearchResults();
        })
        .finally(() => {
            // 로딩 상태 해제
            searchBtn.innerHTML = originalText;
            searchBtn.disabled = false;
        });
}

// 검색 결과 표시
function displaySearchResults(results) {
    const searchResults = document.getElementById('search_results');
    const searchResultsList = document.getElementById('search_results_list');
    
    if (!results || results.length === 0) {
        searchResultsList.innerHTML = '<p class="text-muted mb-0">검색 결과가 없습니다.</p>';
        searchResults.style.display = 'block';
        return;
    }
    
    let html = '';
    results.forEach(function(stock) {
        html += `
            <div class="search-result-item d-flex justify-content-between align-items-center py-2 px-2 border-bottom" 
                 style="cursor: pointer;" 
                 data-code="${stock.code}" 
                 data-name="${stock.name}">
                <div>
                    <strong>${stock.name}</strong>
                    <br>
                    <small class="text-muted">${stock.code} (${stock.market || 'KOSPI/KOSDAQ'})</small>
                </div>
                <button type="button" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
        `;
    });
    
    searchResultsList.innerHTML = html;
    searchResults.style.display = 'block';
    
    // 검색 결과 항목 클릭 이벤트
    const resultItems = searchResultsList.querySelectorAll('.search-result-item');
    resultItems.forEach(function(item) {
        item.addEventListener('click', function() {
            const code = this.getAttribute('data-code');
            const name = this.getAttribute('data-name');
            selectStock(code, name);
        });
    });
}

// 검색 결과 숨기기
function hideSearchResults() {
    const searchResults = document.getElementById('search_results');
    if (searchResults) {
        searchResults.style.display = 'none';
    }
}

// 종목 선택
function selectStock(code, name) {
    const stockCodeInput = document.getElementById('stock_code');
    const stockNameInput = document.getElementById('stock_name');
    const addStockBtn = document.getElementById('add_stock_btn');
    const searchInput = document.getElementById('stock_search');
    
    // 입력 필드에 값 설정
    if (stockCodeInput) stockCodeInput.value = code;
    if (stockNameInput) stockNameInput.value = name;
    
    // 추가 버튼 활성화
    if (addStockBtn) {
        addStockBtn.disabled = false;
        addStockBtn.classList.remove('btn-secondary');
        addStockBtn.classList.add('btn-primary');
    }
    
    // 검색 입력 필드 클리어
    if (searchInput) searchInput.value = '';
    
    // 검색 결과 숨기기
    hideSearchResults();
    
    // 성공 메시지
    showAlert(`${name} (${code}) 종목이 선택되었습니다.`, 'success');
}

console.log('한국 주식 추적기 JavaScript 로드 완료');
