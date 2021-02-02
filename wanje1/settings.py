"""
Django settings for wanje1 project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '(n9h+vyqdqi^trto5tz@)yyx7i(o$d1hrowhas1bh(&-57&xpm'
SECRET_KEY = os.environ.get('SECRET_KEY','(n9h+vyqdqi^trto5tz@)yyx7i(o$d1hrowhas1bh(&-57&xpm')
#시크릿키는 그대로 사용하면 된다. os.environ.get()으로 개발환경 파일에서 값을 읽어올 수 있다.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG',1))
# True는 1일 의미한다. 그렇지 않은 경우에는 0이 될 수 있도록 만들면 된다.
if os.environ.get('DJANGO_ALLOWED_HOSTS'):
    ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')
else:
    ALLOWED_HOSTS = []
#호스트로 허용되는 주소를 적어두는 곳이다. 서비스로 공개할때는 보안을 위해 서버가 될 url만 남겨놓는것이 맞다. 반면에 개발할때는 127.0.0.1이나
#localhost로 장고에 접근할 수 있어야 된다. 이런 목적으로 env파일에서 DJANGO_ALLOWED_HOST를 읽어올 수 있다면 그 값을 사용하록 없다면 이전과 동일하게
#사용한다.

# ALLOWED_HOSTS = [
# 
# ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', #더 많은 장고의 기능을 제공한다.
    
    'crispy_forms', # 템플릿의 폼의 모양을 예쁘게 바꿔준다. pip install django-crispy_forms로 설치해야된다.
                    #그리고 아래에 CRISPY_TEMPLATE_PACK = 'bootstrap4'라고 해야된다.

    'markdownx',   #포스트를 작성할때 줄바꿈이나 글자크기를 바꾸거나 내용중간에 그림을 넣을 수 있게 해준다.
                    #piip install django-markdownx를 해주면 된다. 그리고 url에도 경로를 추가해야 원활하게 작동한다.
    'blog',
    'single_pages',


    'django.contrib.sites', #django.contrib.sites도 넣어야 allauth가 작동한다. 그리고 다하고 migrate도 해준다.
    'allauth',              #그리고 admin에서 site에 들어가서 도메인을 바꾸고 template을 수정한다.
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', #이 4가지 라이브러리를 입력해야된다. 그러면 구글 로그인 기능을 사용 할 수 있다. 
    
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

ROOT_URLCONF = 'wanje1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'wanje1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE','django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE',os.path.join(BASE_DIR,'db.sqlite3')),
        'USER': os.environ.get('SQL_USER','user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD','password'),
        'HOST': os.environ.get('SQL_HOST','localhost'),
        'PORT': os.environ.get('SQL_PORT','5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join('BASE_DIR','_static') #_static으로 바꾼다. wsgi

MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR,'_media')

CRISPY_TEMPLATE_PACK = 'bootstrap4' #crispy_forms의 스타일을 bootstarp4로 하겠다는 뜻

AUTHENTICATION_BACKENDS = ( #authentification_beckends설정과 site_id를 추가한다. 그 뒤에 url도 추가한다.
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED=True #회원가입을 할때 이메일을 반드시 받는것으로 설정한다. 
ACCOUNT_EMAIL_VERIFICATION='none' #이메일 발송세팅이 추가적으로 필요해서 여기서는 다루지 않는다.(필요하면 나중에 공부하자.)
LOGIN_REDIRECT_URL = '/blog/'  # 로그인하면 블로그 목록 페이지로 리다이렉트 되도록 설정한다.