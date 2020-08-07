import coreschema
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import filters

from app.core.filters import MetaFilter

__all__ = [
    'FitzmeDjangoFilterBackend'
]


class FitzmeDjangoFilterBackend(DjangoFilterBackend):
    filter2schema = {
        MetaFilter: coreschema.Array,
        filters.CharFilter: coreschema.String,
        filters.NumberFilter: coreschema.Number,
        filters.BooleanFilter: coreschema.Boolean,
    }

    def get_coreschema_field(self, field):
        """Convert `django_filters.Filter` to `coreschema.Schema`."""
        field_cls = self.filter2schema.get(type(field), coreschema.String)
        return field_cls(description=str(field.extra.get('help_text', '')))
