TABLE_NAME_LOOKUP: dict[str, str | None] = {
    "counterparty": "dim_counterparty",
    "address": "dim_location",
    "staff": "dim_staff",
    "design": "dim_design",
    "currency": "dim_currency",
    "transaction": "dim_transaction",
    "payment_type": "dim_payment_type",
    "sales_order": "fact_sales_order",
    "purchase_order": "fact_purchase_order",
    "payment": "fact_payment",
    "department": None,
}

EXTRACT_TABLE_NAMES: list[str] = list(TABLE_NAME_LOOKUP.keys())

LOAD_DIM_TABLE_NAMES: list[str] = [
    *[
        table_name
        for table_name in TABLE_NAME_LOOKUP.values()
        if table_name and table_name.startswith("dim_")
    ],
    "dim_date",
]

LOAD_FACT_TABLE_NAMES: list[str] = [
    table_name
    for table_name in TABLE_NAME_LOOKUP.values()
    if table_name and table_name.startswith("fact_")
]

LOAD_TABLE_NAMES: list[str] = [*LOAD_DIM_TABLE_NAMES, *LOAD_FACT_TABLE_NAMES]
