from rest_framework import serializers

from stock.models.stock import Company, DailyPrice


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = '__all__'


class DailyPriceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DailyPrice
        fields = '__all__'
