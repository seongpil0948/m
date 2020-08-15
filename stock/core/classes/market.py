import pandas as pd
from django.db.models import Q
import datetime

from stock.models import Company, DailyPrice

__all__ = [
    'Market'    
]

def get_times(start_date=None, end_date=None):
    if start_date is None:
        start = str(datetime.date.today() - datetime.timedelta(days=365))
    elif type(start_date) == str: # 2020-02-01
        start = [int(i) for i in start_date.split('-')]
        start = datetime.datetime(start[0], start[1], start[2])
    

    if end_date is None:
        end = str(datetime.date.today())
    elif type(end_date) == str:
        end = [int(i) for i in end_date.split('-')]
        end = datetime.datetime(end[0], end[1], end[2])

    return start, end


class Market():
    def __init__(self, code=''):
        self.code = code
        self.codes = [i['code'] for i in Company.objects.all().values('code')]

    @property
    def get_corp_info(self):
        return Company.objects.get(pk=self.code).__dict__

    @property
    def all_corp_info(self):
        return {i.code: i for i in Company.objects.all()}


    @property
    def all_codes(self):
        self.codes = all_comp_codes()

    @property
    def get_daily_price(self, start_date=None, end_date=None):
        "모든 회사의 데이터를 가져옵니다"
        start, end = get_times(start_date=start_date, end_date=end_date)
        q = DailyPrice.objects.filter(
            Q(code=self.code) &
            Q(
                date__gte=start, 
                date__lte=end
            )
        ).order_by('-date')

        data = {}
        for i in q: 
            for col in list(i.__dict__.keys())[2:]: 
                if col not in data: 
                    data[col] = [] 
                data[col].append(i.__dict__[col])
        return pd.DataFrame(data=data)

    # @property
    # @NotImplemented
    # def get_all_price(self, start_date=None, end_date=None):
    #     start, end = get_times(start_date=start_date, end_date=end_date)
    #     q = DailyPrice.objects.filter(
    #         date__gte=start, 
    #         date__lte=end
    #     ).order_by('-date')
