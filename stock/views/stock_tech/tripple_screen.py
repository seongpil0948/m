from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stock.core.strategies.tech import tripple_screen
from stock.serializers.stock_tech import TrippleScreenSerializer


__all__ = [
  'get_tripple_screen'
]

@swagger_auto_schema(
    method='GET',
    operation_id="tripple_screen",
    operation_description="Tripple Screen 이미지를 제공 합니다.",
    query_serializer=TrippleScreenSerializer,
    responses={
        201: 'GOOD',
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
    },
    tags=['tech'],
)
@api_view(['GET'])
def get_tripple_screen(request):
  serializer = TrippleScreenSerializer(data=request.query_params)
  if serializer.is_valid(raise_exception=True):
    image_path = tripple_screen(**serializer.data)
  return Response({'image_path': image_path}, status=status.HTTP_200_OK)

        
