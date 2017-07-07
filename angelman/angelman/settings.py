from rdrf.settings import *

# Insert fkrp before rdrf and the rest of apps. This ensures templates
# and translations of fkrp get loaded first.

FALLBACK_REGISTRY_CODE = "angelman"
LOCALE_PATHS = env.getlist("locale_paths", ['/data/translations/locale'])

INSTALLED_APPS = [
    FALLBACK_REGISTRY_CODE,
] + INSTALLED_APPS

# Angelman WEBAPP_ROOT is different to RDRF base. This allows to find overriden templates
ANGELMAN_WEBAPP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES[0]['DIRS'] = [
    os.path.join(ANGELMAN_WEBAPP_ROOT, FALLBACK_REGISTRY_CODE, 'templates'),
] + TEMPLATES[0]['DIRS']

ROOT_URLCONF = '%s.urls' % FALLBACK_REGISTRY_CODE

LOGIN_FAILURE_LIMIT = 3
SEND_ACTIVATION_EMAIL = False

RECAPTCHA_SITE_KEY = env.get("recaptcha_site_key", "")
RECAPTCHA_SECRET_KEY = env.get("recaptcha_secret_key", "")

PROJECT_TITLE = "Global Angelman Syndrome Registry"
PROJECT_TITLE_LINK = "login_router"
