import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/supplier-collector'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import flask app
from app import app as application
