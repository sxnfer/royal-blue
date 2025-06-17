import logging
import os
from typing import Literal

from psycopg import Connection, Error, connect
from psycopg.rows import DictRow, dict_row

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def connect_db(db_source: Literal["TOTESYS", "DATAWAREHOUSE"]) -> Connection[DictRow]:
    """
    Connect to the TOTESYS or DATAWAREHOUSE database using environment variables.

    Args:
        db_source: Either "TOTESYS" or "DATAWAREHOUSE".

    Returns:
        A psycopg connection with rows returned as dictionaries.

    Raises:
        ValueError: If db_source is not valid.
        Error: If a database error occurs.
        Exception: For any other error.
    """
    if db_source not in ["TOTESYS", "DATAWAREHOUSE"]:
        raise ValueError(
            "db_source invalid, must be either 'TOTESYS' or 'DATAWAREHOUSE'"
        )

    user = os.getenv(f"{db_source}_DB_USER")
    password = os.getenv(f"{db_source}_DB_PASSWORD")
    host = os.getenv(f"{db_source}_DB_HOST")
    dbname = os.getenv(f"{db_source}_DB_DATABASE")
    port = os.getenv(f"{db_source}_DB_PORT")

    try:
        conn: Connection[DictRow] = connect(
            f"user={user} password={password} host={host} dbname={dbname} port={int(port or 0000)}",
            row_factory=dict_row,  # type: ignore
        )

        return conn
    except Error as error:
        logger.error(error)
        raise error
    except Exception as error:
        logger.error(error)
        raise error
