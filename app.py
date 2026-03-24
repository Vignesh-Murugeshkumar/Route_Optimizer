"""
Root-level app wrapper for Render deployment.
This allows gunicorn to find the app from the project root.
"""
import sys
from pathlib import Path

# Add ambulance_ucs to path so we can import from it
sys.path.insert(0, str(Path(__file__).parent / "ambulance_ucs"))

# Import the Flask app
from app import app

if __name__ == "__main__":
    app.run()
