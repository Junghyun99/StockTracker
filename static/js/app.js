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
            
            // 종목 코드 검증 (6자리 숫자)
            if (!/^\d{6}$/.test(stockCode)) {
                e.preventDefault();
                showAlert('종목 코드는 6자리 숫자여야 합니다. (예: 005930)', 'danger');
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

console.log('한국 주식 추적기 JavaScript 로드 완료');
