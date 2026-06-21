from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv("TOKEN")
DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///finance.db")