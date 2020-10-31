from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stock.serializers import CodeSerializer
from stock.core.strategies.ai import regression

__all__ = [
    'get_regression'
]

@swagger_auto_schema(
    method='GET',
    operation_id="회귀",
    operation_description="Consist Of Dense Layers",
    query_serializer=CodeSerializer,
    responses={
        201: 'GOOD',
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
    },
    tags=['tech'],
)
@api_view(['GET'])
def get_regression(request):
    serializer = CodeSerializer(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        predicated = regression(**serializer.validated_data)
        return Response(predicated, status=status.HTTP_200_OK)
    else:
        return Response(request, status=status.HTTP_400_BAD_REQUEST)
