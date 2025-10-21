from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_api_async.database import get_session
from fast_api_async.models import User
from fast_api_async.schemas import (
    Message,
    Token,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_api_async.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI(title='Minha API')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


# TODO: Refatorar create_user para contemplar cenário de email e username
# duplicados
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    """
    Cria um novo usuário no sistema.

    Verifica se o username e email são únicos antes de criar o usuário.
    A senha é automaticamente hasheada antes de ser armazenada.

    Args:
        user (UserSchema): Dados do usuário (username, email, password)
        session (Session): Sessão do banco de dados injetada via dependency

    Raises:
        HTTPException: 400 BAD_REQUEST se username já existe
        HTTPException: 400 BAD_REQUEST se email já existe

    Returns:
        UserPublic: Dados públicos do usuário criado (sem a senha)
    """
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Lista todos os usuários cadastrados no sistema com paginação.

    Endpoint protegido que requer autenticação via Bearer token.
    Retorna uma lista paginada de usuários.

    Args:
        limit (int, optional): Número máximo de usuários por página.
            Defaults to 10.
        offset (int, optional): Número de registros a pular (para paginação).
            Defaults to 0.
        session (Session): Sessão do banco de dados injetada via dependency
        current_user (User): Usuário autenticado injetado via dependency

    Returns:
        UserList: Lista de usuários com paginação aplicada
    """
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


# @app.get(
#     '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
# )
# def read_user(user_id: int):
#     if user_id > len(database) or user_id < 1:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail='User not found'
#         )
#     return database[user_id - 1]


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Atualiza os dados de um usuário específico.

    Endpoint protegido que permite apenas que o próprio usuário
    atualize seus dados. Verifica permissões e unicidade de dados.

    Args:
        user_id (int): ID do usuário a ser atualizado
        user (UserSchema): Novos dados do usuário (username, email, password)
        session (Session): Sessão do banco de dados injetada via dependency
        current_user (User): Usuário autenticado injetado via dependency

    Raises:
        HTTPException: 403 FORBIDDEN se usuário tentar atualizar outro usuário
        HTTPException: 409 CONFLICT se email ou username já existem

    Returns:
        UserPublic: Dados públicos do usuário atualizado
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        current_user.email = user.email
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Email or username already exists',
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Remove um usuário específico do sistema.

    Endpoint protegido que permite apenas que o próprio usuário
    delete sua própria conta. Verifica permissões antes da exclusão.

    Args:
        user_id (int): ID do usuário a ser removido
        session (Session): Sessão do banco de dados injetada via dependency
        current_user (User): Usuário autenticado injetado via dependency

    Raises:
        HTTPException: 403 FORBIDDEN se usuário tentar deletar outro usuário

    Returns:
        Message: Mensagem de confirmação da exclusão
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted'}


# Exercícios
# TODO: Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de
# PUT;
# TODO: Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de
# DELETE;
# TODO: Criar um endpoint de GET para pegar um único recurso como users/{id}
# e fazer seus testes para 200 e 404.


@app.post('/token', response_model=Token, status_code=HTTPStatus.OK)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    Endpoint de autenticação para obter token de acesso.

    Valida as credenciais do usuário (email/senha) e retorna um
    JWT token para autenticação em endpoints protegidos.

    Args:
        form_data (OAuth2PasswordRequestForm): Dados de login
            (username=email, password)
        session (Session): Sessão do banco de dados injetada via dependency

    Raises:
        HTTPException: 401 UNAUTHORIZED se credenciais são inválidas
        HTTPException: 401 UNAUTHORIZED se usuário não existe

    Returns:
        Token: Access token JWT e tipo do token (Bearer)
    """

    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
