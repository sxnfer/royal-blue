import pandas as pd


def dim_location_dataframe(**dataframes) -> pd.DataFrame:
    """
    Create a location dimension DataFrame from raw address data.

    Args:
        dataframes: Keyword arguments containing:
            - address: DataFrame with address fields.

    Returns:
        A DataFrame with location dimension columns and renamed 'location_id'.

    Raises:
        ValueError: If 'address' DataFrame is missing or transformation fails.
    """

    required_keys = ["address"]
    for key in required_keys:
        if key not in dataframes:
            raise ValueError(f"Error: Missing required dataframe '{key}'.")

    address_df = dataframes.get("address")
    try:
        dim_location = address_df[
            [
                "address_id",
                "address_line_1",
                "address_line_2",
                "district",
                "city",
                "postal_code",
                "country",
                "phone",
            ]
        ].drop_duplicates()
        dim_location.rename(columns={"address_id": "location_id"}, inplace=True)
        return dim_location

    except Exception as e:
        raise ValueError(f"Error creating dim_location: {e}")
