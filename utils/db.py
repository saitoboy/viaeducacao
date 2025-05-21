# Este módulo centraliza a configuração da conexão com o banco de dados usando SQLAlchemy.
# Ele carrega a string de conexão do arquivo .env e fornece uma função para obter o engine,
# facilitando o acesso ao banco em outros módulos do projeto ViaEducação.
# Basta importar get_engine() para usar a conexão de forma prática e segura!
#
# Exemplo de uso:
# from utils.db import get_engine
# engine = get_engine()
#
# Certifique-se de que a variável DATABASE_URL está definida no seu .env.

from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não configurada no arquivo .env")
    return create_engine(DATABASE_URL)
