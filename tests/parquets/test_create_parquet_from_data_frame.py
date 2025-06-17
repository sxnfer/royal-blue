import logging
from copy import deepcopy
from io import BytesIO

import pandas as pd
import pytest

from src.utils.custom_errors import InvalidDataFrame
from src.utils.parquets.create_parquet_from_data_frame import (
    create_parquet_from_data_frame,
)


@pytest.mark.describe("create_parquet_from_data_frame Utility Function Behaviour")
class TestCreateParquetFromDataFrame:
    # @pytest.mark.skip
    @pytest.mark.it("check for mutation of DataFrame passed as argument")
    def test_mutation(self, test_data_frame):
        test_data_frame_value_ref = deepcopy(test_data_frame)
        create_parquet_from_data_frame(test_data_frame)

        pd.testing.assert_frame_equal(test_data_frame, test_data_frame_value_ref)

    # @pytest.mark.skip
    @pytest.mark.it("check it returns a parquet file")
    def test_returns_data_in_parquet_format(self, test_data_frame):
        result = create_parquet_from_data_frame(test_data_frame)

        assert isinstance(result, BytesIO)

    # @pytest.mark.skip
    @pytest.mark.it("check generated parquet file contains expected data")
    def test_parquet_has_expected_data(self):
        pass

    # @pytest.mark.skip
    @pytest.mark.it(
        "check should raise an exception if an arugment other than a valid DataFrame is passed"
    )
    def test_invalid_args(self):
        with pytest.raises(InvalidDataFrame, match="ERROR: invalid DataFrame"):
            create_parquet_from_data_frame(1500)  # type: ignore

    # @pytest.mark.skip
    @pytest.mark.it(
        "check that it returns an exception if an empty DataFrame is passed"
    )
    def test_empty_data_frame(self):
        empty_data_frame = pd.DataFrame()
        with pytest.raises(InvalidDataFrame, match="ERROR: invalid DataFrame"):
            create_parquet_from_data_frame(empty_data_frame)

    # @pytest.mark.skip
    @pytest.mark.it("check that InvalidDataFrame exceptions get logged")
    def test_(self, caplog):
        empty_data_frame = pd.DataFrame()
        error_message = "ERROR: invalid DataFrame"
        with caplog.at_level(logging.ERROR):
            with pytest.raises(InvalidDataFrame, match=error_message):
                create_parquet_from_data_frame(empty_data_frame)

        logged_record = caplog.records[0]
        assert logged_record.levelname == "ERROR"
        assert error_message in logged_record.message
