import logging

from types_boto3_s3.client import S3Client

from src.utils.pydantic_models import State
from src.utils.s3.add_file_to_s3_bucket import add_file_to_s3_bucket

logger = logging.getLogger(__name__)


def set_current_state(
    new_state: State,
    bucket_name,
    s3_client: S3Client,
    file_name="lambda_state.json",
):
    """
    Converts the given pydantic State object into JSON and uploads it to S3 as `lambda_state.json`.

    Args:
        current_state (State): a pydantic State object representing the current state.
        bucket_name (str): Name of the S3 bucket.
        s3_client (S3Client): S3 client instance.
        file_name (str): Name of the file to upload. Defaults to 'lambda_state.json'.



    Raises:
        Exception: If the upload fails.
    """

    try:
        if not isinstance(new_state, State):
            raise TypeError(f"Expected a State object, got {type(new_state).__name__}")
        json_data = new_state.model_dump_json()
        result = add_file_to_s3_bucket(s3_client, bucket_name, file_name, json_data)

        if result.get("error"):
            logger.error(f"Failed to update state in S3: {result['error']}")
            raise Exception("Failed to upload current state to S3.")
        return result

    except Exception as err:
        logger.error(f"Failed to set current state: {err}")
        raise err
