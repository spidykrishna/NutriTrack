#!/usr/bin/env python
import os
import sys

# Setup path
sys.path.insert(0, '/mnt/okcomputer/output/meal_planner')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_planner.settings')

import django
django.setup()

from django.core.management import call_command

if __name__ == "__main__":
    # Run the development server
    call_command('runserver', '0.0.0.0:8000')
