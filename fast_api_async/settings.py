from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação usando Pydantic Settings.

    Gerencia as configurações da aplicação através de variáveis de ambiente
    ou arquivo .env. Herda de BaseSettings para validação automática e
    carregamento de configurações.

    Attributes:
        DATABASE_URL (str): URL de conexão com o banco de dados
    """
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    DATABASE_URL: str
