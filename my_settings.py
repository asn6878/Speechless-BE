from pathlib import Path

# 시크릿 키
SECRET_KEY = 'django-insecure-^e3(0nuj5f*s#knr7=23t45%832m5or(l^hz*_vt%%a#5auy^#'

# sqlite3 데이터베이스
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}