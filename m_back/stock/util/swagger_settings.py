import coreschema
from drf_yasg import openapi
from drf_yasg.inspectors import CoreAPICompatInspector, FieldInspector
from drf_yasg.utils import force_real_str

__all__ = [
    'DjangoFilterInspector',
    'MultiCollectionFormatInspector',
]


class DjangoFilterInspector(CoreAPICompatInspector):
    location_to_in = {
        'query': openapi.IN_QUERY,
        'path': openapi.IN_PATH,
        'form': openapi.IN_FORM,
        'body': openapi.IN_FORM,
    }
    coreapi_types = {
        coreschema.Array: openapi.TYPE_ARRAY,
        coreschema.Integer: openapi.TYPE_INTEGER,
        coreschema.Number: openapi.TYPE_NUMBER,
        coreschema.String: openapi.TYPE_STRING,
        coreschema.Boolean: openapi.TYPE_BOOLEAN,
    }

    def coreapi_field_to_parameter(self, field):
        """Convert `coreschema.Schema` to `openapi.Parameter`."""
        schema = field.schema
        schema_type = self.coreapi_types.get(type(schema), openapi.TYPE_STRING)

        # Additional args
        coreschema_attrs = ['format', 'pattern', 'enum', 'min_length', 'max_length']
        additional_args = {attr: getattr(schema, attr, None) for attr in coreschema_attrs}
        if schema_type == openapi.TYPE_ARRAY:
            additional_args['items'] = openapi.Items(type='string')
            additional_args['collectionFormat'] = 'multi'

        return openapi.Parameter(
            name=field.name,
            in_=self.location_to_in[field.location],
            description=force_real_str(schema.description) if schema else None,
            required=field.required,
            type=schema_type,
            **additional_args
        )


class MultiCollectionFormatInspector(FieldInspector):
    """Use collectionFormat: multi for array-type parameters."""
    def process_result(self, result, method_name, obj, **kwargs):
        if isinstance(result, openapi.Parameter):
            if result['type'] == openapi.TYPE_ARRAY:
                if result['in'] in (openapi.IN_FORM, openapi.IN_QUERY):
                    result.collection_format = 'multi'

        return result
