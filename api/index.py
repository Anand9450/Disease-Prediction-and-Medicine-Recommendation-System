import sys
import os

# Add the parent directory to sys.path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel expects a variable named 'app' (or handler)
# We already have 'app' from main.py
