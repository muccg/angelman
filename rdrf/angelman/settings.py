from rdrf.settings import *

# Insert fkrp before rdrf and the rest of apps. This ensures templates
# and translations of fkrp get loaded first.

FALLBACK_REGISTRY_CODE = "angelman"

INSTALLED_APPS = [
    FALLBACK_REGISTRY_CODE,
] + INSTALLED_APPS

# Angelman WEBAPP_ROOT is different to RDRF base. This allows to find overriden templates
ANGELMAN_WEBAPP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES[0]['DIRS'] = [
    os.path.join(ANGELMAN_WEBAPP_ROOT, FALLBACK_REGISTRY_CODE, 'templates'),
] + TEMPLATES[0]['DIRS']

LANGUAGES += (
    ('no', 'Norwegian'),
)

ROOT_URLCONF = '%s.urls' % FALLBACK_REGISTRY_CODE

LOGIN_FAILURE_LIMIT = 3
SEND_ACTIVATION_EMAIL = False

EMAIL_NOTIFICATIONS += (
    ("account-locked", "Account Locked"),
)

RECAPTCHA_SITE_KEY = env.get("recaptcha_site_key", "")
RECAPTCHA_SECRET_KEY = env.get("recaptcha_secret_key", "")
