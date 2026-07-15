"""
Application Settings

Loads all environment variables
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# =====================================================
# Project Root
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv(PROJECT_ROOT / ".env")

# =====================================================
# Database Configuration
# =====================================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "option_writing")

# =====================================================
# Data Paths
# =====================================================

DATA_PATH = PROJECT_ROOT / "data"

RAW_DATA_PATH = DATA_PATH / "raw"

BHAVCOPY_PATH = RAW_DATA_PATH / "bhavcopy"

VIX_PATH = RAW_DATA_PATH / "india_vix"

TBILL_PATH = RAW_DATA_PATH / "risk_free_rate"

PROCESSED_PATH = DATA_PATH / "processed"

PARQUET_PATH = DATA_PATH / "parquet"

FINAL_PATH = DATA_PATH / "final"

LOG_PATH = PROJECT_ROOT / "logs"

SQL_PATH = PROJECT_ROOT / "sql"

MODEL_PATH = PROJECT_ROOT / "models"

REPORT_PATH = PROJECT_ROOT / "reports"