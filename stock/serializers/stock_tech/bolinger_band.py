from stock.serializers.common.common import *
from rest_framework import serializers

__all__ = [
    'BolingerBandSerializer',
]

class BolingerBandSerializer(Code, StartEndDate, WindowSize):
  class Meta:
    ref_name = 'BolingerBandSerializer'
