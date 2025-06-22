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


def test_pagina_test_deve_retornar_html():
    """
    Esse teste tem 3 etapas (AAA)

    - A: Arrange - Arranjo
    - A: Act - Executa o System Under Test (SUT)
    - A: Assert - Garanta que A == A

    """
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get('/pagina-test')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert '<h1>Olá mundo!</h1>' in response.text
