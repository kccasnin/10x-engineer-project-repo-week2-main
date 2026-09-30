# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.storage import storage


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)

@pytest.fixture
def sample_prompt_data():
    """Sample prompt data for testing."""
    return {
        "title": "Sample Prompt",
        "content": "This is a test prompt.",
        "description": "A description for the sample prompt."
    }

@pytest.fixture
def sample_collection_data():
    """Sample collection data for testing."""
    return {
        "name": "Sample Collection",
        "description": "A collection for storing prompts."
    }

@pytest.fixture
def sample_tag_data():
    """Sample tag data for testing."""
    return {
        "name": "Sample Tag"
    }

@pytest.fixture(autouse=True)
def clear_storage():
    """Clear storage before each test."""
    storage.clear()
    yield
    storage.clear()
