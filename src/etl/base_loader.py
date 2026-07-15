"""
Base ETL Loader

Reusable loader for batch inserting DataFrames into MariaDB.
"""

from sqlalchemy import text


class BaseLoader:

    def __init__(self, engine):
        self.engine = engine

    def batch_insert(
        self,
        dataframe,
        insert_sql,
        batch_size=5000
    ):
        """
        Insert DataFrame into database using batch execution.

        Parameters
        ----------
        dataframe : pandas.DataFrame
        insert_sql : str
        batch_size : int
        """

        records = dataframe.to_dict("records")

        query = text(insert_sql)

        total_records = len(records)

        print(f"Loading {total_records:,} records...")

        with self.engine.begin() as conn:

            for start in range(0, total_records, batch_size):

                end = min(start + batch_size, total_records)

                batch = records[start:end]

                conn.execute(query, batch)

        print(f"Successfully loaded {total_records:,} records.")