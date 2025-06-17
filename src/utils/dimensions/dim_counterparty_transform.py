import pandas as pd


def dim_counterparty_dataframe(**dataframes) -> pd.DataFrame:
    """
    Create a dimension table for counterparties by merging with legal address data.

    Args:
        dataframes: Keyword arguments containing:
            - counterparty: DataFrame with 'counterparty_id', 'counterparty_legal_name', 'legal_address_id'.
            - address: DataFrame with 'address_id' and address fields.

    Returns:
        A transformed DataFrame with counterparty and legal address fields.

    Raises:
        ValueError: If 'counterparty' or 'address' is missing.
        KeyError: If required columns are missing in the 'address' DataFrame.
        Exception: For any other unexpected error.
    """
    required_keys = ["counterparty", "address"]

    for key in required_keys:
        if key not in dataframes:
            raise ValueError(f"Error: Missing required dataframe '{key}'.")

    counterparty_df = dataframes.get("counterparty")
    address_df = dataframes.get("address")

    try:
        renamed_address_df = address_df.rename(
            columns={
                "address_id": "legal_address_id",
                "address_line_1": "counterparty_legal_address_line_1",
                "address_line_2": "counterparty_legal_address_line_2",
                "district": "counterparty_legal_district",
                "city": "counterparty_legal_city",
                "postal_code": "counterparty_legal_postal_code",
                "country": "counterparty_legal_country",
                "phone": "counterparty_legal_phone_number",
            }
        )

        counterparty_address_merged_df = counterparty_df.merge(
            renamed_address_df,
            on="legal_address_id",
        )

        dim_counterparty_df = counterparty_address_merged_df[
            [
                "counterparty_id",
                "counterparty_legal_name",
                "counterparty_legal_address_line_1",
                "counterparty_legal_address_line_2",
                "counterparty_legal_district",
                "counterparty_legal_city",
                "counterparty_legal_postal_code",
                "counterparty_legal_country",
                "counterparty_legal_phone_number",
            ]
        ]

        return dim_counterparty_df
    except Exception as e:
        raise e
