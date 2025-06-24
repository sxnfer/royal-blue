import pandas as pd
import pytest

from src.utils.dimensions.dim_design_transform import dim_design_dataframe


@pytest.fixture
def mock_design_df():
    return pd.DataFrame(
        {
            "design_id": [1, 25],
            "created_at": ["02/04/2021", "30/05/2024"],
            "design_name": ["Logo", "Motif"],
            "file_location": ["/designs/logos/", "/designs/motifs/"],
            "file_name": ["bratz_logo.png", "barbie_motif.png"],
        }
    )


def test_dim_design_in_DF(mock_design_df):
    df = {"design": mock_design_df}
    result = dim_design_dataframe(**df)

    assert not result.empty
    assert list(result.columns) == [
        "design_id",
        "design_name",
        "file_location",
        "file_name",
    ]
    assert len(result) == 2


def test_dim_design_missing_design_table(mock_design_df):
    with pytest.raises(ValueError, match="Error: Missing required dataframe 'design'."):
        dim_design_dataframe(**{})


def test_dim_design_empty_DF(mock_design_df):
    empty_df = pd.DataFrame(
        columns=["design_id", "design_name", "file_location", "file_name"]
    )
    dfs = {"design": empty_df}

    result = dim_design_dataframe(**dfs)

    assert result.empty
    assert list(result.columns) == [
        "design_id",
        "design_name",
        "file_location",
        "file_name",
    ]


def test_dim_design_duplicates(mock_design_df):
    duplicated_df = pd.concat(
        [mock_design_df, mock_design_df.iloc[[0]]], ignore_index=True
    )
    dfs = {"design": duplicated_df}

    result = dim_design_dataframe(**dfs)

    assert len(result) == 2

    assert result["design_id"].tolist() == [1, 25]


def test_dim_design_bad_columns(mock_design_df):
    bad_df = pd.DataFrame({"design_id": [1], "file_name": ["x.png"]})
    dfs = {"design": bad_df}

    with pytest.raises(ValueError):
        dim_design_dataframe(**dfs)
