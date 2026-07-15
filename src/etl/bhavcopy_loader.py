"""
Bhavcopy ETL Loader
"""

from tqdm import tqdm
from pathlib import Path

import pandas as pd

from config.database import engine
from config.settings import BHAVCOPY_PATH

from src.etl.base_loader import BaseLoader
from src.etl.etl_logger import ETLLogger

from src.utils.file_utils import (
    calculate_file_hash,
    get_file_size
)

from src.utils.validators import (
    validate_required_columns,
    validate_empty_dataframe
)

TABLE_NAME = "raw_bhavcopy"

BATCH_SIZE = 5000

REQUIRED_COLUMNS = [

    "INSTRUMENT",
    "SYMBOL",
    "EXPIRY_DT",
    "STRIKE_PR",
    "OPTION",

    "OPEN",
    "HIGH",
    "LOW",
    "CLOSE",
    "SETTLE_PR",

    "CONTRACTS",
    "VAL_INLAKH",

    "OPEN_INT",
    "CHG_IN_OI",

    "TIMESTAMP"
]

COLUMN_MAPPING = {

    "INSTRUMENT": "instrument",
    "SYMBOL": "symbol",
    "EXPIRY_DT": "expiry_date",
    "STRIKE_PR": "strike_price",
    "OPTION": "option_type",

    "OPEN": "open_price",
    "HIGH": "high_price",
    "LOW": "low_price",
    "CLOSE": "close_price",
    "SETTLE_PR": "settle_price",

    "CONTRACTS": "contracts",
    "VAL_INLAKH": "value_in_lakh",

    "OPEN_INT": "open_interest",
    "CHG_IN_OI": "change_in_oi",

    "TIMESTAMP": "trading_date"
}

INSERT_SQL = """
INSERT INTO raw_bhavcopy
(
instrument,
symbol,
expiry_date,
strike_price,
option_type,

open_price,
high_price,
low_price,
close_price,
settle_price,

contracts,
value_in_lakh,

open_interest,
change_in_oi,

trading_date
)

VALUES
(
:instrument,
:symbol,
:expiry_date,
:strike_price,
:option_type,

:open_price,
:high_price,
:low_price,
:close_price,
:settle_price,

:contracts,
:value_in_lakh,

:open_interest,
:change_in_oi,

:trading_date
)

ON DUPLICATE KEY UPDATE

open_price = VALUES(open_price),
high_price = VALUES(high_price),
low_price = VALUES(low_price),
close_price = VALUES(close_price),
settle_price = VALUES(settle_price),

contracts = VALUES(contracts),
value_in_lakh = VALUES(value_in_lakh),

open_interest = VALUES(open_interest),
change_in_oi = VALUES(change_in_oi);
"""

def clean_dataframe(df):

    df = df.rename(columns=COLUMN_MAPPING).copy()

    df["expiry_date"] = pd.to_datetime(
        df["expiry_date"],
        format="%d/%m/%y",
        errors="coerce"
    )

    df["trading_date"] = pd.to_datetime(
        df["trading_date"],
        format="%d/%m/%y",
        errors="coerce"
    )

    numeric_columns = [
        "strike_price",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "settle_price",
        "contracts",
        "value_in_lakh",
        "open_interest",
        "change_in_oi"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

    # ============================================================
# Discover Bhavcopy Files
# ============================================================

def discover_files():

    files = sorted(BHAVCOPY_PATH.glob("*.csv"))

    print(f"Found {len(files)} files.")

    return files

# ============================================================
# Load Single File
# ============================================================

def load_single_file(file_path):

    print("=" * 60)
    print(f"Loading : {file_path.name}")
    print("=" * 60)

    # Calculate file metadata
    file_hash = calculate_file_hash(file_path)
    file_size = get_file_size(file_path)

    logger = ETLLogger(engine)

    try:

        # Skip if already loaded
        if logger.is_file_loaded(
            TABLE_NAME,
            file_hash
        ):
            print(f"⏭ Skipping {file_path.name} (already loaded)")
            return 0

        # Read CSV
        df = pd.read_csv(file_path)

        # Validate
        validate_empty_dataframe(df)

        validate_required_columns(
            df,
            REQUIRED_COLUMNS
        )

        print(f"Records Read : {len(df):,}")

        # Clean dataframe
        df = clean_dataframe(df)

        # Insert into database
        loader = BaseLoader(engine)

        loader.batch_insert(
            dataframe=df,
            insert_sql=INSERT_SQL
        )

        # Log success
        logger.log(
            file_name=file_path.name,
            file_size=file_size,
            file_hash=file_hash,
            table_name=TABLE_NAME,
            records_loaded=len(df),
            status="SUCCESS",
            remarks=""
        )

        print(f"✓ Loaded Successfully : {len(df):,} rows")

        return len(df)

    except Exception as e:

        # Log failure
        logger.log(
            file_name=file_path.name,
            file_size=file_size,
            file_hash=file_hash,
            table_name=TABLE_NAME,
            records_loaded=0,
            status="FAILED",
            remarks=str(e)
        )

        print(f"❌ Failed : {file_path.name}")
        print(f"Reason : {e}")

        raise
# ============================================================
# Load All Bhavcopy Files
# ============================================================

def load_bhavcopy():

    files = discover_files()

    if len(files) == 0:
        print("No Bhavcopy CSV files found.")
        return

    total_files = len(files)

    total_records = 0

    successful_files = 0

    failed_files = 0

    skipped_files = 0

    print("\n" + "=" * 60)
    print("STARTING BHAVCOPY ETL")
    print("=" * 60)

    for file in tqdm(files, desc="Loading Bhavcopy"):

        try:

            rows = load_single_file(file)

            if rows == 0:

                skipped_files += 1

            else:

                successful_files += 1

                total_records += rows

        except Exception:

            failed_files += 1

            continue

    print("\n" + "=" * 60)
    print("ETL SUMMARY")
    print("=" * 60)

    print(f"Total Files      : {total_files}")
    print(f"Loaded Files     : {successful_files}")
    print(f"Skipped Files    : {skipped_files}")
    print(f"Failed Files     : {failed_files}")
    print(f"Total Records    : {total_records:,}")

    print("=" * 60)