from io import BytesIO

import pandas as pd
import pytest

from src.utils.parquets.create_data_frame_from_parquet import (
    create_data_frame_from_parquet,
)


@pytest.fixture
def test_dataframe():
    return pd.DataFrame(
        {
            "name": ["Charley", "San", "Oliver"],
            "favourite_icecream": ["Strawberry", "Chocolate", "Vanilla"],
        }
    )


@pytest.mark.describe("parquet_to_dataframe Utility Function Behaviour")
class TestCreateDataFramesfromParquets:
    @pytest.mark.it("Should return a valid DataFrame from a Parquet bytes")
    def test_returns_data_in_parquet_format(self, test_dataframe):
        test_dataframe = pd.DataFrame(
            {
                "name": ["Charley", "San", "Oliver"],
                "favourite_icecream": ["Strawberry", "Chocolate", "Vanilla"],
            }
        )

        buffer = BytesIO()
        test_dataframe.to_parquet(buffer, index=False)
        test_dataframe_parquet = buffer.getvalue()

        result = create_data_frame_from_parquet(test_dataframe_parquet)

        assert isinstance(result, pd.DataFrame)
        pd.testing.assert_frame_equal(result, test_dataframe)

    @pytest.mark.it(
        "Should raise an exception when invalid parquet bytes are passed into function"
    )
    def test_raises_exception_when_invalid_parquet(self):
        invalid_test_dataframe = "hello"

        with pytest.raises(Exception) as e:
            create_data_frame_from_parquet(invalid_test_dataframe)

        assert isinstance(e.value, Exception)
        assert str(e.value)

    @pytest.mark.it(
        "Should raise an exception when an empty parquet is passed into function"
    )
    def test_raises_exception_when_empty_parquet(self):
        empty_test_dataframe = b""

        with pytest.raises(Exception) as e:
            create_data_frame_from_parquet(empty_test_dataframe)

        assert isinstance(e.value, Exception)
        assert str(e.value)
