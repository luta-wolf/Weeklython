import django
from pathlib import Path
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent
settings.configure(
    DATABASES={
        'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        'bot',
    ]
)
django.setup()

# Now this script or any imported module can use any part of Django it needs.
