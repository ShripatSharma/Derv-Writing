"""
ETL Logger

Maintains ETL audit log for every processed file.
"""

from sqlalchemy import text


class ETLLogger:

    def __init__(self, engine):
        self.engine = engine

    # ==========================================================
    # Check whether file has already been loaded
    # ==========================================================

    def is_file_loaded(
        self,
        table_name,
        file_hash
    ):

        sql = text("""
            SELECT COUNT(*)
            FROM etl_file_log
            WHERE table_name = :table_name
              AND file_hash = :file_hash
              AND status = 'SUCCESS'
        """)

        with self.engine.connect() as conn:

            count = conn.execute(
                sql,
                {
                    "table_name": table_name,
                    "file_hash": file_hash
                }
            ).scalar()

        return count > 0

    # ==========================================================
    # Log File
    # ==========================================================

    def log(
        self,
        file_name,
        file_size,
        file_hash,
        table_name,
        records_loaded,
        status,
        remarks=""
    ):

        sql = text("""

        INSERT INTO etl_file_log
        (
            file_name,
            file_size,
            file_hash,
            table_name,
            records_loaded,
            status,
            remarks
        )

        VALUES
        (
            :file_name,
            :file_size,
            :file_hash,
            :table_name,
            :records_loaded,
            :status,
            :remarks
        )

        ON DUPLICATE KEY UPDATE

            records_loaded = VALUES(records_loaded),
            status = VALUES(status),
            remarks = VALUES(remarks),
            load_timestamp = CURRENT_TIMESTAMP

        """)

        with self.engine.begin() as conn:

            conn.execute(
                sql,
                {
                    "file_name": file_name,
                    "file_size": file_size,
                    "file_hash": file_hash,
                    "table_name": table_name,
                    "records_loaded": records_loaded,
                    "status": status,
                    "remarks": remarks
                }
            ) 