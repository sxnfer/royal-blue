import logging
from io import BytesIO

import pandas as pd

from src.utils.custom_errors import InvalidDataFrame

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_parquet_from_data_frame(data_frame: pd.DataFrame) -> BytesIO:
    """
    Converts a valid, non-empty pandas DataFrame to a gzipped Parquet file stored in memory.

    Args:
        data_frame (pd.DataFrame): The DataFrame to convert.

    Returns:
        BytesIO: A memory buffer containing the gzipped Parquet file.

    Raises:
        InvalidDataFrame: If the input is not a DataFrame or is empty.
    """
    if not isinstance(data_frame, pd.DataFrame) or data_frame.empty:
        error = InvalidDataFrame("ERROR: invalid DataFrame")
        logger.error(error)
        raise error

    parquet_file: BytesIO = BytesIO()
    data_frame.to_parquet(parquet_file, engine="pyarrow", compression="gzip")
    parquet_file.seek(0)

    return parquet_file
