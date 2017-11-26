from .base import *

#Security Warning: don't run with debug turned on in production
DEBUG = False

ALLOWED_HOSTS = ['*.openadaptronik.com', '*.openadaptronik.de', '192.168.99.100']
SECRET_KEY ='%secretkey%'



# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '%name%',
        'USER': '%name%',
        'PASSWORD': '%password%',
        'HOST': '%db%'
    }
}


#
# EMAIL_BACKEND = ''
# EMAIL_HOST = ''
# EMAIL_PORT =
# EMAIL_HOST_USER =
# EMAIL_HOST_PASSWORD =
# EMAIL_USE_TLS =