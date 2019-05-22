# flake8: noqa
import os

from rdrf.settings import *
import angelman


FALLBACK_REGISTRY_CODE = "angelman"
LOCALE_PATHS = env.getlist("locale_paths", ['/data/translations/locale'])

# Adding the angelman app first, so that its templates overrides base templates
INSTALLED_APPS = [
    FALLBACK_REGISTRY_CODE,
] + INSTALLED_APPS

ROOT_URLCONF = '%s.urls' % FALLBACK_REGISTRY_CODE

SEND_ACTIVATION_EMAIL = False

RECAPTCHA_SITE_KEY = env.get("recaptcha_site_key", "")
RECAPTCHA_SECRET_KEY = env.get("recaptcha_secret_key", "")

PROJECT_TITLE = env.get("project_title", "Global Angelman Syndrome Registry")
PROJECT_TITLE_LINK = "login_router"


# Registration
REGISTRATION_CLASS = "angelman.patient_registration.AngelmanRegistration"


# For now keep password validation same as on front end
# at least 6 chars
# has a number
AUTH_PASSWORD_VALIDATORS = [{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'rdrf.auth.password_validation.HasNumberValidator',
    },
]

VERSION = env.get('app_version', '%s (ang)' % angelman.VERSION)
