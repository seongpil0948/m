from rest_framework import viewsets, filters
from stock.models.stock import Company, DailyPrice
from stock.serializers.common.stock import CompanySerializer, DailyPriceSerializer


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    class Meta:
        model = Company
        fields = ['code', 'name_ko', 'name_en', 'industry_code']
        

class DailyPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyPrice.objects.all()
    serializer_class = DailyPriceSerializer

    class Meta:
        model = DailyPrice
        fields = '__all__'
