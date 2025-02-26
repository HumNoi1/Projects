import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.setup import setup_app

if __name__ == "__main__":
    setup_app()