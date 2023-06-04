import os

if os.environ.get('ENVIRONMENT') == 'production':
    from .settings_production import *
else:
    from .settings_local import *