from rest_framework import serializers

class StartEndDate(serializers.Serializer):
  start_date = serializers.CharField(
    max_length=50
  )
  end_date = serializers.CharField(
    max_length=50
  )

class Code(serializers.Serializer):
  code = serializers.CharField(max_length=10)