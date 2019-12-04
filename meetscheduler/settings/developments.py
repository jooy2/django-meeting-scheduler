from .base import *

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z7p$gg&0nh)7-t-xg3*tyanq%(r5vew+8%!26*ebx^to$bfz&c'

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
