from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import requests
import traceback
from django.db import IntegrityError

from stock.models import Company, DailyPrice


# #TODO(창석): Company Model ko_name, en_name 채워주는 함수 필요
def get_naver_rank():
    """
    네이버 금융 랭킹 30위 정보를 가져오는 함수
    """
    url = "https://finance.naver.com/sise/lastsearch2.nhn"
    table = pd.read_html(url, encoding='euc-kr')

    name = table[1][['종목명']].dropna(how="all")
    lst_names = name.values.tolist()

    rank_name = sum(lst_names, [])
    print(f"네이버 랭킹 갯 수: {len(rank_name)}")

    return rank_name


def get_krx(names):
    """
    한국 거래소에 등록 된 종목코드 정보를 가져와 네이버 금융 랭킹과 매핑하는 함수
    """
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

    # 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column 들은 제외해준다.
    code_df = code_df[['회사명', '종목코드']]

    # 한글로된 컬럼명을 영어로 바꿔준다.
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    # 인기순위에서 뽑은 종목명과 한국거래소에서 가져온 종목코드를 매핑
    company_name_code = code_df[code_df['name'].isin(names)]
    company_ko_name = sum(company_name_code[['name']].values.tolist(), [])
    company_code = sum(company_name_code[['code']].values.tolist(), [])
    for ko_name, code in zip(company_ko_name, company_code):
        try:
            Company.objects.get_or_create(
                name_ko=ko_name,
                code=code
            )
        except IntegrityError:
            print(f"tmp 이미 존재하는 종목코드 입니다 -> {code}")
    print(f"네이버 주식랭킹과 한국거래소 종목코드와 매핑 된 갯 수: {len(company_name_code)}")

    return company_name_code


def parse_page(code, page):
    """
    종목코드와 페이지를 입력하면 해당 페이지의 테이블을 크롤링하는 함수
    """
    try:
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.format(code=code, page=page)
        res = requests.get(url)
        _soap = BeautifulSoup(res.text, 'lxml')
        _df = pd.read_html(str(_soap.find("table")), header=0)[0]
        _df = _df.dropna()
        return _df
    except Exception as e:
        traceback.print_exc()
    return None


# def get_naver_finance(code):
#     """
#     메인 로직
#     yfinance 에 없는 종목코드를 입력하여 네이버 금융에서 데이터를 크롤링하는 함수
#     TODO(창석): 여러번 요청 시 Naver 에서 막음 해결 필요
#     """
#     print(f"start {code}")
#     url = f"https://finance.naver.com/item/sise_day.nhn?code={code}"
#     res = requests.get(url)
#     res.encoding = 'utf-8'
#
#     if res.status_code == 200:
#         soap = BeautifulSoup(res.text, 'lxml')
#         el_table_navi = soap.find("table", class_="Nnavi")
#         el_td_last = el_table_navi.find("td", class_="pgRR")
#         # 마지막 페이지를 가져옵니다.
#         pg_last = el_td_last.a.get('href').rsplit('&')[1]
#         pg_last = pg_last.split('=')[1]
#         pg_last = int(pg_last)
#
#         df = None
#         for page in range(1, pg_last+1):
#             _df = parse_page(code, page)
#             # 페이지 별로 돌면서 입력한 날짜보다 큰 날짜들만 크롤링해옵니다.
#             _df_filtered = _df[_df['날짜'] > start.strftime('%Y.%m.%d')]
#             print(_df_filtered)
#             if df is None:
#                 df = _df_filtered
#             else:
#                 df = pd.concat([df, _df_filtered])
#             if len(_df) > len(_df_filtered):
#                 print(df)
#                 print("end")
#                 break
#     else:
#         raise print("TMP: Naver finance 일별 데이터를 가져오는데 실패하였습니다.")

# init
rank_names = get_naver_rank()  # Naver Top 30 Company
name_codes = get_krx(rank_names)  # Naver to krx mapping

code_list = sum(name_codes[['code']].values.tolist(), [])  # mapped Company Code

pk = DailyPrice.objects.last().pk
success_list = []
fail_list = []
results = {}

for code in code_list:
    print(f'===== start code -> {code} =====')
    try:
        company = Company.objects.get(code=code)
    except Company.DoesNotExist:
        raise print('tmp Company 테이블에 존재하지 않은 종목코드 입니다.')

    try:
        latest_obj_date = DailyPrice.objects.filter(code=code).last().date
    except AttributeError:
        start = None
        print('tmp Company 는 생성되어있지만 DailyPrice 값이 채워져있지 않습니다.')
    else:
        target = datetime.strptime(latest_obj_date, '%Y-%m-%d')
        start = target + timedelta(days=1)

    try:
        results[code] = pdr.get_data_yahoo(f"{code}.KS", start)
    except Exception as e:
        print(f'Yahoo 에서 {code} 를 뽑는데 오류가 발생')  # TODO(창석) 여기 리스트들을 뽑아서 Naver 에서 크롤링
        fail_list.append(code)
    else:
        print('예외를 통과 Database 에 생성')
        for idx, row in enumerate(results[code].iterrows()):
            pk += 1
            row = row[1]
            date = results[code].index[idx]
            DailyPrice.objects.create(
                pk=pk,
                code=company,
                date=date.strftime("%Y-%m-%d"),
                volume=row['Volume'],
                open_price=row['Open'],
                high_price=row['High'],
                low_price=row['Low'],
                close_price=row['Close']
            )
            success_list.append(code)
        print(f"{code} Complete")

print('===== yahoo 에 있는 데이터 리스트 =====')
success_list = np.unique(success_list).tolist()
print(success_list)
print('===== yahoo 에 없는 데이터 리스트 =====')
print(fail_list)

# #TODO(창석): yahoo 에 없는 데이터 크롤링
# get_naver_finance(code=118990)
