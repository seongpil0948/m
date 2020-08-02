from session import RetrySession
import requests as req
from bs4 import BeautifulSoup as bs

session = RetrySession()
session['User-agent'] == 'james'
url = 'https://kr.investing.com/equities/south-korea'
soup = bs(session.get(url), 'html.parser')

table = soup.find('id', 'cross_rate_markets_stocks_1')
print(soup.prettify())