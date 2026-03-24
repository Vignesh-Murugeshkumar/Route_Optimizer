"""
Root-level app wrapper for Render deployment.
This allows gunicorn to find the app from the project root.
"""
import sys
from pathlib import Path

# Add project root to path (parent of this file)
sys.path.insert(0, str(Path(__file__).parent))

# Import the Flask app from ambulance_ucs package
from ambulance_ucs.app import app

if __name__ == "__main__":
    app.run()
