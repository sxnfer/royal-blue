TABLE_NAME_LOOKUP: dict[str, str | None] = {
    "counterparty": "dim_counterparty",
    "address": "dim_location",
    "staff": "dim_staff",
    "design": "dim_design",
    "sales_order": "fact_sales_order",
    "currency": "dim_currency",
    "dim_date": "dim_date",
    "department": None,
    "purchase_order": None,
    "payment_type": None,
    "payment": None,
    "transaction": None,
}

EXTRACT_TABLE_NAMES: list[str] = list(TABLE_NAME_LOOKUP.keys())

LOAD_DIM_TABLE_NAMES: list[str] = [
    table_name
    for table_name in TABLE_NAME_LOOKUP.values()
    if table_name and table_name.startswith("dim_")
]

LOAD_FACT_TABLE_NAMES: list[str] = [
    table_name
    for table_name in TABLE_NAME_LOOKUP.values()
    if table_name and table_name.startswith("fact_")
]

LOAD_TABLE_NAMES: list[str] = [*LOAD_DIM_TABLE_NAMES, *LOAD_FACT_TABLE_NAMES]
