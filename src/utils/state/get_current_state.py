import logging
from typing import Dict

from types_boto3_s3.client import S3Client

from src.utils.constants import EXTRACT_TABLE_NAMES, LOAD_TABLE_NAMES
from src.utils.pydantic_models import State, StateTableItem
from src.utils.s3.add_file_to_s3_bucket import add_file_to_s3_bucket
from src.utils.s3.get_file_from_s3_bucket import get_file_from_s3_bucket
from src.utils.s3.s3_error_map import s3_error_map

logger = logging.getLogger(__name__)


def initialize_state(
    extract_table_names: list[str] = EXTRACT_TABLE_NAMES,
    transform_table_names: list[str] = LOAD_TABLE_NAMES,
    load_table_names: list[str] = LOAD_TABLE_NAMES,
) -> State:
    new_state: State = State()

    for table_name in extract_table_names:
        new_state.extract_state.tables[table_name] = StateTableItem(
            table_name=table_name
        )
    for table_name in transform_table_names:
        new_state.transform_state.tables[table_name] = StateTableItem(
            table_name=table_name
        )
    for table_name in load_table_names:
        new_state.load_state.tables[table_name] = StateTableItem(table_name=table_name)

    return new_state


def get_current_state(
    s3_client: S3Client,
    bucket_name: str,
    key: str = "lambda_state.json",
    s3_error_map: Dict[str, str] = s3_error_map,
) -> State:
    """
    Retrieves the current State as JSON from an S3 bucket and returns it as a pydantic State object.
    If the state file does not exist, initializes an empty state and uploads it to S3.

    Args:
        s3_client (S3Client): Boto3 S3 client instance.
        bucket_name (str): Name of the S3 bucket.
        key (str, optional): Key/path of the state file in the bucket. Defaults to "lambda_state.json".
        s3_error_map (Dict[str, str], optional): Mapping of S3 error codes to messages.

    Returns:
        State: Parsed JSON state from the file or initialized empty state.

    Raises:
        Exception: For any S3 error other than a missing key.
    """

    s3_response = get_file_from_s3_bucket(s3_client, bucket_name, key)

    if s3_response.get("error"):
        if s3_response["error"]["message"] == f"NoSuchKey: {s3_error_map['NoSuchKey']}":
            empty_state = initialize_state()
            body = empty_state.model_dump_json()

            add_file_to_s3_bucket(s3_client, bucket_name, key, body)

            return empty_state

        else:
            raise Exception(s3_response["error"]["message"])

    data = State.model_validate(s3_response["success"]["data"])

    return data
