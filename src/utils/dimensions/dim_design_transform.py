import pandas as pd


def dim_design_dataframe(**dataframes) -> pd.DataFrame:
    """
    Create a design dimension DataFrame from raw design data.

    Args:
        dataframes: Keyword arguments containing:
            - design: DataFrame with 'design_id', 'design_name', 'file_location', 'file_name'.

    Returns:
        A DataFrame with design dimension columns, duplicates removed.

    Raises:
        ValueError: If 'design' DataFrame is missing or transformation fails.
    """

    required_keys = ["design"]

    for key in required_keys:
        if key not in dataframes:
            raise ValueError(f"Error: Missing required dataframe '{key}'.")

    design_df = dataframes.get("design")

    try:
        dim_design = design_df[
            ["design_id", "design_name", "file_location", "file_name"]
        ].drop_duplicates()

        return dim_design

    except Exception as e:
        raise ValueError(f"Error creating dim_design: {e}")
