import pytest
from fastapi.testclient import TestClient

from fast_api_async.app import app


@pytest.fixture(scope='module')
def client():
    # Arrange
    return TestClient(app)
