import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')

# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = ["*"]


CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS","").split(",")


AUTH_USER_MODEL='accounts.Account'
CSRF_TRUSTED_ORIGINS=os.getenv("CSRF_TRUSTED_ORIGINS","").split(",")
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
# Set session cookie age to 1 week (default is 1209600 seconds)



LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-us', _('English')),
    ('ar', _('Arabic')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/')
]


DEBUG = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    'mathfilters',
    'apps.accounts.apps.AccountsConfig',
    'apps.home.apps.HomeConfig',
    'apps.store.apps.StoreConfig',
    'apps.category.apps.CategoryConfig',
    'apps.job.apps.JobConfig',
    'apps.contact.apps.ContactConfig',
    'apps.Admin.apps.AdminConfig',
    'apps.business_listing.apps.BusinessListingConfig',
    'apps.property.apps.PropertyConfig',
    'apps.vechiles.apps.VechilesConfig',
    'apps.discover.apps.DiscoverConfig',
    'channels',
    'apps.message',

    

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
#For removing origin issue in google login
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"


# Import urls
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.accounts.context_processors.user_profile',
               
               
            ],
        },
    },
]

# WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = "config.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


TIME_ZONE = 'Asia/Dubai'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
  
]
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "app_cache_table",
    }
}


FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 Mb limit


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '.debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }



# for django messages


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
   
}
