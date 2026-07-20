from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def no_cache(monkeypatch):
    """Force cache misses so tests always hit the product service logic."""
    with patch("app.services.cache_service.cache_get", return_value=None), \
         patch("app.services.cache_service.cache_set", return_value=None):
        yield


@pytest.fixture
def client():
    return TestClient(app)
