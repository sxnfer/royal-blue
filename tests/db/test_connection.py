import logging
from unittest.mock import patch

import pytest
from psycopg import Connection, OperationalError
from psycopg.rows import dict_row

from src.utils.db.connection import connect_db


@pytest.mark.describe("Tests connect_db")
class TestConnectDb:
    @pytest.mark.it("check that it returns a Connection object")
    def test_return_value(self, patched_connect):
        conn = connect_db("TOTESYS")
        assert isinstance(conn, Connection)

    @pytest.mark.it("check that it is called once with expected arguments")
    def test_connect_success(self, patched_connect):
        conn = connect_db("TOTESYS")

        assert conn is not None
        patched_connect.assert_called_once_with(
            "user=user password=pass host=localhost dbname=testdb port=5432",
            row_factory=dict_row,
        )

    @pytest.mark.it("check that the DB connection is open")
    def test_connection_open(self, patched_connect):
        conn = connect_db("TOTESYS")
        assert not conn.closed

    @pytest.mark.it("check that it raises an exception when connection fails")
    def test_connect_db_exception(self, patched_envs):
        error_message = "Connection failed"
        with patch(
            "src.utils.db.connection.connect", side_effect=Exception(error_message)
        ):
            with pytest.raises(Exception, match=error_message):
                connect_db("TOTESYS")

    @pytest.mark.it(
        "check that it raises OperationalError upon entering wrong DB credentials"
    )
    def test_raises_operational_error(self, patched_envs_error):
        with pytest.raises(OperationalError) as error:
            connect_db("TOTESYS")
        assert "name resolution" in str(error.value) or "nodename" in str(error.value)

    @pytest.mark.it("check that if it raises exceptions, they are logged by logger")
    def test_logs_errors(self, patched_envs, caplog):
        error_massage = "Connection failed"
        with patch(
            "src.utils.db.connection.connect", side_effect=Exception(error_massage)
        ):
            with caplog.at_level(logging.ERROR):
                with pytest.raises(Exception):
                    connect_db("TOTESYS")

            logged_record = caplog.records[0]
            assert logged_record.levelname == "ERROR"
            assert error_massage in logged_record.message
