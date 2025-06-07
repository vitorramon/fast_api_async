from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api_async.app import app


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)

    - A: Arrange - Arranjo
    - A: Act - Executa o System Under Test (SUT)
    - A: Assert - Garanta que A == A

    """
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get('/')
    # Assert
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK
