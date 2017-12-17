from .base import *

# DEBUG = True equals Development-Mode
DEBUG = True

# Cache Settings https://docs.djangoproject.com/en/2.0/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'cache:11211',
        'KEY_PREFIX': 'rattler-default',
    },
    'sessions': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'cache:11211',
        'KEY_PREFIX': 'rattler-session',
    },
}

# Databses https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rattler',
        'USER': 'rattler',
        'PASSWORD': '123456',
        'HOST': 'db'
    }
}

# E-Mails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp'

# Sessions
SESSION_CACHE_ALIAS = 'sessions'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
