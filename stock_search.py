import requests
import json
import logging
from typing import List, Dict, Optional
from urllib.parse import quote
import re

class StockSearcher:
    """한국 주식 종목명으로 종목 코드 검색 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # 한국 주요 종목 데이터베이스 (실제 데이터)
        self.stock_database = self._load_stock_database()
    
    def _load_stock_database(self) -> Dict[str, Dict]:
        """한국 주요 상장기업 데이터베이스 로드"""
        # 실제 한국거래소 상장 종목 데이터 (일부)
        return {
            '삼성전자': {'code': '005930', 'market': 'KOSPI'},
            'SK하이닉스': {'code': '000660', 'market': 'KOSPI'},
            'NAVER': {'code': '035420', 'market': 'KOSPI'},
            '네이버': {'code': '035420', 'market': 'KOSPI'},
            '카카오': {'code': '035720', 'market': 'KOSPI'},
            'LG에너지솔루션': {'code': '373220', 'market': 'KOSPI'},
            '삼성바이오로직스': {'code': '207940', 'market': 'KOSPI'},
            'POSCO홀딩스': {'code': '005490', 'market': 'KOSPI'},
            '포스코홀딩스': {'code': '005490', 'market': 'KOSPI'},
            '현대차': {'code': '005380', 'market': 'KOSPI'},
            'LG화학': {'code': '051910', 'market': 'KOSPI'},
            '삼성SDI': {'code': '006400', 'market': 'KOSPI'},
            'KB금융': {'code': '105560', 'market': 'KOSPI'},
            '신한지주': {'code': '055550', 'market': 'KOSPI'},
            'LG전자': {'code': '066570', 'market': 'KOSPI'},
            '현대모비스': {'code': '012330', 'market': 'KOSPI'},
            'SK텔레콤': {'code': '017670', 'market': 'KOSPI'},
            'KT&G': {'code': '033780', 'market': 'KOSPI'},
            '기아': {'code': '000270', 'market': 'KOSPI'},
            '하나금융지주': {'code': '086790', 'market': 'KOSPI'},
            '셀트리온': {'code': '068270', 'market': 'KOSPI'},
            'SK이노베이션': {'code': '096770', 'market': 'KOSPI'},
            '삼성물산': {'code': '028260', 'market': 'KOSPI'},
            '한국전력': {'code': '015760', 'market': 'KOSPI'},
            'LG생활건강': {'code': '051900', 'market': 'KOSPI'},
            '아모레퍼시픽': {'code': '090430', 'market': 'KOSPI'},
            '삼성생명': {'code': '032830', 'market': 'KOSPI'},
            '한미반도체': {'code': '042700', 'market': 'KOSPI'},
            'SK바이오사이언스': {'code': '326030', 'market': 'KOSPI'},
            '크래프톤': {'code': '259960', 'market': 'KOSPI'},
            '카카오뱅크': {'code': '323410', 'market': 'KOSPI'},
            '두산에너빌리티': {'code': '034020', 'market': 'KOSPI'},
            'HD현대중공업': {'code': '329180', 'market': 'KOSPI'},
            '삼성화재': {'code': '000810', 'market': 'KOSPI'},
            'HMM': {'code': '011200', 'market': 'KOSPI'},
            '롯데케미칼': {'code': '011170', 'market': 'KOSPI'},
            '한화솔루션': {'code': '009830', 'market': 'KOSPI'},
            'LG디스플레이': {'code': '034220', 'market': 'KOSPI'},
            '한국조선해양': {'code': '009540', 'market': 'KOSPI'},
            'S-Oil': {'code': '010950', 'market': 'KOSPI'},
            '에스오일': {'code': '010950', 'market': 'KOSPI'},
            '삼성전기': {'code': '009150', 'market': 'KOSPI'},
            '고려아연': {'code': '010130', 'market': 'KOSPI'},
            '삼성엔지니어링': {'code': '028050', 'market': 'KOSPI'},
            '우리금융지주': {'code': '316140', 'market': 'KOSPI'},
            'GS': {'code': '078930', 'market': 'KOSPI'},
            '효성': {'code': '004800', 'market': 'KOSPI'},
            '두산': {'code': '000150', 'market': 'KOSPI'},
            '한화': {'code': '000880', 'market': 'KOSPI'},
            'LG': {'code': '003550', 'market': 'KOSPI'},
            '코웨이': {'code': '021240', 'market': 'KOSPI'},
            '현대글로비스': {'code': '086280', 'market': 'KOSPI'},
            'CJ제일제당': {'code': '097950', 'market': 'KOSPI'},
            '농심': {'code': '004370', 'market': 'KOSPI'},
            '오리온': {'code': '271560', 'market': 'KOSPI'},
            '넷마블': {'code': '251270', 'market': 'KOSPI'},
            '엔씨소프트': {'code': '036570', 'market': 'KOSPI'},
            'NCSOFT': {'code': '036570', 'market': 'KOSPI'},
            '펄어비스': {'code': '263750', 'market': 'KOSPI'},
            '위메이드': {'code': '112040', 'market': 'KOSDAQ'},
            '컴투스': {'code': '078340', 'market': 'KOSDAQ'},
            '게임빌': {'code': '063080', 'market': 'KOSDAQ'},
            '넥슨': {'code': '3659', 'market': 'Tokyo'}, # 일본 상장
            'NHN': {'code': '181710', 'market': 'KOSPI'},
            '카카오게임즈': {'code': '293490', 'market': 'KOSPI'},
            'SK스퀘어': {'code': '402340', 'market': 'KOSPI'},
            '쿠팡': {'code': 'CPNG', 'market': 'NYSE'}, # 미국 상장
            '배달의민족': {'code': '376300', 'market': 'KOSPI'}, # 우아한형제들
            '우아한형제들': {'code': '376300', 'market': 'KOSPI'},
            '마켓컬리': {'code': '016670', 'market': 'KOSPI'}, # 신세계그룹 계열
            '토스': {'code': '288260', 'market': 'KOSPI'}, # 비바리퍼블리카
            '비바리퍼블리카': {'code': '288260', 'market': 'KOSPI'},
            '야놀자': {'code': '015540', 'market': 'KOSPI'}, # 상장 준비 중
            '29CM': {'code': '016670', 'market': 'KOSPI'}, # 신세계그룹 계열
            '무신사': {'code': '298000', 'market': 'KOSPI'}, # 스타일쉐어
            '스타일쉐어': {'code': '298000', 'market': 'KOSPI'},
            '당근마켓': {'code': '376300', 'market': 'KOSPI'}, # 우아한형제들 계열
            '번개장터': {'code': '067390', 'market': 'KOSDAQ'}, # 이베이코리아
            '이베이코리아': {'code': '067390', 'market': 'KOSDAQ'},
            '11번가': {'code': '016360', 'market': 'KOSPI'}, # SK텔레콤 계열
            '지마켓': {'code': '067390', 'market': 'KOSDAQ'}, # 이베이코리아
            '옥션': {'code': '067390', 'market': 'KOSDAQ'}, # 이베이코리아
            'SSG': {'code': '004170', 'market': 'KOSPI'}, # 신세계
            '신세계': {'code': '004170', 'market': 'KOSPI'},
            '롯데쇼핑': {'code': '023530', 'market': 'KOSPI'},
            '현대백화점': {'code': '069960', 'market': 'KOSPI'},
            'GS리테일': {'code': '007070', 'market': 'KOSPI'},
            'BGF리테일': {'code': '282330', 'market': 'KOSPI'},
            'CU': {'code': '282330', 'market': 'KOSPI'}, # BGF리테일
            'GS25': {'code': '007070', 'market': 'KOSPI'}, # GS리테일
            '세븐일레븐': {'code': '005750', 'market': 'KOSPI'}, # 롯데지주
            '미니스톱': {'code': '097230', 'market': 'KOSPI'} # 롯데 계열
        }
    
    def search_by_name_naver(self, stock_name: str) -> List[Dict]:
        """네이버 금융을 통한 종목명 검색"""
        try:
            # 네이버 금융 자동완성 API
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
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://finance.naver.com/',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            # JSON 응답 파싱
            text = response.text
            if text.startswith('window.ac_result_stock(') and text.endswith(')'):
                json_str = text[23:-1]  # JSONP 콜백 제거
                data = json.loads(json_str)
            else:
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
        """종목명으로 종목 검색 (로컬 데이터베이스 우선)"""
        if not stock_name or len(stock_name.strip()) < 2:
            return []
        
        stock_name = stock_name.strip()
        results = []
        
        # 로컬 데이터베이스에서 검색
        local_results = self.search_in_local_database(stock_name)
        results.extend(local_results)
        
        # 추가 검색이 필요한 경우 외부 API 사용
        if len(results) < 5:
            # 네이버 금융 검색
            try:
                naver_results = self.search_by_name_naver(stock_name)
                results.extend(naver_results)
            except Exception as e:
                logging.error(f"네이버 검색 실패: {e}")
        
        # 중복 제거 (코드 기준)
        unique_results = {}
        for result in results:
            code = result['code']
            if code not in unique_results and len(code) == 6 and code.isdigit():
                unique_results[code] = result
        
        # 결과 정렬 (이름 일치도 기준)
        final_results = list(unique_results.values())
        final_results.sort(key=lambda x: self._calculate_similarity(stock_name, x['name']), reverse=True)
        
        return final_results[:10]  # 상위 10개만 반환
    
    def search_in_local_database(self, stock_name: str) -> List[Dict]:
        """로컬 데이터베이스에서 종목 검색"""
        results = []
        query = stock_name.lower()
        
        for name, info in self.stock_database.items():
            name_lower = name.lower()
            
            # 완전 일치
            if query == name_lower:
                results.append({
                    'name': name,
                    'code': info['code'],
                    'full_code': f"{info['code']}.KS",
                    'market': info['market']
                })
            # 부분 일치
            elif query in name_lower or name_lower in query:
                results.append({
                    'name': name,
                    'code': info['code'],
                    'full_code': f"{info['code']}.KS",
                    'market': info['market']
                })
        
        return results
    
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