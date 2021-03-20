from .base import *

DEBUG = False
ALLOWED_HOST = ['molepangbe.pythonanywhere.com']

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:3000',
    'http://localhost:3000'
]
