from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stock.serializers.stock_tech.momentum import DualMomentumSerializer
from stock.core.strategies.tech import DualMomentum

__all__ = [
    'dual_momentum'
]

@swagger_auto_schema(
    method='GET',
    operation_id="듀얼 모멘텀",
    operation_description="듀얼 모멘텀 기법을 제공 합니다",
    query_serializer=DualMomentumSerializer,
    responses={
        201: 'GOOD',
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
    },
    tags=['tech'],
)
@api_view(['GET'])
def dual_momentum(request):
    serializer = DualMomentumSerializer(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        ranked = DualMomentum(**serializer.validated_data).abs_momentum
        return Response(ranked, status=status.HTTP_200_OK)
    else:
        return Response(request, status=status.HTTP_400_BAD_REQUEST)
