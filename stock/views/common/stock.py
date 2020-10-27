from django.shortcuts import render
from rest_framework import viewsets, filters
from stock.models.stock import Company, DailyPrice
from stock.serializers.common.stock import CompanySerializer, DailyPriceSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    # pagination_class = GeneralLimitOffsetPagination
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # filter_backends = (
    #     filters.SearchFilter,
    #     filters.OrderingFilter,
    # )
    # ordering_fields = '__all__'
    # search_fields = ['uuid']
    # ordering = ['updated_at', 'created_at', 'uuid']
    class Meta:
        model = Company
        fields = ['code', 'name_ko', 'name_en', 'industry_code']
        

class DailyPriceViewSet(viewsets.ModelViewSet):
    queryset = DailyPrice.objects.all()
    serializer_class = DailyPriceSerializer