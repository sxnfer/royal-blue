from io import BytesIO

import pandas as pd


def create_data_frame_from_parquet(parquet_file) -> pd.DataFrame:
    """
    Converts a Parquet file in bytes into a Pandas DataFrame.

    Args:
    parquet_file (bytes): The contents of a Parquet file as a byte object.

    Returns:
    pd.DataFrame: DataFrame containing the data extracted from the Parquet file.

    Raises:
    ValueError: If the Parquet file cannot be converted into a DataFrame.
    """
    try:
        restored_data_frame = pd.read_parquet(BytesIO(parquet_file))
        return restored_data_frame
    except Exception as e:
        raise ValueError(f"Failed to convert Parquet file to DataFrame: {e}")
