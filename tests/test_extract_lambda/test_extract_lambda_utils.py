from copy import deepcopy
from datetime import datetime

import pandas as pd
import pytest

from src.utils.custom_errors import InvalidEmptyList
from src.utils.extract_lambda_utils import (
    create_data_frame_from_list,
    create_parquet_metadata,
    get_last_updated_from_raw_table_data,
)


@pytest.mark.describe("Test create_data_frame_from_list")
class TestCreateDataFramFromList:
    # @pytest.mark.skip
    @pytest.mark.it(
        "check for purity, making sure it returns a different object than the one passed as argument"
    )
    def test_purity(self, test_table_data_list):
        result = create_data_frame_from_list(test_table_data_list)
        assert result is not test_table_data_list

    # @pytest.mark.skip
    @pytest.mark.it("check for mutation")
    def test_mutation(self):
        test_table_data = [
            {
                "currency_id": 1,
                "currency_code": "usd",
                "last_updated": datetime(2025, 5, 5, 5, 5, 5, 5),
            }
        ]
        test_table_data_value_ref = deepcopy(test_table_data)

        create_data_frame_from_list(test_table_data)
        assert test_table_data == test_table_data_value_ref

    # @pytest.mark.skip
    @pytest.mark.it("check that it raises an Exception if an empty list is passed")
    def test_empty_list(self):
        test_list = []
        with pytest.raises(InvalidEmptyList):
            create_data_frame_from_list(test_list)

    # @pytest.mark.skip
    @pytest.mark.it(
        "check that it returns a dataframe if passed a list of dictionaries"
    )
    def test_success(self):
        last_updated = datetime(2025, 5, 5, 5, 5, 5, 5)

        test_table_data = [
            {
                "currency_id": 1,
                "currency_code": "usd",
                "last_updated": last_updated,
            }
        ]

        result = create_data_frame_from_list(test_table_data)
        assert isinstance(result, pd.DataFrame)

    # @pytest.mark.skip
    @pytest.mark.it("check that if passed a non iterable value it raises an exception")
    def test_(self):
        test_data = 100
        with pytest.raises(Exception):
            create_data_frame_from_list(test_data)  # type: ignore

    # @pytest.mark.skip
    @pytest.mark.it(
        "check that the dataframe has as many entries as the list passed to it"
    )
    def test_len_dataframe(self):
        test_table_data = [
            {
                "currency_id": 1,
                "currency_code": "usd",
                "last_updated": datetime(2025, 5, 5, 5, 5, 5, 5),
            },
            {
                "currency_id": 2,
                "currency_code": "eur",
                "last_updated": datetime(2025, 5, 5, 5, 0, 0, 0),
            },
        ]

        result = create_data_frame_from_list(test_table_data)
        assert len(result) == len(test_table_data)


@pytest.mark.describe("Test get_last_updated_from_raw_table_data")
class TestGetLastUpdatedFromRawTableData:
    # @pytest.mark.skip
    @pytest.mark.it("check it does not mutate list")
    def test_mutation(self):
        test_table_data = [
            {
                "currency_id": 1,
                "currency_code": "usd",
                "last_updated": datetime(2025, 5, 5, 5, 5, 5, 5),
            }
        ]
        test_table_data_value_ref = deepcopy(test_table_data)

        get_last_updated_from_raw_table_data(test_table_data)
        assert test_table_data == test_table_data_value_ref

    @pytest.mark.it("check it raises an exception if passed an empty list")
    def test_empty_list(self):
        test_list = []
        with pytest.raises(InvalidEmptyList, match="ERROR: List is empty"):
            get_last_updated_from_raw_table_data(test_list)

    @pytest.mark.it("check it returns a datetime for list of one dictionary")
    def test_datetime_return(self):
        last_updated = datetime(2025, 5, 5, 5, 5, 5, 5)
        test_list = [
            {
                "currency_id": 0,
                "currency_code": "usd",
                "last_updated": last_updated,
            }
        ]

        assert get_last_updated_from_raw_table_data(test_list) == last_updated
        assert isinstance(get_last_updated_from_raw_table_data(test_list), datetime)

    @pytest.mark.it("check it returns the maximum datetime from a list of dictionaries")
    def test_maximum_time(self):
        test_list = [
            {
                "currency_id": 0,
                "currency_code": "usd",
                "last_updated": datetime(2025, 5, 5, 5, 5, 5, 0),
            },
            {
                "currency_id": 1,
                "currency_code": "arg",
                "last_updated": datetime(2025, 5, 5, 5, 5, 5, 3),
            },
            {
                "currency_id": 2,
                "currency_code": "brl",
                "last_updated": datetime(2025, 5, 5, 5, 5, 5, 2),
            },
            {
                "currency_id": 3,
                "currency_code": "eur",
                "last_updated": datetime(2025, 5, 5, 5, 5, 5, 1),
            },
        ]

        assert get_last_updated_from_raw_table_data(test_list) == datetime(
            2025, 5, 5, 5, 5, 5, 3
        )


@pytest.mark.it(
    "Should generate a filename and key from a given datetime and table name."
)
def test_create_parquet_metadata_returns_correct_filename_and_key():
    dt = datetime(2025, 6, 13, 10, 35, 20, 12345)
    table_name = "currency"

    filename, key = create_parquet_metadata(dt, table_name)

    expected_filename_start = "currency_2025-6-13_10-35-20_"
    assert filename.startswith(expected_filename_start)
    assert filename.endswith(".parquet")

    expected_key_start = "2025/6/13/currency_2025-6-13_10-35-20_"
    assert key.startswith(expected_key_start)
    assert key.endswith(".parquet")
    assert key == f"2025/6/13/{filename}"
