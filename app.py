import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from stock_tracker import StockTracker
from stock_search import StockSearcher

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize stock tracker and searcher
tracker = StockTracker()
searcher = StockSearcher()

@app.route('/')
def index():
    """메인 페이지 - 추적 종목 목록과 하락률 표시"""
    try:
        stocks = tracker.get_tracked_stocks()
        return render_template('index.html', stocks=stocks)
    except Exception as e:
        logging.error(f"Error loading stocks: {e}")
        flash(f'주식 데이터를 불러오는데 실패했습니다: {str(e)}', 'error')
        return render_template('index.html', stocks=[])

@app.route('/add_stock', methods=['POST'])
def add_stock():
    """새로운 추적 종목 추가"""
    stock_code = request.form.get('stock_code', '').strip()
    stock_name = request.form.get('stock_name', '').strip()
    
    if not stock_code:
        flash('종목 코드를 입력해주세요.', 'error')
        return redirect(url_for('index'))
    
    if not stock_name:
        flash('종목명을 입력해주세요.', 'error')
        return redirect(url_for('index'))
    
    try:
        # 종목 코드에 .KS 추가 (한국 주식)
        if not stock_code.endswith('.KS'):
            stock_code += '.KS'
        
        success = tracker.add_stock(stock_code, stock_name)
        if success:
            flash(f'{stock_name} 종목이 추가되었습니다.', 'success')
        else:
            flash('이미 추가된 종목이거나 유효하지 않은 종목입니다.', 'error')
    except Exception as e:
        logging.error(f"Error adding stock {stock_code}: {e}")
        flash(f'종목 추가에 실패했습니다: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/remove_stock/<stock_code>')
def remove_stock(stock_code):
    """추적 종목 제거"""
    try:
        success = tracker.remove_stock(stock_code)
        if success:
            flash('종목이 제거되었습니다.', 'success')
        else:
            flash('종목 제거에 실패했습니다.', 'error')
    except Exception as e:
        logging.error(f"Error removing stock {stock_code}: {e}")
        flash(f'종목 제거에 실패했습니다: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/refresh_data')
def refresh_data():
    """모든 추적 종목의 데이터 새로고침"""
    try:
        updated_count = tracker.refresh_all_stocks()
        flash(f'{updated_count}개 종목의 데이터가 업데이트되었습니다.', 'success')
    except Exception as e:
        logging.error(f"Error refreshing data: {e}")
        flash(f'데이터 새로고침에 실패했습니다: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/search_stock')
def search_stock():
    """종목명으로 종목 검색 API"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({
                'success': False,
                'error': '검색어를 입력해주세요.'
            })
        
        if len(query) < 2:
            return jsonify({
                'success': False,
                'error': '검색어는 2글자 이상 입력해주세요.'
            })
        
        # 종목 검색
        results = searcher.search_stock_by_name(query)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logging.error(f"Error searching stock: {e}")
        return jsonify({
            'success': False,
            'error': '검색 중 오류가 발생했습니다.'
        }), 500

@app.route('/api/popular_stocks')
def popular_stocks():
    """인기 종목 목록 API"""
    try:
        stocks = searcher.get_popular_stocks()
        return jsonify({
            'success': True,
            'stocks': stocks,
            'count': len(stocks)
        })
    except Exception as e:
        logging.error(f"Error getting popular stocks: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stock_status')
def stock_status():
    """AJAX용 주식 상태 API"""
    try:
        stocks = tracker.get_tracked_stocks()
        return jsonify({
            'success': True,
            'stocks': stocks,
            'count': len(stocks)
        })
    except Exception as e:
        logging.error(f"Error getting stock status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
