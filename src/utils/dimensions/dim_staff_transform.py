import pandas as pd


def dim_staff_dataframe(**dataframes) -> pd.DataFrame:
    """
    Build the staff dimension table by merging staff data with department details.

    Args:
        dataframes: Keyword arguments containing:
            - staff: DataFrame with 'staff_id', 'first_name', 'last_name', 'department_id', 'email_address'.
            - department: DataFrame with 'department_id', 'department_name', 'location'.

    Returns:
        A DataFrame with staff dimension columns including department name and location.

    Raises:
        ValueError: If required DataFrames are missing.
        KeyError: If expected columns are missing during merge.
        Exception: For other unexpected errors during processing.
    """
    required_keys = ["staff", "department"]

    for key in required_keys:
        if key not in dataframes:
            raise ValueError(f"Error: Missing required dataframe '{key}'.")

    staff_df = dataframes.get("staff")
    departments_df = dataframes.get("department")

    try:
        staff_df = staff_df.merge(
            departments_df[["department_id", "department_name", "location"]],
            how="left",
            on="department_id",
        )

        dim_staff = staff_df[
            [
                "staff_id",
                "first_name",
                "last_name",
                "department_name",
                "location",
                "email_address",
            ]
        ].drop_duplicates()

        return dim_staff

    except KeyError as e:
        raise KeyError(f"Error creating dim_staff: {e}")
    except Exception as e:
        raise Exception(f"Error creating dim_staff: {e}")
