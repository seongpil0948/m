from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stock.core.strategies.tech import efficient_portfolio

__all__ = [
  'get_efficient_portfolio'
]

@swagger_auto_schema(
    method='GET',
    operation_id="efficient_portfolio",
    operation_description="효율적 투자선과 샤프지수의 포트폴리오 이미지를 제공 합니다.",
    responses={
        201: 'GOOD',
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
    },
    tags=['tech'],
)
@api_view(['GET'])
def get_efficient_portfolio(request):
		image_path = efficient_portfolio()
		return Response({'image_path': image_path}, status=status.HTTP_200_OK)

        
