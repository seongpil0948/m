from stock.serializers.common.common import StartEndDate, CodeSerializer

__all__ = [
    'TrippleScreenSerializer',
]

class TrippleScreenSerializer(StartEndDate, CodeSerializer):
  class Meta:
    ref_name = 'TrippleScreenSerializer'

