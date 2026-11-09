#!/usr/bin/env python
"""Command-line entry point for the URL Shortener Django project."""

import os
import sys
from pathlib import Path
from types import ModuleType

PROJECT_DIR = Path(__file__).resolve().parent
package = ModuleType("url_shortener")
package.__path__ = [str(PROJECT_DIR)]
sys.modules.setdefault("url_shortener", package)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "url_shortener.settings")

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
