import os

DATABASES = {
    'postgres': {
        'host': os.environ.get('M_HOSTNAME', 'secret'),
        'port': os.environ.get('M_PORT', 5432),
        'user': os.environ.get('M_USERNAME', 'secret'),
        'password': os.environ.get('M_PASSWORD', 'secret'),
        'database': os.environ.get('M_DATABASE', 'secret')
    }
}
