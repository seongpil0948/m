import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from stock.core.data import Market
from stock.models import Company, get_all_corper
from stock.utils.s3 import plt_upload_wrap

"""
efficient_frontier and sharpe PortFolio = 효율적 투자선과 샤프지수 포폴
252 = 미국 평균 개장일

자산가격의 정규 분포에서 예상 수익률은 평균값인 u, 표준편차(sqrt(분산(분산각편차 제곱후 더하여 평균)))는 시그마 
"""

__all__ = [
    'efficient_portfolio'
]

def efficient_portfolio():
    codes = get_all_corper()
    datas = {}
    for c in codes:
        df = Market(code=c).df
        if df is not None:
            datas[c] = df['close_price']
    dfs = pd.DataFrame(data=datas)
    codes = dfs.keys().to_list()
    daily_ret = dfs.pct_change() # percent_change 일간 수익률
    annual_ret = daily_ret.mean() * 252 

    daily_cov = daily_ret.cov() # 공분산
    annual_cov = daily_cov * 252

    port_ret = [] 
    port_risk = [] 
    port_weights = []
    sharpe_ratio = [] 

    """
    1. monte carlo simulation for approximation

    2.  Sharpe 지수
        위험 단위당 수익률을 계산 한다는 점에서 수익률의 표준편차와 다르다
        risk 에 비해 수익률이 얼마나 높은지

    3.  columns = returns , risk, Sharpe, stock1, stock2 ...
        포트폴리오 20000개가 각기다른 리스크와 예상 수익률을 가진다

    4.  점들 분포의 좌측의 곡선이 최적 투자 곡선이다
    5.  샤프 지수에 따라 컬러맵 과 테두리  설정
    6.  샤프지수가 가장 큰 포폴을 붉은 별표 표시
    7.  리스크가 가장 작은 표시

    선택된 기간동안 risk% 의 변동률을 겪으며 returns% 의 수익을 안긴다 
    """
    for _ in range(20000): # 1
        weights = np.random.random(len(codes)) # random number length equeal to stocks
        weights /= np.sum(weights) # norm or array to add to zero

        # 랜덤하게 생성된 종목별 비중(weight) 배열과 종목별 연간 수익률을 곱한다
        returns = np.dot(weights, annual_ret) 
        risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights))) 

        port_ret.append(returns) 
        port_risk.append(risk) 
        port_weights.append(weights)
        sharpe_ratio.append(returns/risk) # 2

    portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}
    for i, c in enumerate(codes): 
        portfolio[c] = [weight[i] for weight in port_weights] 
    df = pd.DataFrame(portfolio) 
    df = df[['Returns', 'Risk', 'Sharpe'] + [c for c in codes]] # 3.

    max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]
    min_risk = df.loc[df['Risk'] == df['Risk'].min()]

    df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis', # 4
        edgecolors='k', figsize=(11,7), grid=True)  # 5.
    plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r', 
        marker='*', s=300) # 6
    plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r', 
        marker='X', s=200) # 7
    plt.title('Portfolio Optimization') 
    plt.xlabel('Risk') 
    plt.ylabel('Expected Returns')

    path = plt_upload_wrap(plt=plt, tech_name=efficient_portfolio.__name__)
    return path
