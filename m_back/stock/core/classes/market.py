import pandas as pd
from django.db.models import Q
import datetime

from stock.models import Company, DailyPrice

__all__ = [
    'Market'    
]

class Market():
    def __init__(self, code=0):
        self.code = code

    @property
    def get_comp_info(self):
        return Company.objects.get(pk=self.code).__dict__

    def get_daily_price(self, start_date=None, end_date=None):
        if start_date is None:
            start_date = str(datetime.date.today() - datetime.timedelta(days=365))
        start = [int(i) for i in start_date.split('-')]

        if end_date is None:
            end_date = str(datetime.date.today())
        end = [int(i) for i in end_date.split('-')]
        
        q = DailyPrice.objects.filter(
            Q(code=self.code) &
            Q(
                date__gte=datetime.datetime(start[0], start[1], start[2]), 
                date__lte=datetime.datetime(end[0], end[1], end[2])
            )
        ).order_by('-date')

        data = {}
        for i in q: 
            for col in list(i.__dict__.keys())[2:]: 
                if col not in data: 
                    data[col] = [] 
                data[col].append(i.__dict__[col])
        return pd.DataFrame(data=data)
