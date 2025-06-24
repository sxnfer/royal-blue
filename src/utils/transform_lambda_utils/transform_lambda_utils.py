from datetime import datetime
from types import FunctionType
from typing import List

import pandas as pd
from types_boto3_s3.client import S3Client

from src.utils.extract_lambda_utils import create_parquet_metadata
from src.utils.parquets.create_data_frame_from_parquet import (
    create_data_frame_from_parquet,
)
from src.utils.parquets.create_parquet_from_data_frame import (
    create_parquet_from_data_frame,
)
from src.utils.pydantic_models import LambdaResult, StateLogItem
from src.utils.s3.add_file_to_s3_bucket import add_file_to_s3_bucket
from src.utils.s3.get_file_from_s3_bucket import get_file_from_s3_bucket


def get_dataframes_from_files_to_process(
    s3_client: S3Client, bucket: str, files_to_process: List[StateLogItem]
):
    all_df_to_process = {}
    for file_data in files_to_process:
        table_name = file_data.table_name
        key = file_data.key

        response = get_file_from_s3_bucket(s3_client, bucket, key)

        parquet = response["success"]["data"]

        df = create_data_frame_from_parquet(parquet)

        all_df_to_process[table_name] = df

    return all_df_to_process


# mutates result and state
def add_log_to_result_and_state(
    log: StateLogItem,
    result: LambdaResult,
    state,
    table_name: str,
    last_updated: datetime,
    operation_timestamp: datetime,
):
    result.files_to_process.append(log)
    state["transform_state"]["tables"][table_name] = {}
    state["transform_state"]["tables"][table_name]["transformation_timestamp"] = (
        operation_timestamp
    )
    state["transform_state"]["tables"][table_name]["transform_log"] = []
    state["transform_state"]["tables"][table_name]["transform_log"].append(log)

    state["transform_state"]["last_updated"] = last_updated


def initialize_dim_date(
    create_dim_date_df_func: FunctionType,
    s3_client: S3Client,
    bucket_name: str,
    result: LambdaResult,
    final_state,
):
    new_table_name = "dim_date"
    dim_date_df = create_dim_date_df_func("20221102", "20400101")
    dim_date_transformation_time_stamp = datetime.now()
    dim_date_log_item = get_log_item_and_upload_df_to_s3(
        s3_client=s3_client,
        bucket_name=bucket_name,
        last_updated=dim_date_transformation_time_stamp,
        new_table_name=new_table_name,
        df=dim_date_df,
        operation_timestamp=dim_date_transformation_time_stamp,
        create_parquet_from_df_func=create_parquet_from_data_frame,  # type: ignore
    )

    add_log_to_result_and_state(
        log=dim_date_log_item,
        result=result,
        state=final_state,
        last_updated=dim_date_transformation_time_stamp,
        operation_timestamp=dim_date_transformation_time_stamp,
        table_name=new_table_name,
    )


def get_log_item_and_upload_df_to_s3(
    s3_client: S3Client,
    bucket_name: str,
    last_updated: datetime,
    new_table_name: str,
    df: pd.DataFrame,
    operation_timestamp: datetime,
    create_parquet_from_df_func: FunctionType,
):
    parquet = create_parquet_from_df_func(df)
    file_name, key = create_parquet_metadata(
        last_updated,
        new_table_name,
    )

    response = add_file_to_s3_bucket(s3_client, bucket_name, key, parquet)

    if response.get("error"):
        raise Exception("something went wrong while upload")

    log_item = StateLogItem(
        table_name=new_table_name,
        last_updated=last_updated,
        operation_timestamp=operation_timestamp,
        file_name=file_name,
        key=key,
    )

    return log_item
