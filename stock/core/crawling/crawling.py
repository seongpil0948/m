from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_datareader as pdr
import pprint
import requests


#TODO(창석): KOSPI TOP 100 을 뽑는데 yfinance 에 있으면 거기서 가져오고, 없으면 크롤링해서 DB 저장

# finance naver 인기순위
url = "https://finance.naver.com/sise/lastsearch2.nhn"
table = pd.read_html(url, encoding='euc-kr')

# TODO(창석): [현재] 인기검색 종목명을 가져와 corper_list 에서 종목코드를 Get
# TODO(창석): [변경] 코드명을 제공하는 곳에서 코드명을 가져와 pandas_datareader 에서 데이터를 Get
corp_lists = pd.read_csv('../data/corper_list.csv')
target_codes = corp_lists['종목코드'].values.tolist()
target_names = corp_lists['기업명'].values.tolist()

# delete NaN value
name = table[1][['종목명']].dropna(how="all")
lst_names = name.values.tolist()

# 2차원 리스트를 1차원으로 변경
company_name_list = sum(lst_names, [])
