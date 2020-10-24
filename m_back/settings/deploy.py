from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False
CORS_ORIGIN_WHITELIST = [
  "localhost:5555",
  "https://mincorp.netlify.app/"
]