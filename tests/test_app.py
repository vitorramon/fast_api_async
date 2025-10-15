from http import HTTPStatus

from fast_api_async.schemas import UserPublic

# Exercícios
# TODO: Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de PUT;
# TODO: Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de DELETE;
# TODO: Criar um endpoint de GET para pegar um único recurso como users/{id} e
# fazer seus testes para 200 e 404.
# TODO: Refatorar os testes para usar o user fixture
# TODO: Implementar o banco de dados para o endpoint de listagem por id, criado no exercício anterior.

def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA)

    - A: Arrange - Arranjo
    - A: Act - Executa o System Under Test (SUT)
    - A: Assert - Garanta que A == A

    """
    # Act
    response = client.get('/')
    # Assert
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK

# TODO: Refatorar os testes para usar o user fixture
def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


# def test_get_user(client):
#     response = client.get('/users/1')
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         'id': 1,
#         'email': 'alice@example.com',
#         'username': 'alice',
#     }


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'alice_updated',
            'email': 'alice@example.com',
            'password': 'new_secret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice_updated',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted',
    }

def test_update_user_should_return_not_found(client):
    response = client.put(
        '/users/666',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/666')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


# def test_get_user_should_return_not_found(client):
#     response = client.get('/users/666')
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user):
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'teste@test.com',
            'password': 'mynewsecret',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Email or username already exists'
    }
