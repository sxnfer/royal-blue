from botocore.exceptions import ClientError


def add_file_to_s3_bucket(client, bucket_name, key, body) -> dict[str, dict]:
    """
    Uploads a file to an S3 bucket and handles common errors.

    Args:
    client: A boto3 S3 client object.
    bucket_name (str): The name of the S3 bucket to upload to.
    key (str): The S3 object key (i.e., the path and filename in the bucket).
    body (bytes): The file content as bytes to upload to S3.

    Returns:
    dict: A dictionary indicating success or error. On success, contains a message and file info.
    On error, contains an error message and the raw error response.

    Raises:
    None. Errors are caught and returned as part of the response dictionary.
    """
    try:
        response = client.put_object(Bucket=bucket_name, Key=key, Body=body)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]

        if status_code != 200:
            return {"error": {"message": f"{status_code}: Unexpected error"}}

        return {
            "success": {
                "message": f"File uploaded to s3://{bucket_name}/{key}",
                "data": {"bucket": bucket_name, "key": key},
            }
        }

    except ClientError as err:
        code = err.response["Error"]["Code"]
        error_map = {
            "NoSuchBucket": "The specified bucket does not exist.",
            "AccessDenied": "Access denied when writing to the S3 bucket.",
            "InvalidBucketName": "The specified bucket is not valid.",
            "BucketAlreadyExists": "The bucket name is already in use.",
            "BucketAlreadyOwnedByYou": "You already own this bucket.",
        }
        message = error_map.get(code)
        return {"error": {"message": f"{code}: {message}", "raw_response": err}}

    except Exception as err:
        return {"error": {"message": f"{str(err)}", "raw_response": err}}
