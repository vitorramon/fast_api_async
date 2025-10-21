from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_api_async.app import app
from fast_api_async.database import get_session
from fast_api_async.models import User, table_registry
from fast_api_async.security import get_password_hash


@pytest.fixture
def client(session):
    """
    Fixture que fornece um cliente de teste do FastAPI.

    Cria um TestClient configurado com override da sessão do banco
    para usar o banco em memória nos testes.

    Args:
        session (Session): Fixture de sessão do banco de dados

    Yields:
        TestClient: Cliente de teste configurado para os testes
    """

    # Arrange
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    """
    Fixture que fornece uma sessão de banco de dados em memória.

    Cria um banco SQLite em memória para isolamento completo entre
    testes. As tabelas são criadas e destruídas automaticamente.

    Yields:
        Session: Sessão do SQLAlchemy para o banco em memória
    """
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 5, 20)):
    """
    Context manager para mockar timestamps de criação no banco.

    Intercepta eventos de inserção no SQLAlchemy para definir
    um timestamp fixo no campo created_at, útil para testes determinísticos.

    Args:
        model: Modelo SQLAlchemy para interceptar eventos
        time (datetime, optional): Timestamp fixo a ser usado.
            Defaults to datetime(2025, 5, 20).

    Yields:
        datetime: O timestamp que está sendo usado no mock
    """

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    """
    Fixture que cria um usuário de teste no banco.

    Cria um usuário com dados fixos para usar nos testes, incluindo
    a senha em texto plano para facilitar testes de autenticação.

    Args:
        session (Session): Sessão do banco de dados

    Returns:
        User: Instância do usuário criado com atributo clean_password
    """
    password = 'testtest'
    user = User(
        username='testando',
        email='testando@test.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    """
    Fixture que gera um token de autenticação válido.

    Faz login com o usuário de teste e retorna o access_token
    para usar em testes de endpoints protegidos.

    Args:
        client (TestClient): Cliente de teste do FastAPI
        user (User): Usuário de teste para autenticação

    Returns:
        str: Token JWT de acesso válido
    """
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    token_data = response.json()
    return token_data['access_token']
