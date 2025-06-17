import logging
import os
from copy import deepcopy
from datetime import datetime
from pprint import pformat

import boto3
import orjson
from psycopg import Error
from types_boto3_s3.client import S3Client

from src.utils.db.connection import connect_db
from src.utils.db.db_helpers import (
    get_table_data,
    get_totesys_table_names,
    handle_psycopg_exceptions,
)
from src.utils.extract_lambda_utils import (
    create_data_frame_from_list,
    create_parquet_metadata,
    get_last_updated_from_raw_table_data,
    initialize_table_state,
)
from src.utils.parquets.create_parquet_from_data_frame import (
    create_parquet_from_data_frame,
)
from src.utils.s3.add_file_to_s3_bucket import add_file_to_s3_bucket
from src.utils.state.get_current_state import get_current_state
from src.utils.state.set_current_state import set_current_state
from src.utils.typing_utils import EmptyDict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event: EmptyDict, context: EmptyDict):
    """
    Extracts new or updated data from all tables in the TOTESYS database, converts the data into parquet files,
    uploads them to an S3 bucket, and updates the extraction state. Designed to run as an AWS Lambda function
    for incremental ETL processing.

    Args:
    event (EmptyDict): AWS Lambda event object (not used, included for compatibility).
    context (EmptyDict): AWS Lambda context object (not used, included for compatibility).

    Returns:
    A JSON-encoded summary of the files processed, including table name, extraction timestamp,
    last updated timestamp, file name, and S3 key.

    Example of the output:
    {
        "files_to_process": [
            {
                "table_name": "counterparty",
                "extraction_timestamp": "2025-06-10T20:51:34.260407",
                "last_updated": "2022-11-03T14:20:51.563000",
                "file_name": "counterparty_2022-11-3_14-20-51_563000.parquet",
                "key": "2022/11/3/counterparty_2022-11-3_14-20-51_563000.parquet",
            },
            {
                "table_name": "address",
                "extraction_timestamp": "2025-06-10T20:51:37.179714",
                "last_updated": "2022-11-03T14:20:49.962000",
                "file_name": "address_2022-11-3_14-20-49_962000.parquet",
                "key": "2022/11/3/address_2022-11-3_14-20-49_962000.parquet",
            }
    }

    Raises:
    Error: If a database error occurs during extraction.
    Exception: If any other error occurs during the process, such as S3 upload failure or unexpected issues.
    """
    conn = connect_db("TOTESYS")
    s3_client: S3Client = boto3.client("s3")
    INGEST_ZONE_BUCKET_NAME = os.environ.get("INGEST_ZONE_BUCKET_NAME")
    LAMBDA_STATE_BUCKET_NAME = os.environ.get("LAMBDA_STATE_BUCKET_NAME")
    result = {"files_to_process": []}

    try:
        with conn:
            logger.info("Starting extraction process for all tables")

            totesys_tables = get_totesys_table_names(conn)

            for table_name in totesys_tables:
                logger.info(f"Starting extraction of {table_name}")

                current_state = get_current_state(s3_client, LAMBDA_STATE_BUCKET_NAME)
                current_state = initialize_table_state(current_state, table_name)

                current_state_last_updated: datetime | None = current_state[
                    "ingest_state"
                ][table_name]["last_updated"]

                table_data = get_table_data(
                    conn,
                    table_name,  # type: ignore
                    current_state_last_updated,
                )
                extraction_timestamp = datetime.now()

                if not len(table_data):
                    logger.info(f"No new data to extract from table: {table_name}")
                    continue

                new_table_data_last_updated: datetime = (
                    get_last_updated_from_raw_table_data(table_data)
                )

                table_df = create_data_frame_from_list(table_data)
                parquet_file = create_parquet_from_data_frame(table_df)

                filename, key = create_parquet_metadata(
                    new_table_data_last_updated, table_name
                )

                response = add_file_to_s3_bucket(
                    s3_client, INGEST_ZONE_BUCKET_NAME, key, parquet_file
                )

                # ! REVIEW should I get raw error object from add_file_to_s3_bucket function??
                if response.get("error"):
                    raise response["error"]["raw_response"]  # type: ignore

                new_state_log_entry = {
                    "table_name": table_name,
                    "extraction_timestamp": extraction_timestamp,
                    "last_updated": new_table_data_last_updated,
                    "file_name": filename,
                    "key": key,
                }

                result["files_to_process"].append(new_state_log_entry)

                updated_state_all = deepcopy(current_state)
                updated_state_all["ingest_state"][table_name]["last_updated"] = (
                    #  TODO THEO check unbound error when not ignoring types
                    new_table_data_last_updated  # type: ignore
                )
                updated_state_all["ingest_state"][table_name]["ingest_log"].append(
                    new_state_log_entry  # type: ignore
                )

                set_current_state(
                    updated_state_all, LAMBDA_STATE_BUCKET_NAME, s3_client
                )

                logger.info(f"Finish extracting table:{table_name} data")

        logger.info("Result of extraction process:\n%s", pformat(result))
        logger.info("End of extraction process for all tables")

        return orjson.dumps(result)

    except Error as err:
        handle_psycopg_exceptions(err)
        raise err

    except Exception as err:
        logger.critical(err, exc_info=err)
        raise err


if __name__ == "__main__":
    pass
