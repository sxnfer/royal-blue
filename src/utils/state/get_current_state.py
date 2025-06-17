import logging
from typing import Any, Dict

import orjson
from types_boto3_s3.client import S3Client

from src.utils.s3.add_file_to_s3_bucket import add_file_to_s3_bucket
from src.utils.s3.get_file_from_s3_bucket import get_file_from_s3_bucket
from src.utils.s3.s3_error_map import s3_error_map

logger = logging.getLogger(__name__)


def get_current_state(
    s3_client: S3Client,
    bucket_name: str,
    key: str = "lambda_state.json",
    s3_error_map: Dict[str, str] = s3_error_map,
) -> Dict[str, Any]:
    """
    Retrieves the current state JSON from an S3 bucket and returns it as a dictionary.
    If the state file does not exist, initializes an empty state and uploads it to S3.

    Args:
        s3_client (S3Client): Boto3 S3 client instance.
        bucket_name (str): Name of the S3 bucket.
        key (str, optional): Key/path of the state file in the bucket. Defaults to "lambda_state.json".
        s3_error_map (Dict[str, str], optional): Mapping of S3 error codes to messages.

    Returns:
        Dict[str, Any]: Parsed JSON state from the file or initialized empty state.

    Raises:
        Exception: For any S3 error other than a missing key.
    """
    try:
        s3_response = get_file_from_s3_bucket(s3_client, bucket_name, key)

        if s3_response.get("error"):
            if (
                s3_response["error"]["message"]
                == f"NoSuchKey: {s3_error_map['NoSuchKey']}"
            ):
                empty_state = {
                    "ingest_state": {"last_updated": None, "tables": {}},
                    "transform_state": {"last_updated": None, "tables": {}},
                    "load_state": {"last_updated": None, "tables": {}},
                }
                body = orjson.dumps(empty_state)

                add_file_to_s3_bucket(s3_client, bucket_name, key, body)

                return empty_state

            else:
                raise Exception(s3_response["error"]["message"])

        data = orjson.loads(s3_response["success"]["data"])
        return data

    except orjson.JSONDecodeError as e:
        logger.error(f"ERROR: Invalid JSON in {key}: {e}")
        return {"ingest_state": {}}
