import sys
import os

# Add the authentic_events directory to the Python search path to resolve relative imports
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(basedir, 'authentic_events'))

# Import the main app instance from app.py
from authentic_events.app import app
