import pandas as pd
import pytest

from src.utils.dimensions.dim_staff_transform import dim_staff_dataframe


@pytest.fixture
def valid_dataframes():
    staff_df = pd.DataFrame(
        {
            "staff_id": [1],
            "first_name": ["John"],
            "last_name": ["Doe"],
            "department_id": [100],
            "email_address": ["john.doe@example.com"],
        }
    )

    department_df = pd.DataFrame(
        {
            "department_id": [100],
            "department_name": ["Engineering"],
            "location": ["Building A"],
        }
    )

    return {"staff": staff_df, "department": department_df}


@pytest.mark.it("test dim_staff_dataframe")
class TestDimStaffDataframe:
    @pytest.mark.it("check should test that column names match OLAP data")
    def test_columns(self, valid_dataframes):
        result = dim_staff_dataframe(**valid_dataframes)
        expected = {
            "staff_id",
            "first_name",
            "last_name",
            "department_name",
            "location",
            "email_address",
        }

        assert set(result.columns) == expected

    @pytest.mark.it("check should return correct values after merging")
    def test_values_and_merge(self, valid_dataframes):
        result = dim_staff_dataframe(**valid_dataframes)

        assert result.shape == (1, 6)
        row = result.iloc[0]

        assert row["staff_id"] == 1
        assert row["first_name"] == "John"
        assert row["last_name"] == "Doe"
        assert row["department_name"] == "Engineering"
        assert row["location"] == "Building A"
        assert row["email_address"] == "john.doe@example.com"

    @pytest.mark.it("check .drop_duplicates() removes duplicate rows")
    def test_drop_duplicates_effect(self):
        staff_df = pd.DataFrame(
            {
                "staff_id": [1, 1],
                "first_name": ["John", "John"],
                "last_name": ["Doe", "Doe"],
                "department_id": [100, 100],
                "email_address": ["john.doe@example.com", "john.doe@example.com"],
            }
        )
        department_df = pd.DataFrame(
            {
                "department_id": [100],
                "department_name": ["Engineering"],
                "location": ["Building A"],
            }
        )
        data = {"staff": staff_df, "department": department_df}
        result = dim_staff_dataframe(**data)
        # Should only have one unique row after drop_duplicates
        assert result.shape[0] == 1

    @pytest.mark.it("check left join behavior with unmatched department_id")
    def test_left_join_with_no_matching_department(self):
        staff_df = pd.DataFrame(
            {
                "staff_id": [1, 2],
                "first_name": ["John", "Jane"],
                "last_name": ["Doe", "Smith"],
                "department_id": [100, 999],  # 999 does not exist in department_df
                "email_address": ["john.doe@example.com", "jane.smith@example.com"],
            }
        )
        department_df = pd.DataFrame(
            {
                "department_id": [100],
                "department_name": ["Engineering"],
                "location": ["Building A"],
            }
        )
        data = {"staff": staff_df, "department": department_df}
        result = dim_staff_dataframe(**data)
        assert result.shape[0] == 2
        # For unmatched department_id, department_name and location should be NaN
        unmatched_row = result[result["staff_id"] == 2].iloc[0]
        assert pd.isna(unmatched_row["department_name"])
        assert pd.isna(unmatched_row["location"])

    @pytest.mark.it("check should raise ValueError when staff table is missing")
    def test_missing_staff(self):
        data = {"department": pd.DataFrame()}
        with pytest.raises(
            ValueError, match="Error: Missing required dataframe 'staff'."
        ):
            dim_staff_dataframe(**data)

    @pytest.mark.it("check should raise ValueError when department table is missing")
    def test_missing_department(self):
        data = {"staff": pd.DataFrame()}
        with pytest.raises(
            ValueError, match="Error: Missing required dataframe 'department'."
        ):
            dim_staff_dataframe(**data)

    @pytest.mark.it(
        "check should raise KeyError when required department column is missing"
    )
    def test_missing_department_column(self):
        staff_df = pd.DataFrame(
            {
                "staff_id": [1],
                "first_name": ["John"],
                "last_name": ["Doe"],
                "department_id": [100],
                "email_address": ["john.doe@example.com"],
            }
        )

        department_df = pd.DataFrame(
            {
                "department_id": [100],
                # "department_name" intentionally missing
                "location": ["Building A"],
            }
        )

        data = {"staff": staff_df, "department": department_df}

        with pytest.raises(KeyError):
            dim_staff_dataframe(**data)

    @pytest.mark.it("check should catch generic exceptions and raise them")
    def test_generic_exception(self, valid_dataframes, monkeypatch):
        # monkeypatch merge to throw generic Exception
        def raise_exception(*args, **kwargs):
            raise Exception("Unexpected error")

        monkeypatch.setattr(valid_dataframes["staff"], "merge", raise_exception)
        with pytest.raises(
            Exception, match="Error creating dim_staff: Unexpected error"
        ):
            dim_staff_dataframe(**valid_dataframes)
