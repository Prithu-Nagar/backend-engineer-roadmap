"""WSGI entry point for the URL Shortener application."""

import os
import sys
from pathlib import Path
from types import ModuleType

PROJECT_DIR = Path(__file__).resolve().parent
package = ModuleType("url_shortener")
package.__path__ = [str(PROJECT_DIR)]
sys.modules.setdefault("url_shortener", package)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "url_shortener.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
