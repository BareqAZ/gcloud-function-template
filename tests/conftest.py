# Python standard library
import os
import sys

# Third-party libraries
import pytest

# Add the above directory to sys.path so that we can import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Local imports
from main import app  # noqa E402


@pytest.fixture
def client():
    return app.test_client()


headers = {
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json",
}
