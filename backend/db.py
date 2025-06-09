import psycopg2
import os
from dotenv import load_dotenv


os.environ["DB_HOST"] = "localhost"  # Força o valor correto
load_dotenv()

print("DEBUG backend DB_HOST:", os.getenv("DB_HOST"))  # Debug

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
