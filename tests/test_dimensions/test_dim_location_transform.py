import pandas as pd
import pytest

from src.utils.dimensions.dim_location_transform import dim_location_dataframe


@pytest.fixture
def mock_address_df():
    return pd.DataFrame(
        {
            "address_id": ["1", "25"],
            "address_line_1": ["123 Lane", "456 Avenue"],
            "address_line_2": ["Suite 4", "Flat 5"],
            "district": ["Central", "North"],
            "city": ["London", "Bristol"],
            "postal_code": ["E1 6AN", "BS1 4TB"],
            "country": ["UK", "UK"],
            "phone": ["0123456789", "0123456774"],
        }
    )


@pytest.mark.describe("dim_location_dataframe Function Behaviour")
class TestDimLocationDataframe:
    @pytest.mark.it("Should return a dataframe with the correct columns")
    def test_dim_address_in_DF(self, mock_address_df):
        test_extracted_dataframes = {"address": mock_address_df}
        result = dim_location_dataframe(**test_extracted_dataframes)

        assert isinstance(result, pd.DataFrame)

        columns = [
            "location_id",
            "address_line_1",
            "address_line_2",
            "district",
            "city",
            "postal_code",
            "country",
            "phone",
        ]
        for title in columns:
            assert title in result.columns

        assert len(result) == 2

    @pytest.mark.it("Should raise ValueError if the address table is missing")
    def test_dim_address_missing_address_table(self):
        with pytest.raises(
            ValueError, match="Error: Missing required dataframe 'address'."
        ):
            dim_location_dataframe(**{})

    @pytest.mark.it("Should return an empty dataframe if the address table is empty")
    def test_dim_address_empty_DF(self):
        test_empty_dataframe = pd.DataFrame(
            columns=[
                "address_id",
                "address_line_1",
                "address_line_2",
                "district",
                "city",
                "postal_code",
                "country",
                "phone",
            ]
        )
        result = dim_location_dataframe(**{"address": test_empty_dataframe})

        assert result.empty

    @pytest.mark.it("Should allow rows with missing vlaues to be included")
    def test_dim_address_partial_address_entry(self, mock_address_df):
        mock_address_df.loc[0, "phone"] = None
        test_extracted_dataframes = {"address": mock_address_df}
        result = dim_location_dataframe(**test_extracted_dataframes)

        assert result.isnull().values.any()

    @pytest.mark.it("Should remove duplicate rows if they exist")
    def test_dim_address_duplicates(self, mock_address_df):
        test_duplicated_df = pd.concat(
            [mock_address_df, mock_address_df], ignore_index=True
        )
        test_extracted_dataframes = {"address": test_duplicated_df}
        result = dim_location_dataframe(**test_extracted_dataframes)

        assert len(result) == 2

    @pytest.mark.it("Should raise an error if a column has the wrong invalid data type")
    def test_dim_address_incorrect_data_type(self, mock_address_df):
        mock_address_df["city"] = [{"a": 1}, {"b": 2}]
        test_extracted_dataframes = {"address": mock_address_df}

        with pytest.raises(ValueError, match="Error creating dim_location"):
            dim_location_dataframe(**test_extracted_dataframes)

    @pytest.mark.it("Should raise an error if a column is missing")
    def test_dim_address_missing_columns(self, mock_address_df):
        mock_address_df.drop(columns=["city"], inplace=True)
        test_extracted_dataframes = {"address": mock_address_df}

        with pytest.raises(ValueError, match="Error creating dim_location"):
            dim_location_dataframe(**test_extracted_dataframes)

    @pytest.mark.it("Should ignore unrelated columns")
    def test_dim_address_unrelated_columns(self, mock_address_df):
        mock_address_df["unrelated_column"] = ["unrelated_1", "unrelated_2"]
        test_extracted_dataframes = {"address": mock_address_df}

        result = dim_location_dataframe(**test_extracted_dataframes)

        assert "unrelated_column" not in result.columns
