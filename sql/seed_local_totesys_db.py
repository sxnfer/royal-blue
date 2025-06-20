from pprint import pprint

import pandas as pd

from src.utils.db.connection import connect_db
from src.utils.load_lambda_utils import create_db_entries_from_df

if __name__ == "__main__":
    address_df = pd.read_parquet(
        "sql_local_tests/seed_data/address_2022-11-3_14-20-49_962000.parquet"
    )
    counterparty_df = pd.read_parquet(
        "sql_local_tests/seed_data/counterparty_2022-11-3_14-20-51_563000.parquet"
    )
    currency_df = pd.read_parquet(
        "sql_local_tests/seed_data/currency_2022-11-3_14-20-49_962000.parquet"
    )
    department_df = pd.read_parquet(
        "sql_local_tests/seed_data/department_2022-11-3_14-20-49_962000.parquet"
    )
    design_df = pd.read_parquet(
        "sql_local_tests/seed_data/design_2025-6-9_12-0-9_793000.parquet"
    )
    payment_type_df = pd.read_parquet(
        "sql_local_tests/seed_data/payment_type_2022-11-3_14-20-49_962000.parquet"
    )
    sales_order_df = pd.read_parquet(
        "sql_local_tests/seed_data/sales_order_2025-6-9_13-11-9_744000.parquet"
    )
    staff_df = pd.read_parquet(
        "sql_local_tests/seed_data/staff_2022-11-3_14-20-51_563000.parquet"
    )
    pprint(type(currency_df["created_at"][0]))

    currency_df["created_at"] = currency_df["created_at"].dt.tz_localize("UTC")
    currency_df["last_updated"] = currency_df["last_updated"].dt.tz_localize("UTC")

    # print(type(currency_df["currency_code"][0]))

    conn = connect_db("TOTESYS")

    with conn:
        create_db_entries_from_df(conn, "currency", currency_df)

# Failed to insert records into currency: malformed array literal: "GBP"
# DETAIL:  Array value must start with "{" or dimension information.
# CONTEXT:  unnamed portal parameter $2 = '...'
