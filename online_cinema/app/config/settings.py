import os
from pathlib import Path

from dotenv import dotenv_values, load_dotenv
from split_settings.tools import include

load_dotenv()
dotenv_values(".env")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

include(
    'components/database.py',
    'components/application_definition.py',
    'components/password_validation.py',
    'components/internationalization.py',
)

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

INTERNAL_IPS = os.environ.get('INTERNAL_IPS').split(' ')


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
