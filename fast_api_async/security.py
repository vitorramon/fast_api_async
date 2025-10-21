from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_async.database import get_session
from fast_api_async.models import User

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str) -> str:
    """
    Gera um hash seguro da senha usando Argon2.

    Utiliza a biblioteca pwdlib com configurações recomendadas
    para criar um hash criptograficamente seguro da senha.

    Args:
        password (str): Senha em texto plano a ser hasheada

    Returns:
        str: Hash da senha usando Argon2
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash armazenado.

    Utiliza verificação segura do Argon2 para comparar a senha
    fornecida com o hash armazenado no banco de dados.

    Args:
        plain_password (str): Senha em texto plano a ser verificada
        hashed_password (str): Hash da senha armazenado no banco

    Returns:
        bool: True se a senha corresponde ao hash, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """
    Cria um token JWT de acesso com tempo de expiração.

    Gera um token JWT contendo os dados fornecidos mais um
    timestamp de expiração. O token é assinado com a chave secreta.

    Args:
        data (dict): Dados a serem incluídos no payload do token

    Returns:
        str: Token JWT codificado como string
    """
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    """
    Obtém o usuário atual a partir do token JWT fornecido.

    Valida o token JWT, extrai o email do usuário e busca o usuário
    correspondente no banco de dados. Usado como dependency em endpoints
    que requerem autenticação.

    Args:
        session (Session): Sessão do banco de dados injetada via dependency
        token (str): Token JWT extraído do header Authorization

    Raises:
        HTTPException: 401 UNAUTHORIZED se token é inválido
        HTTPException: 401 UNAUTHORIZED se token não contém 'sub'
        HTTPException: 401 UNAUTHORIZED se usuário não existe

    Returns:
        User: Instância do usuário autenticado
    """
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))
    if not user:
        raise credentials_exception
    return user
