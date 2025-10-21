# FastAPI Async - Sistema de Gerenciamento de Usuários

Uma API REST moderna construída com FastAPI, incluindo sistema completo de autenticação JWT, gerenciamento de usuários e cobertura de testes abrangente.

## 🚀 Funcionalidades

- **Autenticação JWT**: Sistema completo de autenticação com tokens Bearer
- **Gerenciamento de Usuários**: CRUD completo (Create, Read, Update, Delete)
- **Segurança**: Hashing de senhas com Argon2
- **Banco de Dados**: SQLAlchemy 2.0 com migrações Alembic
- **Testes**: Suite completa de testes com pytest e cobertura
- **Documentação**: Docstrings completas e documentação automática
- **Linting**: Formatação de código com Ruff

## 🛠️ Tecnologias

- **FastAPI** 0.115.12 - Framework web moderno e rápido
- **SQLAlchemy** 2.0.41 - ORM para Python
- **Alembic** 1.16.4 - Migrações de banco de dados
- **PyJWT** 2.10.1 - Implementação JWT para Python
- **pwdlib[argon2]** 0.2.1 - Hashing seguro de senhas
- **pytest** 8.4.0 - Framework de testes
- **Ruff** 0.11.13 - Linter e formatador
- **Poetry** - Gerenciamento de dependências

## 📋 Pré-requisitos

- Python 3.13+
- Poetry

## ⚡ Instalação e Configuração

1. **Clone o repositório**
```bash
git clone https://github.com/vitorramon/fast_api_async.git
cd fast_api_async
```

2. **Instale as dependências**
```bash
poetry install
```

3. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Execute as migrações**
```bash
poetry run alembic upgrade head
```

## 🏃 Como Executar

### Desenvolvimento
```bash
poetry run task run
```

### Produção
```bash
poetry run uvicorn fast_api_async.app:app --host 0.0.0.0 --port 8000
```

A API estará disponível em `http://localhost:8000`

## 📚 Documentação da API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔗 Endpoints Principais

### Autenticação
- `POST /token` - Obter token de acesso
- `POST /users/` - Criar novo usuário

### Usuários (Protegidos por JWT)
- `GET /users/` - Listar usuários
- `PUT /users/{user_id}` - Atualizar usuário
- `DELETE /users/{user_id}` - Deletar usuário

## 🧪 Testes

### Executar todos os testes
```bash
poetry run task test
```

### Executar com cobertura
```bash
poetry run pytest --cov=fast_api_async --cov-report=html
```

### Ver relatório de cobertura
```bash
open htmlcov/index.html
```

## 🔍 Qualidade de Código

### Linting
```bash
poetry run task lint
```

### Formatação
```bash
poetry run task format
```

### Pré-formatação (com correções automáticas)
```bash
poetry run task pre_format
```

## 📁 Estrutura do Projeto

```
fast_api_async/
├── fast_api_async/
│   ├── __init__.py
│   ├── app.py          # Aplicação principal e endpoints
│   ├── database.py     # Configuração do banco
│   ├── models.py       # Modelos SQLAlchemy
│   ├── schemas.py      # Schemas Pydantic
│   ├── security.py     # Autenticação e segurança
│   └── settings.py     # Configurações da aplicação
├── tests/
│   ├── conftest.py     # Fixtures de teste
│   ├── test_app.py     # Testes dos endpoints
│   ├── test_db.py      # Testes do banco
│   └── test_security.py # Testes de autenticação
├── migrations/         # Migrações Alembic
├── htmlcov/           # Relatórios de cobertura
├── pyproject.toml     # Configuração do projeto
├── alembic.ini        # Configuração do Alembic
└── README.md
```

## 🗄️ Banco de Dados

### Criar nova migração
```bash
poetry run alembic revision --autogenerate -m "Descrição da migração"
```

### Aplicar migrações
```bash
poetry run alembic upgrade head
```

### Reverter migração
```bash
poetry run alembic downgrade -1
```

## 🔐 Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação:

1. Faça login via `POST /token` com email e senha
2. Use o token retornado no header `Authorization: Bearer <token>`
3. Tokens expiram em 30 minutos

### Exemplo de uso:
```bash
# 1. Obter token
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=senha123"

# 2. Usar token em endpoints protegidos
curl -X GET "http://localhost:8000/users/" \
     -H "Authorization: Bearer <seu_token_aqui>"
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona feature incrível'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Vitor Ramon**
- Email: vitorramon.info@gmail.com
- GitHub: [@vitorramon](https://github.com/vitorramon)

## 📝 Notas de Desenvolvimento

### TODO List
- [ ] Implementar endpoint GET /users/{id}
- [ ] Adicionar testes para cenários 404
- [ ] Implementar refresh tokens
- [ ] Adicionar paginação avançada
- [ ] Implementar rate limiting
- [ ] Adicionar logs estruturados

### Padrões de Commit
Este projeto segue [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `test:` testes
- `refactor:` refatoração
- `deps:` dependências