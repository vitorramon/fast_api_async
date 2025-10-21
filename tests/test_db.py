from dataclasses import asdict

from sqlalchemy import select

from fast_api_async.models import User


def test_create_user(session, mock_db_time):
    """
    Testa a criação de usuário no banco de dados com timestamp mockado.

    Verifica se um usuário é criado corretamente no banco e se o
    timestamp de criação é definido pelo mock para testes determinísticos.
    """
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='secret')

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'test'))

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
    }
