import pandas as pd


def dim_date_dataframe(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Generate a date dimension DataFrame with calendar attributes.

    Args:
        start_date: Start date string (e.g., 'YYYY-MM-DD').
        end_date: End date string (e.g., 'YYYY-MM-DD').

    Returns:
        A DataFrame with columns for date_id, year, month, day, day_of_week,
        day_name, month_name, and quarter.

    Raises:
        ValueError: If start_date or end_date are invalid dates.
    """

    all_dates = pd.date_range(
        start=start_date, end=end_date, tz="Europe/London", normalize=True
    )
    date_dataframe = pd.DataFrame({"date_value": all_dates})

    date_dataframe["year"] = date_dataframe["date_value"].dt.year
    date_dataframe["month"] = date_dataframe["date_value"].dt.month
    date_dataframe["day"] = date_dataframe["date_value"].dt.day
    date_dataframe["day_of_week"] = date_dataframe["date_value"].dt.weekday + 1
    date_dataframe["day_name"] = date_dataframe["date_value"].dt.day_name()
    date_dataframe["month_name"] = date_dataframe["date_value"].dt.month_name()
    date_dataframe["quarter"] = date_dataframe["date_value"].dt.quarter
    date_dataframe["date_id"] = date_dataframe["date_value"].dt.date

    date_dataframe = date_dataframe[
        [
            "date_id",
            "year",
            "month",
            "day",
            "day_of_week",
            "day_name",
            "month_name",
            "quarter",
        ]
    ]

    return date_dataframe
