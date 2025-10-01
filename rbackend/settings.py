import os
from pathlib import Path
from django.contrib.messages import constants as messages
from datetime import timedelta
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# OAuth Configuration
GOOGLE_OAUTH2_CLIENT_ID = config('GOOGLE_OAUTH2_CLIENT_ID', default='')
GOOGLE_OAUTH2_SECRET = config('GOOGLE_OAUTH2_SECRET', default='')
GOOGLE_OAUTH2_REDIRECT_URI = 'http://localhost:8000/api/auth/google/'

GITHUB_OAUTH2_CLIENT_ID = config('GITHUB_OAUTH2_CLIENT_ID', default='')
GITHUB_OAUTH2_SECRET = config('GITHUB_OAUTH2_SECRET', default='')
ALLOWED_GITHUB_REDIRECT_URIS = [
    'http://localhost:5173/geo_pages1/login',
    'http://jackieng.hk/geo_pages1/login',
    'http://localhost:8000/api/auth/github/',
    'http://jackieng.hk/api/auth/github/',
    ]

# Quick-start development settings - unsuitable for production
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key-for-dev')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['209.97.164.73', 'jackieng.hk', '127.0.0.1',
                 'localhost', 'backend.jackieng.hk', 'test.jackieng.hk', 
                 '192.168.1.114', 'localhost:8000', 'localhost:5173',]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # for REST API
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # for authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    
    'channels', # for WebSocket support
    
    # apps in this project
    'gpsinfo',
    'accounts',
    'events',
    'api',
    'pages',
    'mobile_auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # Remove DEFAULT_PERMISSION_CLASSES or set to AllowAny
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
        
    # This ensures unauthenticated responses are handled properly
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'UNAUTHENTICATED_USER': None,
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
}
# settings.py

# Frontend URL
FRONTEND_URL = 'http://localhost:5173'

# Password reset configuration
ACCOUNT_EMAIL_CONFIRMATION_URL = FRONTEND_URL + '/geo_pages1/confirm-email/{0}'
ACCOUNT_PASSWORD_RESET_CONFIRM = FRONTEND_URL + '/geo_pages1/password-reset-confirm/{uidb64}/{token}'

# If you're using a custom adapter for password reset
#ACCOUNT_ADAPTER = 'yourapp.adapters.CustomAccountAdapter'

ASGI_APPLICATION = 'rbackend.asgi:application'  # Point to your ASGI application
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],  # Redis server for Channels
        },
    },
}


# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://209.97.164.73:5173",
    "https://jackieng.hk",
    "https://www.jackieng.hk",
]

# For CSRF protection with AJAX requests
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
]

# CSRF cookie settings
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read the cookie
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_SAMESITE = 'Lax'  # or 'None' if using HTTPS

CORS_ALLOW_ALL_ORIGINS = True  # Set to False for security; True was for debugging

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_CREDENTIALS = True

# Or completely disable CSRF for API views (NOT RECOMMENDED)
CSRF_EXEMPT_URLS = ['localhost:8000/api/auth/password/reset/']

ROOT_URLCONF = 'rbackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.user_registration_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'rbackend.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        # 'PORT': config('DB_PORT'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Hong_Kong'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'rbackend/static'),
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Allauth Configuration
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'accounts.CustomUser'

# Allauth settings
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

# ACCOUNT_USERNAME_REQUIRED = True
# ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_LOGIN_METHODS = {'username', 'email'}

# ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'email2*', 'username*', 'password1*', 'password2*']

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'GEOStar.hk'
ACCOUNT_MAX_EMAIL_ADDRESSES = 2
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'  # Use 'https' in production

# Social account settings
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# # Social OAuth providers
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': GOOGLE_OAUTH2_CLIENT_ID,
#             'secret': GOOGLE_OAUTH2_SECRET,
#         },
#         'SCOPE': ['profile', 'email'],
#         'AUTH_PARAMS': {'access_type': 'online'},
#         'OAUTH_PKCE_ENABLED': True,
#     },
#     'github': {
#         'APP': {
#             'client_id': GITHUB_OAUTH2_CLIENT_ID,
#             'secret': GITHUB_OAUTH2_SECRET,
#         },
#         'SCOPE': ['user:email'],
#     }
# }

# Login/Logout URLs
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'pages:index'
LOGOUT_REDIRECT_URL = 'pages:index'
ACCOUNT_LOGOUT_REDIRECT_URL = 'pages:index'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jackieng5000@gmail.com'
EMAIL_HOST_PASSWORD = 'xgei huhu vyco eqwk'
DEFAULT_FROM_EMAIL = 'noreply@jackieng.hk'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}