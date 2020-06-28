from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@_1+7x42#p@h*ubuj52wv8$)lgryv9^7nc5eru-*u3)s&n9l&l'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += [
    'wagtail.contrib.styleguide',
    'django_extensions',
    'debug_toolbar',
]

INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

for logger in LOGGING['loggers'].values():
    logger['handlers'] = ['console']
    logger['level'] = 'DEBUG'

AUTH_PASSWORD_VALIDATORS = []

WAGTAIL_SITE_NAME = 'Portfolio Dev'
BASE_URL = 'http://127.0.0.1:8000'


try:
    from .local import *
except ImportError:
    pass
