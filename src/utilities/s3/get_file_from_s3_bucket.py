from typing import Union

from botocore.exceptions import ClientError
from types_boto3_s3.client import S3Client

from src.utilities.s3.s3_error_map import s3_error_map


def get_file_from_s3_bucket(
    client: S3Client, bucket_name, key, error_map=s3_error_map
) -> dict[str, dict[str, Union[str, bytes]]]:
    """
    Retrieves a file object from the specified S3 bucket.

    Args:
        client (BaseClient): Boto3 S3 client instance.
        bucket_name (str): Name of the S3 bucket.
        key (str): Key (path/filename) of the S3 object.
        error_map (dict, optional): Mapping of S3 error codes to messages.

    Returns:
        dict: A dictionary with either:
            - "success": containing message and raw file content as bytes,
            - or "error": containing error message.

    Raises:
    None. Errors are caught and returned as part of the response dictionary.
    """

    try:
        response = client.get_object(Bucket=bucket_name, Key=key)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]

        if status_code != 200:
            return {"error": {"message": f"{status_code}: Unexpected error"}}

        # content = response["Body"].read().decode("utf-8")
        content = response["Body"].read()
        return {
            "success": {
                "message": f"File retrieved from s3://{bucket_name}/{key}",
                "data": content,
            }
        }

    except ClientError as err:
        code = err.response["Error"]["Code"]
        message = error_map.get(code)
        return {"error": {"message": f"{code}: {message}"}}

    except Exception as ex:
        return {"error": {"message": f"{str(ex)}"}}
