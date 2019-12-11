from .base import *

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_value_from_secret('DB_NAME'),
        'HOST': get_value_from_secret('DB_HOST'),
        'USER': get_value_from_secret('DB_USER'),
        'PASSWORD': get_value_from_secret('DB_PASSWORD'),
        'PORT': get_value_from_secret('DB_PORT'),
        'OPTIONS': {'charset': 'utf8'}
    }
}
