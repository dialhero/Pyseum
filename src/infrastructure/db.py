from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[2] / ".ignore" / ".env"
load_dotenv(dotenv_path=env_path)

DB_SECRET = os.getenv("DB_SECRET")
DB_SECRET_KEY = os.getenv("DB_SECRET_KEY")

db_secret = {
    "secret": DB_SECRET, 
    "secret_key": DB_SECRET_KEY}

print(f"secret: {db_secret['secret']}")
print(f"secret_key: {db_secret['secret_key']}")