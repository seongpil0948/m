from stock.serializers.common.common import *
from rest_framework import serializers

__all__ = [
    'BolingerBandSerializer',
]

class BolingerBandSerializer(CodeSerializer, StartEndDate, WindowSizeSerializer):
  class Meta:
    ref_name = 'BolingerBandSerializer'
