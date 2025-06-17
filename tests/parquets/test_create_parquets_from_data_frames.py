from io import BytesIO
from unittest.mock import Mock

import pandas as pd
import pytest

from src.utils.parquets.create_parquets_from_data_frames import (
    create_parquets_from_data_frames,
)


@pytest.mark.describe("create_parquets_from_data_frames Utility Function Behaviour")
class TestCreateParquetsFromDataFrames:
    @pytest.mark.it("check should return 'parquet_file' values as Parquet file buffers")
    def test_returns_data_in_parquet_format(self, valid_data_frame_data):
        result = create_parquets_from_data_frames(valid_data_frame_data)

        data = result["success"]["data"]

        assert "success" in result
        assert "Parquet file conversion successful." == result["success"]["message"]

        for item in data:
            assert isinstance(item["parquet_file"], BytesIO)

    @pytest.mark.it("check should return a list of the same length as the input list")
    def test_returns_same_number_of_files(self, valid_data_frame_data):
        result = create_parquets_from_data_frames(valid_data_frame_data)

        assert len(result["success"]["data"]) == len(valid_data_frame_data)

    @pytest.mark.it(
        "check should preserve 'table_name' and 'last_updated' values in the returned output"
    )
    def test_preserves_data(self, valid_data_frame_data):
        result = create_parquets_from_data_frames(valid_data_frame_data)
        data = result["success"]["data"]
        for i in range(len(valid_data_frame_data)):
            assert data[i]["table_name"] == valid_data_frame_data[i]["table_name"]
            assert data[i]["last_updated"] == valid_data_frame_data[i]["last_updated"]

    @pytest.mark.it(
        "check should return an error if the data_frame is not a valid DataFrame"
    )
    def test_invalid_dataframe_raises_error(self):
        broken_data = [
            {
                "table_name": "bad_table",
                "last_updated": "2025-01-01",
                "data_frame": {
                    "country": ["Lancashire", "Greater Manchester"],
                    "city": ["Preston", "Manchester"],
                    "road": ["Victoria", "Oxford Road"],
                },
            }
        ]
        result = create_parquets_from_data_frames(broken_data)

        assert "error" in result
        assert result["error"]["message"] == "bad_table: invalid data type."

    @pytest.mark.it(
        "Should return an error if an unexpected exception is raised during conversion"
    )
    def test_unexpected_exception_raised(self):
        mock_df = Mock(spec=pd.DataFrame)
        mock_df.to_parquet.side_effect = Exception("Failed Conversion")

        data = [
            {
                "table_name": "failed_table",
                "last_updated": "2025-01-01",
                "data_frame": mock_df,
            }
        ]

        result = create_parquets_from_data_frames(data)

        assert "error" in result
        assert result["error"]["message"] == "failed_table: Failed Conversion"
