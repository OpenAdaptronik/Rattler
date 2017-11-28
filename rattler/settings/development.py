from .base import *

print('HSLOO')

# DEBUG = True equals Development-Mode
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dqfc+6=p^h_qo0^j_bs4yb1q%6r%$)=y8)c_q)7s_b$qp4ldx$'
ALLOWED_HOSTS = ['*']

# Adding the debug_toolbar to the Installed_Apps
INSTALLED_APPS += [
    #'debug_toolbar'
]


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rattler',
        'USER': 'rattler',
        'PASSWORD': '123456',
        'HOST': 'db'
    }
}





#MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#DEBUG_TOOLBAR_CONFIG = {
#    'JQUERY_URL': '',
#}

#
# EMAIL_BACKEND = ''
# EMAIL_HOST = ''
# EMAIL_PORT =
# EMAIL_HOST_USER =
# EMAIL_HOST_PASSWORD =
# EMAIL_USE_TLS =

