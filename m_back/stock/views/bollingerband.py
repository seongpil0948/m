import matplotlib.pyplot as plt

from stock.core.classes import Market
from stock.models import Company, get_all_corper
"""
매수: %b > 0.8 and MFI > 80
매도: %b < 0.2 and MFI > 20

볼린저 밴드는 다음과 같이 구성된다.
    1. N기간 동안의 이동평균(MA)
    2. 이동평균 위의 K배 표준편차 상위 밴드
    3. 이동평균 아래의 K배 표준편차 하위 밴드
    4. 일반적으로 N과 K의 값은 20과 2이다. 평균값의 기본 선택의 단순 이동 평균이지만,
        필요에 따라 다른 종류의 평균값을 쓸 수 있다.
        지수 이동 평균(Exponential moving averages)은 일반적인 대안이다.
        대개 중간 밴드와 표준 편차의 계산을 위해 같은 기간을 사용한다.

1. percentB = 주가가 상단 밴드에 위치시 1.0, 중간 0.5, 하단 0 
2. 밴드사이의 폭을 의미 = 스퀴즈 확인 = 변동성이 극히 낮아지며 곧이어 확 높아지는 변동성을 예상
    추세의 시작과 마지막을 포착 하며 강한 상승세 일경우 하단 볼린저 밴드가 확 낮아진다
    u - 2std 를 감안 해보면 당연하다. 

"""
codes = get_all_corper()
df = Market(code=codes[0]).get_daily_price
df['MA5'] = df['close_price'].rolling(window=5).mean() # mean avg
df['stddev'] = df['close_price'].rolling(window=5).std()
df['upper'] = df['MA5'] + (df['stddev'] * 2)
df['lower'] = df['MA5'] - (df['stddev'] * 2)
df['PB'] = (df['close_price'] - df['lower']) / (df['upper'] - df['lower']) # 1
df['bandwidth'] = (df['upper'] - df['lower']) / df['MA5'] * 100 # 2
df = df[5:]

plt.figure(figsize=(9, 5)) 
plt.plot(df.index, df['close_price'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label = 'Upper band')      
plt.plot(df.index, df['MA5'], 'k--', label='Moving average 5') 
plt.plot(df.index, df['lower'], 'c--', label = 'Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
plt.legend(loc='best') 
plt.title('Bollinger Band (5 day, 2 std)') 

plt.subplot(2, 1, 1)
plt.plot(df.index, df['bandwidth'], color='m', label='BandWidth')
plt.grid(True)
plt.legend(loc='best')

plt.subplot(2, 1, 2)  # ③
plt.plot(df.index, df['PB'], color='b', label='%B')
plt.grid(True)
plt.legend(loc='best')

plt.show()     