import logging

import orjson
from types_boto3_s3.client import S3Client

from src.utilities.s3.add_file_to_s3_bucket import add_file_to_s3_bucket

logger = logging.getLogger(__name__)


def set_current_state(
    current_state: dict, bucket_name, s3_client: S3Client, file_name="lambda_state.json"
) -> dict:
    """
    Converts the given dictionary to JSON and uploads it to S3 as `lambda_state.json`.

    Args:
        current_state (dict): Dictionary representing the current state.
        bucket_name (str): Name of the S3 bucket.
        s3_client (S3Client): S3 client instance.
        file_name (str): Name of the file to upload. Defaults to 'lambda_state.json'.

    Returns:
        dict: Result dictionary from the `add_file_to_s3_bucket` function.

    Raises:
        Exception: If the upload fails.
    """

    try:
        json_data = orjson.dumps(current_state)
        result = add_file_to_s3_bucket(s3_client, bucket_name, file_name, json_data)

        if result.get("error"):
            logger.error(f"Failed to update state in S3: {result['error']}")
            raise Exception("Failed to upload current state to S3.")
        return result

    except Exception as e:
        logger.error(f"Failed to set current state: {e}")
        raise
