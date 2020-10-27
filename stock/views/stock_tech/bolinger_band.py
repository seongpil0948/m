from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stock.core.strategies.tech import bolinger_band
from stock.serializers.stock_tech import BolingerBandSerializer

__all__ = [
  'get_bolinger_band'
]

@swagger_auto_schema(
    method='GET',
    operation_id="bolinger_band",
    operation_description="볼린저 밴드 이미지를 제공 합니다.",
    query_serializer=BolingerBandSerializer,
    responses={
        201: 'GOOD',
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
    },
    tags=['tech'],
)
@api_view(['GET'])
def get_bolinger_band(request):
	serializer = BolingerBandSerializer(data=request.query_params)
	if serializer.is_valid(raise_exception=True):
		image_path = bolinger_band(**serializer.data)
		return Response({'image_path': image_path}, status=status.HTTP_200_OK)
	else:
		return Response(request.query_params, status=status.HTTP_400_BAD_REQUEST)

        
