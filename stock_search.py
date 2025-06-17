import requests
import json
import logging
from typing import List, Dict, Optional
from urllib.parse import quote

class StockSearcher:
    """한국 주식 종목명으로 종목 코드 검색 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_by_name_naver(self, stock_name: str) -> List[Dict]:
        """네이버 금융을 통한 종목명 검색"""
        try:
            # 네이버 금융 검색 API
            url = "https://ac.finance.naver.com/ac"
            params = {
                'q': stock_name,
                'q_enc': 'UTF-8',
                'st': '111',
                'frm': 'stock',
                'r_format': 'json',
                'r_enc': 'UTF-8',
                'r_unicode': '0',
                't_korstock': '1',
                't_jstock': '0'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'items' in data and isinstance(data['items'], list):
                for item in data['items'][:10]:  # 상위 10개만
                    if isinstance(item, list) and len(item) >= 2:
                        name = item[0]
                        code = item[1]
                        
                        # 종목 코드가 6자리 숫자인지 확인
                        if len(code) == 6 and code.isdigit():
                            results.append({
                                'name': name,
                                'code': code,
                                'full_code': f"{code}.KS",
                                'market': 'KOSPI/KOSDAQ'
                            })
            
            return results
            
        except Exception as e:
            logging.error(f"네이버 검색 실패: {e}")
            return []
    
    def search_by_name_investing(self, stock_name: str) -> List[Dict]:
        """Investing.com을 통한 종목명 검색"""
        try:
            url = "https://api.investing.com/api/financialdata/search/"
            params = {
                'search-text': stock_name,
                'isCommonLangIncluded': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'data' in data:
                for item in data['data'][:5]:  # 상위 5개만
                    if 'symbol' in item and 'name' in item:
                        symbol = item['symbol']
                        name = item['name']
                        
                        # 한국 주식인지 확인 (KRX, KS 등)
                        if any(market in symbol for market in ['.KS', '.KQ']):
                            code = symbol.replace('.KS', '').replace('.KQ', '')
                            if len(code) == 6 and code.isdigit():
                                results.append({
                                    'name': name,
                                    'code': code,
                                    'full_code': symbol,
                                    'market': 'KOSPI/KOSDAQ'
                                })
            
            return results
            
        except Exception as e:
            logging.error(f"Investing.com 검색 실패: {e}")
            return []
    
    def search_stock_by_name(self, stock_name: str) -> List[Dict]:
        """종목명으로 종목 검색 (여러 소스 통합)"""
        if not stock_name or len(stock_name.strip()) < 2:
            return []
        
        stock_name = stock_name.strip()
        all_results = []
        
        # 네이버 금융 검색
        naver_results = self.search_by_name_naver(stock_name)
        all_results.extend(naver_results)
        
        # Investing.com 검색
        investing_results = self.search_by_name_investing(stock_name)
        all_results.extend(investing_results)
        
        # 중복 제거 (코드 기준)
        unique_results = {}
        for result in all_results:
            code = result['code']
            if code not in unique_results:
                unique_results[code] = result
        
        # 결과 정렬 (이름 일치도 기준)
        final_results = list(unique_results.values())
        final_results.sort(key=lambda x: self._calculate_similarity(stock_name, x['name']), reverse=True)
        
        return final_results[:10]  # 상위 10개만 반환
    
    def _calculate_similarity(self, query: str, target: str) -> float:
        """간단한 문자열 유사도 계산"""
        query = query.lower()
        target = target.lower()
        
        # 완전 일치
        if query == target:
            return 1.0
        
        # 포함 관계
        if query in target or target in query:
            return 0.8
        
        # 첫 글자 일치
        if query[0] == target[0]:
            return 0.3
        
        return 0.0
    
    def get_popular_stocks(self) -> List[Dict]:
        """인기 종목 목록 반환"""
        popular_stocks = [
            {'name': '삼성전자', 'code': '005930', 'full_code': '005930.KS'},
            {'name': 'SK하이닉스', 'code': '000660', 'full_code': '000660.KS'},
            {'name': 'NAVER', 'code': '035420', 'full_code': '035420.KS'},
            {'name': '카카오', 'code': '035720', 'full_code': '035720.KS'},
            {'name': 'LG에너지솔루션', 'code': '373220', 'full_code': '373220.KS'},
            {'name': '삼성바이오로직스', 'code': '207940', 'full_code': '207940.KS'},
            {'name': 'POSCO홀딩스', 'code': '005490', 'full_code': '005490.KS'},
            {'name': '현대차', 'code': '005380', 'full_code': '005380.KS'},
            {'name': 'LG화학', 'code': '051910', 'full_code': '051910.KS'},
            {'name': '삼성SDI', 'code': '006400', 'full_code': '006400.KS'}
        ]
        
        return popular_stocks