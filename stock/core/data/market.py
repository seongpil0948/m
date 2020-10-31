import pandas as pd
from django.db.models import Q
import datetime

from stock.models import Company, DailyPrice


def get_times(start_date=None, end_date=None, return_type=str):
    if start_date is None:
        start = str(datetime.date.today() - datetime.timedelta(days=730))
    elif type(start_date) == str: # 2020-02-01
        start = [int(i) for i in start_date.split('-')]
        if return_type == str:
            start = str(datetime.datetime(start[0], start[1], start[2])).split(' ')[0]
        elif return_type == 'datetime':
            start = datetime.datetime(start[0], start[1], start[2])
        
    if end_date is None:
        end = str(datetime.date.today() - datetime.timedelta(days=365))
    elif type(end_date) == str:
        end = [int(i) for i in end_date.split('-')]
        if return_type == str:
            end = str(datetime.datetime(end[0], end[1], end[2])).split(' ')[0]
        elif return_type == 'datetime':
            end = datetime.datetime(end[0], end[1], end[2])
    return start, end


def get_recently_price(code="100220"):
    query = DailyPrice.objects.filter(code_id=code).order_by('date').last()
    return query.date, query.close_price

# from stock.core.data.market import Market 
class Market():
    def __init__(self, start_date=None, end_date=None, code='285130'):
        if start_date is None or end_date is None:
            query = DailyPrice.objects.filter(code_id=code).order_by('date')
            if query.first() is None:
                raise ValueError(f"유효하지 않은 코드: {code}.")
            if start_date is None:
                start_date = query.first().date
            if end_date:
                end_date = query.last().date

        self.code = code
        self.start, self.end = get_times(start_date=start_date, end_date=end_date)
        self.df = self.get_daily_price # basic df

    def add_rolling(self, window_size=10):
        add_colums = ['MMax', 'MAvg', 'MMin', 'STD']
        roll = self.df['close_price'].rolling(window=window_size)
        self.df['MMax'] =  roll.max()
        self.df['MAvg'] =  roll.mean()                       
        self.df['MMin'] =  roll.min()
        self.df['STD'] = roll.std()
        for col in add_colums:
            self.df[col] = self.df[col].fillna(method='bfill')

    @property
    def get_corp_info(self):
        return Company.objects.get(pk=self.code).__dict__

    @property
    def all_corp_info(self):
        return {i.code: i for i in Company.objects.all()}
    @property
    def get_all_corper_codes(self):
        return [i[0] for i in Company.objects.values_list('code')]      

    @property
    def get_daily_price(self):
        "단일 회사의 데이터를 가져옵니다"
        q = DailyPrice.objects.filter(
            Q(code=self.code) &
            Q(
                date__gte=self.start, 
                date__lte=self.end
            )
        ).order_by('-date')

        data = {}
        for i in q: 
            for col in list(i.__dict__.keys())[2:]: 
                if col not in data: 
                    data[col] = [] 
                data[col].append(i.__dict__[col])

        df = pd.DataFrame(data=data)
        if df.shape[0] > 1:
            df = df.set_index('date', drop=True)
            return df.drop(['code_id'], axis='columns')
    
    @property
    def close_prices(self):
        return self.get_daily_price['close_price'].to_list()
