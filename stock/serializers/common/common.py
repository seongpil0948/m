from rest_framework import serializers

__all__ = [
  'StartEndDate',
  'CodeSerializer',
  'WindowSizeSerializer',
  'StartEndCodeWindowSerializer',
  'StartEndCodeSerializer'
]

class StartEndDate(serializers.Serializer):
  start_date = serializers.CharField(
    max_length=50
  )
  end_date = serializers.CharField(
    max_length=50
  )


class CodeSerializer(serializers.Serializer):
  code = serializers.CharField(max_length=10)


class WindowSizeSerializer(serializers.Serializer):
  window_size = serializers.IntegerField()


class StartEndCodeSerializer(StartEndDate, CodeSerializer):
  class Meta:
    ref_name = 'StartEndCodeSerializer'


class StartEndCodeWindowSerializer(StartEndDate, CodeSerializer, WindowSizeSerializer):
  class Meta:
    ref_name = 'StartEndCodeSerializer'