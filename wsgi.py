"""
WSGI config for ENTstore project - Root level wrapper
"""

import os
import sys

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Change working directory to backend
os.chdir(backend_path)

# Import the actual WSGI application
from myproject.wsgi import application