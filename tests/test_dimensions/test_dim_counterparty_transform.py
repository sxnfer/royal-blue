import pandas as pd
import pytest

from src.utils.dimensions.dim_counterparty_transform import (
    dim_counterparty_dataframe,
)


@pytest.fixture
def valid_dataframes():
    counterparty_df = pd.DataFrame({
        "counterparty_id": [1],
        "counterparty_legal_name": ["ABC Corp"],
        "legal_address_id": [10],
    })

    address_df = pd.DataFrame({
        "legal_address_id": [10],
        "address_line_1": ["123 Main St"],
        "address_line_2": ["Suite 100"],
        "district": ["District A"],
        "city": ["Metropolis"],
        "postal_code": ["12345"],
        "country": ["USA"],
        "phone": ["555-1234"],
    })

    return {"counterparty": counterparty_df, "address": address_df}


@pytest.mark.it("test dim_counterparty_dataframe")
class TestDimCounterpartyDataframe:
    @pytest.mark.it("check should test that column names match OLAP data")
    def test_columns(self, valid_dataframes):
        result = dim_counterparty_dataframe(**valid_dataframes)
        expected = {
            "counterparty_id",
            "counterparty_legal_name",
            "counterparty_legal_address_line_1",
            "counterparty_legal_address_line_2",
            "counterparty_legal_district",
            "counterparty_legal_city",
            "counterparty_legal_postal_code",
            "counterparty_legal_country",
            "counterparty_legal_phone_number",
        }

        assert set(result.columns) == expected

    @pytest.mark.it("check should return correct values after merging and renaming")
    def test_values_and_merge(self, valid_dataframes):
        result = dim_counterparty_dataframe(**valid_dataframes)

        assert result.shape == (1, 9)
        row = result.iloc[0]

        assert row["counterparty_id"] == 1
        assert row["counterparty_legal_name"] == "ABC Corp"
        assert row["counterparty_legal_address_line_1"] == "123 Main St"
        assert row["counterparty_legal_address_line_2"] == "Suite 100"
        assert row["counterparty_legal_district"] == "District A"
        assert row["counterparty_legal_city"] == "Metropolis"
        assert row["counterparty_legal_postal_code"] == "12345"
        assert row["counterparty_legal_country"] == "USA"
        assert row["counterparty_legal_phone_number"] == "555-1234"

    @pytest.mark.it("check should raise ValueError when counterparty table is missing")
    def test_missing_counterparty(self):
        data = {"address": pd.DataFrame()}
        with pytest.raises(
            ValueError, match="Error: Missing required dataframe 'counterparty'."
        ):
            dim_counterparty_dataframe(**data)

    @pytest.mark.it("check should raise ValueError when address table is missing")
    def test_missing_address(self):
        data = {"counterparty": pd.DataFrame()}
        with pytest.raises(
            ValueError, match="Error: Missing required dataframe 'address'."
        ):
            dim_counterparty_dataframe(**data)

    @pytest.mark.it(
        "check should raise KeyError when required address column is missing"
    )
    def test_missing_address_column(self):
        address_df = pd.DataFrame({
            "legal_address_id": [10],
            # 'address_line_1' : intentionally missing
            "address_line_2": ["Suite 100"],
            "district": ["District A"],
            "city": ["Metropolis"],
            "postal_code": ["12345"],
            "country": ["USA"],
            "phone": ["555-1234"],
        })

        counterparty_df = pd.DataFrame({
            "counterparty_id": [1],
            "counterparty_legal_name": ["ABC Corp"],
            "legal_address_id": [10],
        })

        data = {"counterparty": counterparty_df, "address": address_df}

        with pytest.raises(KeyError):
            dim_counterparty_dataframe(**data)
