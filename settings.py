import os
<<<<<<< HEAD
from pathlib import Path
from django.core.management.utils import get_random_secret_key
SECRET_KEY = get_random_secret_key()
=======
import sys
sys.path.append('/home/yuikairi/yuikairi.pythonanywhere.com')
from pathlib import Path
>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
<<<<<<< HEAD
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

=======
STATIC_DIR = os.path.join(BASE_DIR, 'static')
>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

<<<<<<< HEAD
SESSION_COOKIE_SECURE = True  # HTTPSを使用している場合のみTrueに設定してください
SESSION_COOKIE_HTTPONLY = True  # JavaScriptからのアクセスを防ぐための設定
SESSION_FILE_PATH = "/tmp/django_sessions"
SESSION_COOKIE_AGE = 1209600
CSRF_COOKIE_SECURE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'



=======
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default_secret_key_for_local')

# SECURITY WARNING: don't run with debug turned on in production!
>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d
DEBUG = False

ALLOWED_HOSTS = ['yuikairi.pythonanywhere.com']


<<<<<<< HEAD


=======
>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
<<<<<<< HEAD
    'accounts',
    'boards',
    'django_extensions',
    'scripts',
=======
    'my_board.accounts.apps.AccountsConfig',
    'my_board.boards.apps.BoardsConfig',
    'django_extensions',
    'scripts',

>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'board_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'board_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yuikairi$default',
        'USER': 'yuikairi',
        'PASSWORD': '19870802hy',
<<<<<<< HEAD
        'HOST': 'yuikairi.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
=======
        'HOST': 'mysql.server',
>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d
    }
}


<<<<<<< HEAD


=======
>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
AUTH_USER_MODEL = 'accounts.CustomUser'#accountsのユーザーに設定→マイグレーション→views.pyでホーム画面作成

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# メールサーバーへの接続設定
DEFAULT_FROM_EMAIL = 'xxxxxx@gmail.com'  # メールの送信元のアドレスを入力
EMAIL_HOST = 'smtp.gmail.com'            # GmailのSMPTサーバー　　　
EMAIL_PORT = 587                         # SMPTサーバーのポート番号
<<<<<<< HEAD
EMAIL_HOST_USER = '#'    # Gmailのアドレスを入力
EMAIL_HOST_PASSWORD = '#' # Gmailのアプリ用パスワードを入力
EMAIL_USE_TLS = True # SMTP サーバと通信する際に TLS (セキュア) 接続を使う

AUTHENTICATION_BACKENDS = [
    'accounts.backends.MyCustomBackend',
=======
EMAIL_HOST_USER = 'your_email_here@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password_here'
EMAIL_USE_TLS = True # SMTP サーバと通信する際に TLS (セキュア) 接続を使う

AUTHENTICATION_BACKENDS = [
     'accounts.backends.MyCustomBackend',
>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d
    'django.contrib.auth.backends.ModelBackend',
]

POSTS_PER_PAGE = 10

LOGGING = {
<<<<<<< HEAD
    "version": 1,  # the dictConfig format version
    "disable_existing_loggers": False,  # retain the default loggers
=======
    'version': 1,                       # the dictConfig format version
    'disable_existing_loggers': False,  # retain the default loggers
>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d
}




<<<<<<< HEAD
=======

>>>>>>> 7121590d2f44f53137001a0f8830fcf6c350dc0d
