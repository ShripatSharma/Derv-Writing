"""
Database Connection
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)

# ==========================================
# Server Connection
# ==========================================

SERVER_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
)

server_engine = create_engine(
    SERVER_URL,
    pool_pre_ping=True,
    echo=False,
)

# ==========================================
# Database Connection
# ==========================================

from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

# ==========================================
# Utility Function
# ==========================================

def execute_sql(query):
    with engine.begin() as conn:
        conn.execute(text(query))