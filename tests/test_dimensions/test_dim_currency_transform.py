import pandas as pd
import pytest

from src.utils.dimensions.dim_currency_transform import dim_currency_dataframe


@pytest.fixture
def valid_currency_dataframe():
    return {
        "currency": pd.DataFrame(
            {
                "currency_id": [1, 2, 3],
                "currency_code": ["USD", "EUR", "JPY"],
            }
        )
    }


@pytest.mark.describe("tests the functionality of the currency dimension function")
class TestCurrencyDimensions:
    @pytest.mark.it("should return a DataFrame")
    def test_transform_returns_dataframe(self, valid_currency_dataframe):
        result = dim_currency_dataframe(**valid_currency_dataframe)
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.it("should have correct column names")
    def test_columns(self, valid_currency_dataframe):
        result = dim_currency_dataframe(**valid_currency_dataframe)
        assert list(result.columns) == ["currency_id", "currency_code", "currency_name"]

    @pytest.mark.it("should return correct currency names")
    def test_currency_lookup_merge(self, valid_currency_dataframe):
        result = dim_currency_dataframe(**valid_currency_dataframe)
        expected_names = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "JPY": "Japanese Yen",
        }
        for _, row in result.iterrows():
            assert row["currency_name"] == expected_names[row["currency_code"]]

    @pytest.mark.it("should raise ValueError if 'currency' key is missing")
    def test_missing_currency_key(self):
        with pytest.raises(ValueError) as exc:
            dim_currency_dataframe(some_other_key=pd.DataFrame())
        assert "Missing required dataframe 'currency'" in str(exc.value)

    @pytest.mark.it("should raise a generic exception for other errors")
    def test_generic_exception(self, monkeypatch):
        # Patch pd.DataFrame.merge to raise an error during execution
        def mock_merge(*args, **kwargs):
            raise RuntimeError("Unexpected failure during merge")

        df = pd.DataFrame(
            {
                "currency_id": [1],
                "currency_code": ["USD"],
            }
        )

        monkeypatch.setattr(pd.DataFrame, "merge", mock_merge)

        with pytest.raises(RuntimeError, match="Unexpected failure during merge"):
            dim_currency_dataframe(currency=df)
