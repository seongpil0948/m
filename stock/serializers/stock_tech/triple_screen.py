from stock.serializers.common.common import StartEndDate, Code

__all__ = [
    'TrippleScreenSerializer',
]

class TrippleScreenSerializer(StartEndDate, Code):
  class Meta:
    ref_name = 'TrippleScreenSerializer'

