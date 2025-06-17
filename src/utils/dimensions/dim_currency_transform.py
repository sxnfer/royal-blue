import pandas as pd


def dim_currency_dataframe(**dataframes) -> pd.DataFrame:
    """
    Create a currency dimension table with currency codes and names.

    Args:
        dataframes: Keyword arguments containing:
            - currency: DataFrame with 'currency_id' and 'currency_code'.

    Returns:
        A DataFrame with 'currency_id', 'currency_code', and 'currency_name'.

    Raises:
        ValueError: If the 'currency' dataframe is missing.
        KeyError: If required columns are missing from input.
        Exception: For any other unexpected error.
    """
    try:
        currency_lookup = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "AUD": "Australian Dollar",
            "CAD": "Canadian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "NZD": "New Zealand Dollar",
            "SEK": "Swedish Krona",
            "NOK": "Norwegian Krone",
            "MXN": "Mexican Peso",
            "INR": "Indian Rupee",
            "BRL": "Brazilian Real",
            "ZAR": "South African Rand",
            "SGD": "Singapore Dollar",
            "HKD": "Hong Kong Dollar",
            "KRW": "South Korean Won",
            "RUB": "Russian Ruble",
            "TRY": "Turkish Lira",
        }
        required_keys = ["currency"]
        for key in required_keys:
            if key not in dataframes:
                raise ValueError(f"Error: Missing required dataframe '{key}'.")

        currency_df = dataframes.get("currency")

        lookup_df = (
            pd.DataFrame.from_dict(
                currency_lookup, orient="index", columns=["currency_name"]
            )
            .reset_index()
            .rename(columns={"index": "currency_code"})
        )

        currency_df = currency_df.merge(
            lookup_df[["currency_code", "currency_name"]],
            how="left",
            on="currency_code",
        )

        dim_currency = currency_df[["currency_id", "currency_code", "currency_name"]]
        return dim_currency

    except Exception as e:
        raise e
