from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'meetscheduler',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'pa55word!!',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8'}
    }
}
