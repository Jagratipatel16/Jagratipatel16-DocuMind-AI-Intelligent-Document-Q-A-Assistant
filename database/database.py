import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# -------------------------
# Load environment variables from .env
# -------------------------

load_dotenv()

# -------------------------
# MySQL Credentials (from .env, never hardcoded)
# -------------------------

USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "3306")
DATABASE = os.getenv("DB_NAME", "documind_ai")

if not USERNAME or not PASSWORD:
    raise RuntimeError(
        "DB_USER / DB_PASSWORD not set. "
        "Copy .env.example to .env and fill in your MySQL credentials."
    )

DATABASE_URL = (
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# -------------------------
# SQLAlchemy Engine
# -------------------------

engine = create_engine(DATABASE_URL)

# -------------------------
# Session
# -------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------
# Base Class
# -------------------------

Base = declarative_base()