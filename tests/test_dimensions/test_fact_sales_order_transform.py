import pandas as pd
import pytest

from src.utils.facts.create_fact_sales_order_from_df import (
    create_fact_sales_order_from_df,
)


@pytest.fixture
def mock_sales_order_df():
    return pd.DataFrame(
        {
            "sales_order_id": [1],
            "created_at": ["2025-06-01T10:30:00"],
            "last_updated": ["2025-06-02T15:45:00"],
            "design_id": [101],
            "staff_id": [501],
            "counterparty_id": [301],
            "units_sold": [10],
            "unit_price": [5.99],
            "currency_id": [1],
            "agreed_payment_date": ["2025-06-10"],
            "agreed_delivery_date": ["2025-06-15"],
        }
    )


@pytest.mark.describe("fact_sales_order_dataframe Transformation Function")
class TestFactSalesOrder:
    @pytest.mark.it(
        "Should return a DataFrame with the required columns when input is valid"
    )
    def test_fact_sales_order_success(self, mock_sales_order_df):
        result = create_fact_sales_order_from_df(mock_sales_order_df)

        expected_columns = [
            "sales_order_id",
            "design_id",
            "sales_staff_id",  # renamed
            "counterparty_id",
            "units_sold",
            "unit_price",
            "currency_id",
            "agreed_payment_date",
            "agreed_delivery_date",
            "created_date",
            "last_updated_date",
            "created_time",
            "last_updated_time",
        ]

        assert not result.empty
        assert len(result) == 1
        for column in expected_columns:
            assert column in result.columns

    @pytest.mark.it("Should correctly parse date and time fields")
    def test_fact_sales_order_date_time_parsing(self, mock_sales_order_df):
        result = create_fact_sales_order_from_df(mock_sales_order_df)

        assert result["created_date"].iloc[0].isoformat() == "2025-06-01"
        assert result["last_updated_date"].iloc[0].isoformat() == "2025-06-02"

        assert result["created_time"].iloc[0].hour == 10
        assert result["created_time"].iloc[0].minute == 30

        assert result["last_updated_time"].iloc[0].hour == 15
        assert result["last_updated_time"].iloc[0].minute == 45

    @pytest.mark.it("Should rename 'staff_id' to 'sales_staff_id'")
    def test_fact_sales_order_column_rename(self, mock_sales_order_df):
        result = create_fact_sales_order_from_df(mock_sales_order_df)

        assert "sales_staff_id" in result.columns
        assert "staff_id" not in result.columns

    @pytest.mark.it("Should drop 'created_at' and 'last_updated'")
    def test_fact_sales_order_drop_original_datetime(self, mock_sales_order_df):
        result = create_fact_sales_order_from_df(mock_sales_order_df)

        assert "created_at" not in result.columns
        assert "last_updated" not in result.columns

    @pytest.mark.it("Should handle multiple rows correctly")
    def test_fact_sales_order_multiple_rows(self, mock_sales_order_df):
        df = pd.concat([mock_sales_order_df] * 3, ignore_index=True)
        result = create_fact_sales_order_from_df(df)

        assert len(result) == 3
        assert all(result["created_date"] == pd.to_datetime("2025-06-01").date())

    @pytest.mark.it("Should raise no error with minimal valid columns")
    def test_fact_sales_order_minimal_required_columns(self):
        minimal_df = pd.DataFrame(
            {
                "created_at": ["2025-01-01T08:00:00"],
                "last_updated": ["2025-01-02T09:00:00"],
                "staff_id": [999],
                "agreed_payment_date": ["2025-01-03"],
                "agreed_delivery_date": ["2025-01-04"],
            }
        )

        result = create_fact_sales_order_from_df(minimal_df)

        assert "sales_staff_id" in result.columns
        assert result["created_date"].iloc[0].isoformat() == "2025-01-01"
