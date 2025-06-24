from io import BytesIO
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils.transform_lambda_utils.extract_dataframe_from_event import (
    get_dataframes_from_event,
)


@pytest.fixture
def test_mock_event():
    return [
        {
            "table_name": "users",
            "extraction_timestamp": "2025-06-01T12:00:00Z",
            "last_updated": "2025-05-31T23:59:00Z",
            "file_name": "users.parquet",
            "key": "raw/users/2025-06-01/users.parquet",
        }
    ]


@pytest.fixture
def test_dataframe():
    return pd.DataFrame(
        {
            "name": ["Charley", "San", "Oliver"],
            "favourite_food": [
                "Fish and chips",
                "Jacket potato",
                "Spaghetti bolognese",
            ],
            "favourite_ice_cream": ["Strawberry", "Chocolate", "Vanilla"],
            "likes_spice": [True, False, True],
            "eats_out_per_week": [2, 0, 3],
        }
    )


@pytest.mark.describe("get_dataframes_from_event Utility Function Behaviour")
class TestExtractDataFramesFromEvent:
    @pytest.mark.it(
        "Should return a valid dictionary of DataFrames from a valid S3 event"
    )
    def test_returns_dataframe_dict_from_valid_event(
        self, test_dataframe, test_mock_event
    ):
        buffer = BytesIO()
        test_dataframe.to_parquet(buffer, index=False)
        parquet_bytes = buffer.getvalue()

        with patch(
            "src.utils.transform_lambda_utils.extract_dataframe_from_event.get_file_from_s3_bucket"
        ) as mock_get_file_from_s3:
            mock_get_file_from_s3.return_value = {"success": {"data": parquet_bytes}}

            result = get_dataframes_from_event(client=None, event=test_mock_event)

            assert isinstance(result, dict)
            assert "users" in result
            pd.testing.assert_frame_equal(result["users"], test_dataframe)

    @pytest.mark.it("Should process multiple tables")
    def test_processes_all_tables_in_event_list(self, test_dataframe):
        event = [
            {
                "table_name": "users",
                "extraction_timestamp": "2025-06-01T12:00:00Z",
                "last_updated": "2025-05-31T23:59:00Z",
                "file_name": "users.parquet",
                "key": "raw/users/2025-06-01/users.parquet",
            },
            {
                "table_name": "orders",
                "extraction_timestamp": "2025-06-01T12:00:00Z",
                "last_updated": "2025-05-31T23:59:00Z",
                "file_name": "orders.parquet",
                "key": "raw/orders/2025-06-01/orders.parquet",
            },
        ]

        buffer = BytesIO()
        test_dataframe.to_parquet(buffer, index=False)
        parquet_bytes = buffer.getvalue()

        with patch(
            "src.utils.transform_lambda_utils.extract_dataframe_from_event.get_file_from_s3_bucket"
        ) as mock_get_file_from_s3:
            mock_get_file_from_s3.return_value = {"success": {"data": parquet_bytes}}

            result = get_dataframes_from_event(client=None, event=event)

            assert isinstance(result, dict)
            for key in ["users", "orders"]:
                assert key in result
            pd.testing.assert_frame_equal(result["users"], test_dataframe)
            pd.testing.assert_frame_equal(result["orders"], test_dataframe)

    @pytest.mark.it("Should raise an exception if the Parquet data is invalid")
    def test_raises_exception_on_invalid_parquet_data(self, test_mock_event):
        with patch(
            "src.utils.transform_lambda_utils.extract_dataframe_from_event.get_file_from_s3_bucket"
        ) as mock_get_file_from_s3:
            mock_get_file_from_s3.return_value = {
                "success": {"data": b"not-a-parquet-file"}
            }

            with pytest.raises(Exception, match="Error processing table 'users'"):
                get_dataframes_from_event(client=None, event=test_mock_event)

    @pytest.mark.it("Should raise an exception if the Parquet file is empty")
    def test_raises_exception_on_empty_parquet_file(self, test_mock_event):
        with patch(
            "src.utils.transform_lambda_utils.extract_dataframe_from_event.get_file_from_s3_bucket"
        ) as mock_get_file_from_s3:
            mock_get_file_from_s3.return_value = {"success": {"data": b""}}

            with pytest.raises(Exception, match="Error processing table 'users'"):
                get_dataframes_from_event(client=None, event=test_mock_event)

    @pytest.mark.it("Should raise an exception if required fields are missing")
    def test_raises_exception_on_missing_event_fields(self):
        broken_event = [
            {
                "extraction_timestamp": "2025-06-01T12:00:00Z",
                "last_updated": "2025-05-31T23:59:00Z",
                "file_name": "users.parquet",
            }
        ]

        with pytest.raises(KeyError):
            get_dataframes_from_event(client=None, event=broken_event)

    @pytest.mark.it("Should raise an exception if S3 returns an error response")
    def test_raises_exception_on_s3_error_response(self, test_mock_event):
        with patch(
            "src.utils.transform_lambda_utils.extract_dataframe_from_event.get_file_from_s3_bucket"
        ) as mock_get_file_from_s3:
            mock_get_file_from_s3.return_value = {
                "error": {"message": "File not found"}
            }

            with pytest.raises(Exception, match="File not found"):
                get_dataframes_from_event(client=None, event=test_mock_event)
