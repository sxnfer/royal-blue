import json
import logging
import os

import boto3
import orjson
import pandas as pd
from types_boto3_s3.client import S3Client

from src.db.connection import connect_db
from src.utilities.load_lambda_utils import create_db_entries_from_df
from src.utilities.parquets.create_data_frame_from_parquet import (
    create_data_frame_from_parquet,
)
from src.utilities.s3.get_file_from_s3_bucket import get_file_from_s3_bucket
from src.utilities.typing_utils import EmptyDict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, context: EmptyDict):
    s3_client: S3Client = boto3.client("s3")
    PROCESS_ZONE_BUCKET_NAME = os.environ.get("PROCESS_ZONE_BUCKET_NAME")
    # LAMBDA_STATE_BUCKET_NAME = os.environ.get("LAMBDA_STATE_BUCKET_NAME")
    conn = connect_db("DATAWAREHOUSE")

    files_to_process = orjson.loads(json.dumps(event)).get("files_to_process")
    logger.info("Start Loading files into Data Warehouse")

    """
    Loads data from parquet files stored in S3 into the DATAWAREHOUSE database. 
    Differentiates between dimension and fact tables, processes each accordingly,
    and logs the progress. Intended to run as an AWS Lambda function as part of 
    the ETL pipeline.
    
    Args:
    event (dict): AWS Lambda event object containing a list of files to process, 
    with metadata including table names and S3 keys.
    context (EmptyDict): AWS Lambda context object (not used, included for compatibility).
        
    Returns:
    None (Although will log whether or not files have been processed successfully).
    
    Raises:
    Exception: If any error occurs during S3 file retrieval, parquet conversion, 
    or database loading.
    """

    if not files_to_process:
        logger.info("No files to process")
        return

    try:
        dims_to_process = []
        facts_to_process = []

        for file_data in files_to_process:
            response = get_file_from_s3_bucket(
                s3_client, bucket_name=PROCESS_ZONE_BUCKET_NAME, key=file_data["key"]
            )
            df: pd.DataFrame = create_data_frame_from_parquet(
                response["success"]["data"]
            )

            if file_data["table_name"].startswith("dim"):
                dims_to_process.append(
                    {
                        "table_name": file_data["table_name"],
                        "data_frame": df,
                    }
                )
            else:
                facts_to_process.append(
                    {
                        "table_name": file_data["table_name"],
                        "data_frame": df,
                    }
                )

        with conn:
            for file_data in dims_to_process:
                logger.info(
                    f"Processing {len(file_data['data_frame'])} rows into table {file_data['table_name']}."
                )
                create_db_entries_from_df(
                    conn, file_data["table_name"], file_data["data_frame"]
                )

            for file_data in facts_to_process:
                create_db_entries_from_df(
                    conn, file_data["table_name"], file_data["data_frame"]
                )

    except Exception as err:
        logger.critical(err)
        raise err

    logger.info("Finish loading files into Data Warehouse")
    # logger.info("Result of loading process:\n%s", pformat(result))
    return


# 2025-06-10 23:45:24,580 | ERROR: Failed to insert records into fact_sales_order: insert or update on table "fact_sales_order" violates foreign key constraint "fact_sales_order_agreed_delivery_location_id_fkey"
# DETAIL:  Key (agreed_delivery_location_id)=(8) is not present in table "dim_location".

if __name__ == "__main__":
    test_args = {
        "files_to_process": [
            {
                "table_name": "dim_counterparty",
                "key": "2022/11/3/dim_counterparty_2022-11-3_14-20-51_563000.parquet",
                "filename": "dim_counterparty_2022-11-3_14-20-51_563000.parquet",
                "last_updated": "2022-11-03T14:20:51.563000",
                "transformation_timestamp": "2025-06-10T23:28:03.354725",
            },
            {
                "table_name": "dim_location",
                "key": "2022/11/3/dim_location_2022-11-3_14-20-49_962000.parquet",
                "filename": "dim_location_2022-11-3_14-20-49_962000.parquet",
                "last_updated": "2022-11-03T14:20:49.962000",
                "transformation_timestamp": "2025-06-10T23:28:03.521823",
            },
            {
                "table_name": "dim_staff",
                "key": "2022/11/3/dim_staff_2022-11-3_14-20-51_563000.parquet",
                "filename": "dim_staff_2022-11-3_14-20-51_563000.parquet",
                "last_updated": "2022-11-03T14:20:51.563000",
                "transformation_timestamp": "2025-06-10T23:28:03.694398",
            },
            {
                "table_name": "dim_design",
                "key": "2025/6/10/dim_design_2025-6-10_17-51-9_671000.parquet",
                "filename": "dim_design_2025-6-10_17-51-9_671000.parquet",
                "last_updated": "2025-06-10T17:51:09.671000",
                "transformation_timestamp": "2025-06-10T23:28:03.874850",
            },
            {
                "table_name": "fact_sales_order",
                "key": "2025/6/10/fact_sales_order_2025-6-10_18-1-10_155000.parquet",
                "filename": "fact_sales_order_2025-6-10_18-1-10_155000.parquet",
                "last_updated": "2025-06-10T18:01:10.155000",
                "transformation_timestamp": "2025-06-10T23:28:06.736708",
            },
            {
                "table_name": "dim_currency",
                "key": "2022/11/3/dim_currency_2022-11-3_14-20-49_962000.parquet",
                "filename": "dim_currency_2022-11-3_14-20-49_962000.parquet",
                "last_updated": "2022-11-03T14:20:49.962000",
                "transformation_timestamp": "2025-06-10T23:28:06.940325",
            },
            {
                "table_name": "dim_date",
                "key": "2025/6/10/dim_date_2025-6-10_23-28-1_818204.parquet",
                "filename": "dim_date_2025-6-10_23-28-1_818204.parquet",
                "last_updated": "2025-06-10T23:28:01.818204",
                "transformation_timestamp": "2025-06-10T23:28:08.095612",
            },
        ]
    }

    # lambda_handler(test_args, {})
