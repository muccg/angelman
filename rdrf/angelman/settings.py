from rdrf.settings import *

# Insert angelman before rdrf and the rest of apps. This ensures
# templates and translations of angelman get loaded first.
INSTALLED_APPS = [
     "angelman",
] + INSTALLED_APPS

FALLBACK_REGISTRY_CODE = "ang"

LOGIN_FAILURE_LIMIT = 3
