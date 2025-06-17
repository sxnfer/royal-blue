import logging
from datetime import datetime
from typing import List

from psycopg import Connection, sql
from psycopg.rows import DictRow

from src.utils.db.error_map import ERROR_MAP

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def filter_out_values(values: List[str], values_to_filter: List[str]) -> List[str]:
    """
    Remove specific values from a list.

    Args:
        values: Original list of strings.
        values_to_filter: Strings to remove from the list.

    Returns:
        A new list with the filtered values removed.

    Raises:
        None
    """
    filtered = [value for value in values if value not in values_to_filter]
    return filtered


def get_totesys_table_names(
    conn: Connection[DictRow],
    table_names_to_filter_out: List[str] = ["_prisma_migrations"],
) -> List[str]:
    """
    Get all public table names from the Totesys database, excluding specified ones.

    Args:
        conn: A PostgreSQL connection object.
        table_names_to_filter_out: Tables to exclude from the results. Defaults to ['_prisma_migrations'].

    Returns:
        A list of table names not filtered out.

    Raises:
        psycopg.Error: If there's a database error.
        Exception: For any unexpected errors.
    """

    query = """
        SELECT table_name
          FROM information_schema.tables
         WHERE table_schema = 'public'
    """

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            response = cursor.fetchall()

            logger.debug(response)

            totesys_table_names = [
                item["table_name"]
                for item in response
                # filter out tables that should not be
                if item["table_name"] not in table_names_to_filter_out
            ]

        return totesys_table_names

    except Exception as e:
        return handle_db_exception(e)  # type: ignore


def get_table_last_updated_timestamp(
    conn: Connection[DictRow], table_name: str
) -> dict:
    """
    Get the latest 'last_updated' timestamp from a given table.

    Args:
        conn: A PostgreSQL connection object.
        table_name: The name of the table to query.

    Returns:
        A dict with:
            - 'success': If data was found.
            - 'error': If no data or a query failure occurred.

    Raises:
        psycopg.Error: If there's a database error.
        Exception: For any unexpected errors.
    """
    try:
        query = sql.SQL(
            "SELECT MAX(last_updated) as last_updated FROM public.{}"
        ).format(sql.Identifier(table_name))

        with conn.cursor() as cursor:
            cursor.execute(query)
            response = cursor.fetchone()

        if response and response["last_updated"] is not None:
            return {
                "success": {
                    "data": {
                        "table_name": table_name,
                        "last_updated": response["last_updated"],
                    }
                }
            }

        return {"error": {"message": "invalid database response"}}

    except Exception as e:
        return handle_db_exception(e)


def get_table_data(
    conn: Connection[DictRow], table_name: str, last_updated: datetime | None = None
) -> List[DictRow]:
    """
    Get all rows from a table, optionally filtered by last_updated.

    Args:
        conn: A database connection.
        table_name: The table to query.
        last_updated: Filter for rows updated after this datetime.

    Returns:
        A list of row dictionaries.

    Raises:
        psycopg.Error: On database errors.
        Exception: On other errors.
    """

    query = sql.SQL("SELECT * FROM public.{}").format(sql.Identifier(table_name))

    if last_updated:
        query_with_last_updated = sql.SQL("WHERE last_updated > {}").format(
            sql.Literal(last_updated)
        )

        query = query + query_with_last_updated

    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return result


def handle_db_exception(e: Exception) -> dict:
    """
    Format and log a database exception.

    Args:
        e: The exception to handle.

    Returns:
        A dictionary with an error message.

    Raises:
        None
    """
    error_type = type(e).__name__
    error_message = ERROR_MAP.get(type(e), ERROR_MAP[Exception])
    logger.error(f"{error_type}: {error_message} | {str(e)}", exc_info=e)

    return {
        "error": {
            "message": f"{error_type}: {error_message}",
        }
    }


def handle_psycopg_exceptions(e: Exception) -> dict:
    """
    Format and log a psycopg exception.

    Args:
        e: The exception to handle.

    Returns:
        A dictionary with an error message.

    Raises:
        None
    """
    error_type = type(e).__name__
    error_message = ERROR_MAP.get(type(e), ERROR_MAP[Exception])
    logger.error(f"{error_type}: {error_message} | {str(e)}", exc_info=e)
