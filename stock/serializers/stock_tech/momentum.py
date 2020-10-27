from stock.serializers.common.common import StartEndDate
from rest_framework import serializers

__all__ = [
    'DualMomentumSerializer',
]

class DualMomentumSerializer(StartEndDate):
    stock_count = serializers.IntegerField()
    def validate(self, attrs):
        return super().validate(attrs)
