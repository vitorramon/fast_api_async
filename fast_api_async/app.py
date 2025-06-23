from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_api_async.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='Minha API')

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    """
    Cria um usuário com os dados fornecidos.
    """
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    """
    Retorna todos os usuários cadastrados.
    """
    return {'users': database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)

    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Usuário com ID {user_id} não encontrado.',
        )

    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Usuário com ID {user_id} não encontrado.',
        )

    return database.pop(user_id - 1)


# Exercícios
# Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de PUT;
# Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de DELETE;
# Criar um endpoint de GET para pegar um único recurso como users/{id} e fazer seus testes para 200 e 404.
