import json
import os
import yfinance as yf
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class StockTracker:
    """한국 주식 추적 및 고점 대비 하락률 계산 클래스"""
    
    def __init__(self, data_file: str = "data/stocks.json"):
        self.data_file = data_file
        self.ensure_data_directory()
        self.stocks = self.load_stocks()
    
    def ensure_data_directory(self):
        """데이터 디렉토리 생성"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def load_stocks(self) -> Dict:
        """저장된 주식 데이터 로드"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Error loading stocks data: {e}")
            return {}
    
    def save_stocks(self):
        """주식 데이터 저장"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.stocks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Error saving stocks data: {e}")
    
    def add_stock(self, stock_code: str, stock_name: str) -> bool:
        """새로운 추적 종목 추가 (한국 및 해외 주식 지원)"""
        try:
            # 이미 존재하는 종목인지 확인
            if stock_code in self.stocks:
                return False
            
            # 해외 주식인지 확인하여 적절한 접미사 추가
            formatted_code = self._format_stock_code(stock_code)
            
            # yfinance로 종목 유효성 검증
            stock = yf.Ticker(formatted_code)
            info = stock.info
            
            if not info or 'regularMarketPrice' not in info:
                # 기본 정보를 가져올 수 없는 경우, 히스토리 데이터로 확인
                hist = stock.history(period="5d")
                if hist.empty:
                    return False
            
            # 종목 추가
            self.stocks[formatted_code] = {
                'name': stock_name,
                'code': formatted_code,
                'original_code': stock_code,
                'added_date': datetime.now().isoformat(),
                'last_updated': None,
                'current_price': None,
                'recent_high': None,
                'recent_high_date': None,
                'decline_rate': None,
                'error_message': None,
                'market_type': self._get_market_type(formatted_code)
            }
            
            # 초기 데이터 업데이트
            self.update_stock_data(formatted_code)
            self.save_stocks()
            return True
            
        except Exception as e:
            logging.error(f"Error adding stock {stock_code}: {e}")
            return False
    
    def _format_stock_code(self, code: str) -> str:
        """주식 코드를 yfinance 형식으로 포맷"""
        # 이미 접미사가 있는 경우 그대로 사용
        if '.' in code or len(code) <= 4:
            return code
        
        # 6자리 숫자인 경우 한국 주식으로 간주
        if len(code) == 6 and code.isdigit():
            return f"{code}.KS"
        
        return code
    
    def _get_market_type(self, code: str) -> str:
        """주식 코드로부터 시장 유형 판단"""
        if code.endswith('.KS'):
            return 'KRX'
        elif code.endswith('.T'):
            return 'TSE'
        elif any(char.isalpha() for char in code) and not '.' in code:
            return 'US'
        else:
            return 'OTHER'
    
    def remove_stock(self, stock_code: str) -> bool:
        """추적 종목 제거"""
        try:
            if stock_code in self.stocks:
                del self.stocks[stock_code]
                self.save_stocks()
                return True
            return False
        except Exception as e:
            logging.error(f"Error removing stock {stock_code}: {e}")
            return False
    
    def calculate_recent_high_decline(self, stock_code: str) -> Tuple[Optional[float], Optional[float], Optional[str], Optional[float]]:
        """직전 고점 대비 하락률 계산"""
        try:
            stock = yf.Ticker(stock_code)
            
            # 최근 3개월 데이터 가져오기
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            hist = stock.history(start=start_date, end=end_date)
            
            if hist.empty:
                return None, None, None, None
            
            # 현재 가격 (최신 종가)
            current_price = float(hist['Close'].iloc[-1])
            
            # 최근 고점 찾기 (최근 3개월 중 최고가)
            recent_high = float(hist['High'].max())
            recent_high_date_idx = hist['High'].idxmax()
            recent_high_date = str(recent_high_date_idx.date())
            
            # 하락률 계산
            decline_rate = ((recent_high - current_price) / recent_high) * 100
            
            return current_price, recent_high, recent_high_date, decline_rate
            
        except Exception as e:
            logging.error(f"Error calculating decline for {stock_code}: {e}")
            return None, None, None, None
    
    def update_stock_data(self, stock_code: str):
        """특정 종목의 데이터 업데이트"""
        try:
            if stock_code not in self.stocks:
                return
            
            current_price, recent_high, recent_high_date, decline_rate = self.calculate_recent_high_decline(stock_code)
            
            self.stocks[stock_code].update({
                'last_updated': datetime.now().isoformat(),
                'current_price': current_price,
                'recent_high': recent_high,
                'recent_high_date': recent_high_date,
                'decline_rate': decline_rate,
                'error_message': None
            })
            
        except Exception as e:
            logging.error(f"Error updating stock data for {stock_code}: {e}")
            self.stocks[stock_code]['error_message'] = str(e)
            self.stocks[stock_code]['last_updated'] = datetime.now().isoformat()
    
    def refresh_all_stocks(self) -> int:
        """모든 추적 종목 데이터 새로고침"""
        updated_count = 0
        for stock_code in self.stocks.keys():
            try:
                self.update_stock_data(stock_code)
                updated_count += 1
            except Exception as e:
                logging.error(f"Error refreshing {stock_code}: {e}")
        
        self.save_stocks()
        return updated_count
    
    def get_tracked_stocks(self) -> List[Dict]:
        """추적 중인 모든 종목 정보 반환"""
        stocks_list = []
        
        for stock_code, data in self.stocks.items():
            stock_info = {
                'code': stock_code,
                'name': data.get('name', ''),
                'current_price': data.get('current_price'),
                'recent_high': data.get('recent_high'),
                'recent_high_date': data.get('recent_high_date'),
                'decline_rate': data.get('decline_rate'),
                'last_updated': data.get('last_updated'),
                'error_message': data.get('error_message'),
                'status': 'error' if data.get('error_message') else 'success',
                'market_type': data.get('market_type', 'KRX'),
                'original_code': data.get('original_code', stock_code)
            }
            
            # 시장 타입에 따른 가격 포맷팅
            market_type = stock_info['market_type']
            currency_symbol = self._get_currency_symbol(market_type)
            
            # 가격 포맷팅
            if stock_info['current_price']:
                if market_type == 'KRX':
                    stock_info['current_price_formatted'] = f"{stock_info['current_price']:,.0f}원"
                else:
                    stock_info['current_price_formatted'] = f"{currency_symbol}{stock_info['current_price']:,.2f}"
            
            if stock_info['recent_high']:
                if market_type == 'KRX':
                    stock_info['recent_high_formatted'] = f"{stock_info['recent_high']:,.0f}원"
                else:
                    stock_info['recent_high_formatted'] = f"{currency_symbol}{stock_info['recent_high']:,.2f}"
            
            # 하락률 포맷팅
            if stock_info['decline_rate'] is not None:
                stock_info['decline_rate_formatted'] = f"{stock_info['decline_rate']:.2f}%"
                
                # 하락률에 따른 상태 분류
                if stock_info['decline_rate'] < 5:
                    stock_info['decline_status'] = 'low'
                elif stock_info['decline_rate'] < 15:
                    stock_info['decline_status'] = 'medium'
                else:
                    stock_info['decline_status'] = 'high'
            
            # 업데이트 시간 포맷팅
            if stock_info['last_updated']:
                try:
                    updated_dt = datetime.fromisoformat(stock_info['last_updated'])
                    stock_info['last_updated_formatted'] = updated_dt.strftime('%Y-%m-%d %H:%M')
                except:
                    stock_info['last_updated_formatted'] = stock_info['last_updated']
            
            # 시장 표시명 추가
            stock_info['market_display'] = self._get_market_display_name(market_type)
            
            stocks_list.append(stock_info)
        
        # 하락률 순으로 정렬 (높은 하락률부터)
        stocks_list.sort(key=lambda x: x.get('decline_rate', 0), reverse=True)
        
        return stocks_list
    
    def _get_currency_symbol(self, market_type: str) -> str:
        """시장 타입에 따른 통화 기호 반환"""
        if market_type == 'KRX':
            return '₩'
        elif market_type == 'TSE':
            return '¥'
        elif market_type == 'US':
            return '$'
        else:
            return '$'
    
    def _get_market_display_name(self, market_type: str) -> str:
        """시장 타입에 따른 표시명 반환"""
        market_names = {
            'KRX': '한국',
            'TSE': '일본',
            'US': '미국',
            'OTHER': '기타'
        }
        return market_names.get(market_type, '기타')
