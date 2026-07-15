"""
Validation utilities for ETL pipelines.
"""


def validate_required_columns(df, required_columns):
    """
    Raise an exception if required columns are missing.
    """

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )


def validate_empty_dataframe(df):
    """
    Raise an exception if dataframe is empty.
    """

    if df.empty:
        raise ValueError("Input dataframe is empty.")