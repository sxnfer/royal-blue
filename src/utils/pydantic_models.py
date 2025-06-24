from datetime import datetime
from typing import Dict, List

import pandas as pd
from pydantic import BaseModel, ConfigDict, TypeAdapter


class ConnectionInfo(BaseModel):
    user: str
    password: str
    host: str
    dbname: str
    port: int


class BaseLambdaSettings(BaseModel):
    lambda_state_bucket: str


class ExtractSettings(BaseLambdaSettings):
    ingest_zone_bucket: str


class TransformSettings(ExtractSettings):
    process_zone_bucket: str


class LoadSettings(BaseModel):
    process_zone_bucket: str


class EnvironmentVariables(BaseModel):
    environment_variable: str


class StateLogItem(BaseModel):
    table_name: str
    last_updated: datetime
    operation_timestamp: datetime
    file_name: str
    key: str


class StateTableItem(BaseModel):
    table_name: str
    last_updated: datetime | None = None
    log_items: List[StateLogItem] = []


class StateTablesTotesys(BaseModel):
    counterparty: StateTableItem = StateTableItem(table_name="counterparty")
    address: StateTableItem = StateTableItem(table_name="address")
    staff: StateTableItem = StateTableItem(table_name="staff")
    design: StateTableItem = StateTableItem(table_name="design")
    sales_order: StateTableItem = StateTableItem(table_name="sales_order")
    currency: StateTableItem = StateTableItem(table_name="currency")
    department: StateTableItem = StateTableItem(table_name="department")
    purchase_order: StateTableItem = StateTableItem(table_name="purchase_order")
    payment_type: StateTableItem = StateTableItem(table_name="payment_type")
    payment: StateTableItem = StateTableItem(table_name="payment")
    transaction: StateTableItem = StateTableItem(table_name="transaction")


class StateTablesWarehouse(BaseModel):
    dim_counterparty: StateTableItem = StateTableItem(table_name="dim_counterparty")
    dim_location: StateTableItem = StateTableItem(table_name="dim_location")
    dim_staff: StateTableItem = StateTableItem(table_name="dim_staff")
    dim_design: StateTableItem = StateTableItem(table_name="dim_design")
    fact_sales_order: StateTableItem = StateTableItem(table_name="fact_sales_order")
    dim_currency: StateTableItem = StateTableItem(table_name="dim_currency")
    dim_date: StateTableItem = StateTableItem(table_name="dim_date")
    dim_payment_type: StateTableItem = StateTableItem(table_name="dim_payment_type")
    dim_transaction: StateTableItem = StateTableItem(table_name="dim_transaction")
    fact_payment: StateTableItem = StateTableItem(table_name="fact_payment")
    fact_purchase_order: StateTableItem = StateTableItem(
        table_name="fact_purchase_order"
    )


class StateItemBase(BaseModel):
    last_updated: datetime | None = None


class StateItemExtract(StateItemBase):
    tables: StateTablesTotesys = StateTablesTotesys()


class StateItemTransform(StateItemBase):
    tables: StateTablesWarehouse = StateTablesWarehouse()


class StateItemLoad(StateItemBase):
    tables: StateTablesWarehouse = StateTablesWarehouse()


class StateItem(BaseModel):
    last_updated: datetime | None = None
    tables: Dict[str, StateTableItem] = {}


class State(BaseModel):
    extract_state: StateItem = StateItem()
    transform_state: StateItem = StateItem()
    load_state: StateItem = StateItem()


class LambdaResult(BaseModel):
    files_to_process: List[StateLogItem] = []


class FactOrDimToProcess(BaseModel):
    table_name: str
    data_frame: pd.DataFrame
    model_config = ConfigDict(arbitrary_types_allowed=True)


FilesToProcessList = TypeAdapter(List[StateLogItem])
