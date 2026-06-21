from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# Railway даёт DATABASE_URL для PostgreSQL
DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///finance.db")

# Railway даёт postgres://, SQLAlchemy хочет postgresql+asyncpg://
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)