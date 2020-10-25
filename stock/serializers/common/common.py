from rest_framework import serializers

__all__ = [
  'StartEndDate',
  'Code',
  'WindowSize'
]

class StartEndDate(serializers.Serializer):
  start_date = serializers.CharField(
    max_length=50
  )
  end_date = serializers.CharField(
    max_length=50
  )

class Code(serializers.Serializer):
  code = serializers.CharField(max_length=10)

class WindowSize(serializers.Serializer):
  window_size = serializers.IntegerField()