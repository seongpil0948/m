from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from stock.views.stock_tech import *

app_name = 'tech'

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
    # API Document
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0)),
    re_path('swagger.(json|yaml)$', schema_view.without_ui(cache_timeout=0)),

    path('dual_momentum', dual_momentum)
]