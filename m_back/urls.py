from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="SP WORLD",
        default_version='stock',
        description="""
        Stock World
        """,
        contact=openapi.Contact(
            name="SP WORLD",
            url="yet..",
            email="seongpil0948@gmail.com"
        ),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stock.urls.common_urls'), name='stocks'),
    path('tech/', include('stock.urls.stock_tech_urls'), name='tech'),
    path('ai/', include('stock.urls.ai_urls'), name='ai')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns