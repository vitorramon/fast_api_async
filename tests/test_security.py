from http import HTTPStatus

from jwt import decode

from fast_api_async.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    """
    Testa a criação e decodificação de tokens JWT.

    Verifica se os tokens são criados corretamente, contêm os dados
    esperados e incluem o campo de expiração.
    """
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_get_token(client, user):
    """
    Testa a obtenção de token via endpoint POST /token.

    Verifica se o endpoint de autenticação retorna um token válido
    quando fornecidas credenciais corretas.
    """
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_jwt_invalid_token(client):
    """
    Testa o comportamento com token JWT inválido.

    Verifica se endpoints protegidos retornam erro 401 (UNAUTHORIZED)
    quando fornecido um token inválido ou malformado.
    """
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid_token'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# Exercícios

# TODO:1. Faça um teste para cobrir o cenário que levanta exception
# `credentials_exception` na autenticação caso o `user` não seja encontrado.
# Ao olhar a cobertura de `security.py` você vai notar que esse contexto não
# está coberto.

# TODO:2. Faça um teste para cobrir o cenário que levanta exception
# `credentials_exception` na autenticação caso o `email` seja enviado, mas não
# exista um User correspondente cadastrado na base de dados. Ao olhar a
# cobertura de `security.py` você vai notar que esse contexto não está
# coberto.

# TODO:3. Reveja os testes criados até a aula 5 e veja se eles ainda fazem
# sentido (testes envolvendo 409)
