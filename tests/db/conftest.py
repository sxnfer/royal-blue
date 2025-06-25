import os
from typing import Any, Iterator, List
from unittest.mock import MagicMock, Mock, patch

import pytest
from psycopg import Connection, connect, conninfo, sql
from psycopg.rows import DictRow, dict_row
from pytest_postgresql.executor import PostgreSQLExecutor
from pytest_postgresql.janitor import DatabaseJanitor

from sql.create_totesys_tables_query import (
    create_totesys_tables_query,
)
from sql.seed_data.totesys_seed_data import totesys_seed_data


@pytest.fixture(scope="function")
def patched_envs(monkeypatch):
    monkeypatch.setenv("TOTESYS_DB_USER", "user")
    monkeypatch.setenv("TOTESYS_DB_PASSWORD", "pass")
    monkeypatch.setenv("TOTESYS_DB_HOST", "localhost")
    monkeypatch.setenv("TOTESYS_DB_DATABASE", "testdb")
    monkeypatch.setenv("TOTESYS_DB_PORT", "5432")


@pytest.fixture(scope="function")
def patched_envs_error(monkeypatch):
    monkeypatch.setenv("TOTESYS_DB_USER", "invalid")
    monkeypatch.setenv("TOTESYS_DB_PASSWORD", "pass")
    monkeypatch.setenv("TOTESYS_DB_HOST", "invalid_host")
    monkeypatch.setenv("TOTESYS_DB_DATABASE", "testdb")
    monkeypatch.setenv("TOTESYS_DB_PORT", "5432")


@pytest.fixture(scope="function")
def connection_info(patched_envs):
    user = os.getenv("TOTESYS_DB_USER")
    password = os.getenv("TOTESYS_DB_PASSWORD")
    host = os.getenv("TOTESYS_DB_HOST")
    dbname = os.getenv("TOTESYS_DB_DATABASE")
    port = os.getenv("TOTESYS_DB_PORT")

    return f"user={user} password={password} host={host} dbname={dbname} port={int(port or 0000)}"


@pytest.fixture(scope="function")
def mock_cursor(patched_envs):
    cursor = Mock()
    cursor.execute.return_value = None
    cursor.fetchall.return_value = []
    cursor.fetchone.return_value = None
    yield cursor


@pytest.fixture(scope="function")
def mock_cursor_context_manager(mock_cursor):
    cursor_context_manager = MagicMock()
    cursor_context_manager.__enter__.return_value = mock_cursor
    cursor_context_manager.__exit__.return_value = None
    yield cursor_context_manager


@pytest.fixture(scope="function")
def mock_connect(
    connection_info,
    mock_cursor_context_manager,
):
    connection = MagicMock(spec=Connection)
    connection.closed = False
    connection.close.return_value = None
    connection.cursor.return_value = mock_cursor_context_manager

    def close_side_effect():
        connection.closed = True
        connection.cursor.side_effect = Exception("Connection is closed")

    connection.close.side_effect = close_side_effect

    connection.__enter__ = Mock(return_value=connection)
    connection.__exit__ = Mock(return_value=None)

    yield connection


@pytest.fixture(scope="function")
def patched_connect(mock_connect):
    with patch(
        "src.utils.db.connection.connect", return_value=mock_connect
    ) as mock_patch:
        yield mock_patch


@pytest.fixture(scope="function")
def totesys_seeded_conn(
    postgresql_proc: PostgreSQLExecutor,
) -> Iterator[Connection[DictRow]]:
    dbname = "my_test_database"
    user = postgresql_proc.user
    password = "secret_password"
    host = postgresql_proc.host
    port = postgresql_proc.port
    version = postgresql_proc.version

    connection_info = conninfo.make_conninfo(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
    )

    with DatabaseJanitor(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
        version=version,
    ):
        conn: Connection[DictRow] = connect(connection_info, row_factory=dict_row)  # type: ignore
        with conn.cursor() as cursor:
            cursor.execute(create_totesys_tables_query)

            for data in totesys_seed_data:
                table_name = data["table_name"]

                seed_data: List[dict[str, Any]] = data["seed_data"]
                columns = list(seed_data[0].keys())
                values_to_insert = [tuple(row.values()) for row in seed_data]

                insert_query = sql.SQL("""
                    INSERT INTO {table_name} ({columns})
                    VALUES ({values})
                """).format(
                    table_name=sql.Identifier(table_name),
                    columns=sql.SQL(",").join(map(sql.Identifier, columns)),
                    values=sql.SQL(",").join(sql.Placeholder() * len(columns)),
                )
                cursor.executemany(insert_query, values_to_insert)
            conn.commit()
        print("conn.closed", conn.closed)
        print("conn.connection", conn.connection)
        yield conn
