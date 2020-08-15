from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Fitzme service Service Documents",
        default_version='all',
        description="""
        Fitzme service 입니다. 사용 가능한 service API를 탐색하고 테스트할 수 있습니다.
        """,
        contact=openapi.Contact(
            name="Intellisys Co., Ltd.",
            url="http://intellisys.co.kr",
            email="intellisys@intellisys.co.kr"
        ),
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stock.stock_urls'), name='stocks')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns