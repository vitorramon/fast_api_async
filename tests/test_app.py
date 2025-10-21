from http import HTTPStatus

from fast_api_async.schemas import UserPublic

# Exercícios
# TODO: Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de
# PUT;
# TODO: Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de
# DELETE;
# TODO: Criar um endpoint de GET para pegar um único recurso como users/{id} e
# fazer seus testes para 200 e 404.
# TODO: Refatorar os testes para usar o user fixture
# TODO: Implementar o banco de dados para o endpoint de listagem por id,
# criado no exercício anterior.


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
    """
    Testa a criação de um novo usuário via endpoint POST /users/.

    Verifica se um usuário é criado corretamente com os dados fornecidos
    e se a resposta retorna os dados públicos esperados.
    """
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


def test_read_users(client, user, token):
    """
    Testa a listagem de usuários via endpoint GET /users/.

    Verifica se o endpoint protegido retorna corretamente a lista
    de usuários quando autenticado com um token válido.
    """
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

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


def test_update_user(client, user, token):
    """
    Testa a atualização de um usuário via endpoint PUT /users/{id}.

    Verifica se um usuário pode atualizar seus próprios dados quando
    autenticado e se as mudanças são aplicadas corretamente.
    """
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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


def test_delete_user(client, user, token):
    """
    Testa a exclusão de um usuário via endpoint DELETE /users/{id}.

    Verifica se um usuário pode deletar sua própria conta quando
    autenticado e se a operação retorna a mensagem de confirmação.
    """
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted',
    }


# def test_update_user_should_return_not_found(client):
#     response = client.put(
#         '/users/666',
#         json={
#             'username': 'bob',
#             'email': 'bob@example.com',
#             'password': 'mynewpassword',
#         },
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


# def test_delete_user_should_return_not_found(client):
#     response = client.delete('/users/666')
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


# def test_get_user_should_return_not_found(client):
#     response = client.get('/users/666')
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user, token):
    """
    Testa o tratamento de erro de integridade ao atualizar usuário.

    Verifica se o endpoint retorna erro 409 (CONFLICT) quando tenta
    atualizar um usuário com username/email já existente.
    """
    client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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
