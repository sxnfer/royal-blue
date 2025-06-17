import pytest

from src.utils.dimensions.dim_date_transform import (
    dim_date_dataframe,
)


@pytest.fixture
def sample_date_df():
    """
    Build a small dim_date DataFrame covering a couple of days across
    year and month boundaries so we can test each attribute.
    """
    return dim_date_dataframe("2021-12-30", "2022-01-02")


def test_columns_and_length(sample_date_df):
    """
    Ensure the DataFrame has the exact columns in the correct order
    and the expected number of rows for the given date range.
    """
    df = sample_date_df

    assert len(df) == 4

    expected_columns = [
        "date_id",
        "year",
        "month",
        "day",
        "day_of_week",
        "day_name",
        "month_name",
        "quarter",
    ]
    assert list(df.columns) == expected_columns
