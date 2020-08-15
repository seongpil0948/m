import pandas as pd
from django.db.models import Max

from stock.core.classes.market import get_times, Market
from stock.models import Company, DailyPrice
 
__all__ = [
    'DualMomentum'    
]

class DualMomentum(Market):
    def __init__(self, start_date=None, end_date=None, stock_count=10):
        super().__init__() # for codes
        self.corpers = super().all_corp_info
        self.start_date, self.end_date = get_times(start_date=start_date, end_date=end_date)
        self.stock_count = stock_count

    @property
    def rltv_momentum(self):
        """특정 기간 동안 수익률이 제일 높았던 stock_count 개의 종목들 (상대 모멘텀)
            - start_date  : 상대 모멘텀을 구할 시작일자 ('2020-01-01')   
            - end_date    : 상대 모멘텀을 구할 종료일자 ('2020-12-31')
            - stock_count : 상대 모멘텀을 구할 종목수
        """       
        
        # KRX 종목별 수익률을 구해서 2차원 리스트 형태로 추가
        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']        
        for i in self.codes:
            # .aggregate(close_price=Max('close_price'))
            old_query = DailyPrice.objects.filter(code=i, date=self.start_date)
            new_query = DailyPrice.objects.filter(code=i, date=self.end_date)
            if len(new_query) == 0 or len(old_query) == 0:
                continue
            old_price = int(old_query[0].close_price)
            new_price = int(new_query[0].close_price)

            returns = (new_price / old_price - 1) * 100
            rows.append([i, self.corpers[i].name_ko, 
                old_price, new_price, returns])

        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        df = df.head(self.stock_count)
        df.index = pd.Index(range(self.stock_count))
        print(df)
        print(f"\nRelative momentum ({self.start_date} ~ {self.end_date}) : "\
            f"{df['returns'].mean():.2f}% \n")
        return df

    @property
    def abs_momentum(self):
        """특정 기간 동안 상대 모멘텀에 투자했을 때의 평균 수익률 (절대 모멘텀)
            - rltv_momentum : get_rltv_momentum() 함수의 리턴값 (상대 모멘텀)
            - start_date    : 절대 모멘텀을 구할 매수일 ('2020-01-01')   
            - end_date      : 절대 모멘텀을 구할 매도일 ('2020-12-31')
        """
        rl_df = self.rltv_momentum
        codes = rl_df['code']
        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']

        for i in codes:
            old_query = DailyPrice.objects.filter(code=i, date=self.start_date)
            new_query = DailyPrice.objects.filter(code=i, date=self.end_date)
            if len(new_query) == 0 or len(old_query) == 0:
                continue

            old_price = int(old_query[0].close_price)
            new_price = int(new_query[0].close_price)

            returns = (new_price / old_price - 1) * 100
            rows.append([i, self.corpers[i].name_ko, 
                old_price, new_price, returns])


        # 절대 모멘텀 데이터프레임을 생성한 후 수익률순으로 출력
        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        print(df)
        print(f"\nAbasolute momentum ({self.start_date} ~ {self.end_date}) : "\
            f"{df['returns'].mean():.2f}%")
        return
