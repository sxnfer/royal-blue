import logging
from copy import copy
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from psycopg import Connection, errors

from src.utils.db.connection import connect_db
from src.utils.db.db_helpers import (
    filter_out_values,
    get_table_data,
    get_table_last_updated_timestamp,
    get_totesys_table_names,
)
from src.utils.db.error_map import ERROR_MAP


@pytest.mark.describe("Test filter_out_values")
class TestFilterOutValues:
    @pytest.mark.it("check for purity")
    def test_purity(self):
        test_table_names = ["a", "b", "c"]
        test_filtered_names = ["b"]

        result = filter_out_values(test_table_names, test_filtered_names)

        assert result is not test_table_names
        assert result is not test_filtered_names

    @pytest.mark.it("check for argument mutation")
    def test_(self):
        test_table_names = ["a", "b", "c"]
        test_filtered_names = ["b"]
        test_table_names_value_ref = copy(test_table_names)
        test_filtered_names_value_ref = copy(test_filtered_names)

        filter_out_values(test_table_names, test_filtered_names)

        assert test_table_names == test_table_names_value_ref
        assert test_filtered_names == test_filtered_names_value_ref

    @pytest.mark.it("check that if passed an empty list it returns an empty list")
    def test_empty_list(self):
        test_table_names = []
        test_filtered_names = []

        result = filter_out_values(test_table_names, test_filtered_names)
        assert result == []

    @pytest.mark.it(
        "check that if passed a list with no filterable values, no values are filtered"
    )
    def test_no_values_to_filter(self):
        test_table_names = ["a", "b", "c"]
        test_filtered_names = ["e"]

        result = filter_out_values(test_table_names, test_filtered_names)

        assert result == test_table_names

    @pytest.mark.it("check that it returns a list with filtered names removed")
    def test_remove_filtered(self):
        test_table_names = ["a", "b", "c"]
        test_filtered_names = ["b"]
        expected_result = ["a", "c"]

        result = filter_out_values(test_table_names, test_filtered_names)
        assert result == expected_result


@pytest.mark.describe("Test get_totesys_table_names")
class TestGetTotesysTableNames:
    @pytest.mark.it("check that it returns a list of strings")
    def test_returns_list_str(self, patched_connect):
        conn = connect_db("TOTESYS")

        result = get_totesys_table_names(conn)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, str)

    @pytest.mark.it("check that filtered out names are not in the returned list")
    def test_filtered_values(self, patched_connect):
        conn = connect_db("TOTESYS")
        table_names_to_filter_out = ["_prisma_migrations"]

        result = get_totesys_table_names(conn, table_names_to_filter_out)

        assert (
            list(set(result).difference(table_names_to_filter_out)).sort()
            == result.sort()
        )

    @pytest.mark.it(
        "check handles and logs all mapped psycopg exceptions properly          "
    )
    @pytest.mark.parametrize("error_class", list(ERROR_MAP.keys()))
    def test_get_totesys_table_names_handles_errors(self, error_class, caplog):
        conn = MagicMock(spec=Connection)

        if error_class is Exception:
            conn.cursor.side_effect = Exception("An unexpected error occurred.")
        else:
            conn.cursor.side_effect = error_class("error")

        with caplog.at_level(logging.ERROR):
            result = get_totesys_table_names(conn)

        assert "error" in result
        assert error_class.__name__ in result["error"]["message"]
        assert ERROR_MAP[error_class] in result["error"]["message"]

        error_logs = [
            record.message for record in caplog.records if record.levelname == "ERROR"
        ]
        assert any(ERROR_MAP[error_class] in msg for msg in error_logs), (
            "Expected log message not found"
        )


@pytest.mark.describe("Test get_table_last_updated_timestamp")
class TestGetTableLastUpdatedTimestamp:
    @pytest.mark.it(
        "check that it returns the latest updated timestamp of table currency"
    )
    def test_returns_timestamp(self, patched_connect, mock_cursor):
        mock_cursor.fetchone.return_value = {
            "last_updated": datetime(2025, 5, 1, 12, 30)
        }
        conn = connect_db("TOTESYS")
        table_name = "currency"

        result = get_table_last_updated_timestamp(conn, table_name)

        assert result["success"]["data"]["table_name"] == table_name
        assert isinstance(result["success"]["data"]["last_updated"], datetime)

    @pytest.mark.it(
        "check it returns an error dictionary with UndefinedTable Exception if there are no records to return"
    )
    def test_(self, patched_connect, mock_cursor):
        mock_cursor.fetchone.side_effect = errors.UndefinedTable("ERROR")
        conn = connect_db("TOTESYS")
        table_name = "currency"

        result = get_table_last_updated_timestamp(conn, table_name)

        assert "error" in result
        assert (
            result["error"]["message"]
            == "UndefinedTable: Table does not exist in the database."
        )

    @pytest.mark.it(
        "check it returns an error dictionary if there are no records to return"
    )
    def test_no(self, patched_connect, mock_cursor):
        mock_cursor.fetchone.return_value = {"last_updated": None}
        conn = connect_db("TOTESYS")
        table_name = "currency"

        result = get_table_last_updated_timestamp(conn, table_name)

        assert result.get("error")
        assert result["error"]["message"] == "invalid database response"


@pytest.mark.describe("Test get_table_data (mocked unit tests)")
class TestGetTableDataMocked:
    @pytest.fixture
    def mock_conn_cursor(self):
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        return mock_conn, mock_cursor

    @pytest.mark.it(
        "check that it returns a list of dictionaries with expected keys and values"
    )
    def test_list_of_dict(self, mock_conn_cursor):
        mock_conn, mock_cursor = mock_conn_cursor
        mock_cursor.fetchall.return_value = [
            {
                "currency_id": 1,
                "currency_code": "USD",
                "created_at": datetime(2023, 1, 1, 12, 0),
                "last_updated": datetime(2023, 1, 2, 12, 0),
            },
            {
                "currency_id": 2,
                "currency_code": "EUR",
                "created_at": datetime(2023, 1, 3, 12, 0),
                "last_updated": datetime(2023, 1, 4, 12, 0),
            },
        ]

        result = get_table_data(mock_conn, "currency")

        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, dict)
            assert isinstance(item["currency_id"], int)
            assert isinstance(item["currency_code"], str)
            assert isinstance(item["created_at"], datetime)
            assert isinstance(item["last_updated"], datetime)

    @pytest.mark.it(
        "check that it returns an empty list if there are no matching results in the database (searching for results within a date in the future)"
    )
    def test_empty_list(self, mock_conn_cursor):
        mock_conn, mock_cursor = mock_conn_cursor
        mock_cursor.fetchall.return_value = []

        result = get_table_data(mock_conn, "currency", datetime(2100, 1, 1))

        assert result == []
