"""Test fixtures for TraceLens"""

import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.storage import storage


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    """Clear storage before each test."""
    storage.clear()
    yield
    storage.clear()


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        "name": "Support Chatbot",
        "description": "Customer support assistant for the billing team"
    }


@pytest.fixture
def sample_project(client, sample_project_data):
    """Create a project and return its data."""
    response = client.post("/projects", json=sample_project_data)
    return response.json()


@pytest.fixture
def sample_trace_data():
    """Sample trace data for testing.

    project_id must be filled in by the test.
    """
    return {
        "model": "openai/gpt-4o-mini",
        "prompt": "Summarize this support ticket: my invoice is wrong",
        "response": "The customer reports an incorrect invoice amount.",
        "prompt_tokens": 1000,
        "completion_tokens": 500,
        "latency_ms": 840,
        "status": "success",
        "tags": ["support", "billing"]
    }
