from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError
from moto import mock_aws

from src.utils.s3.add_file_to_s3_bucket import add_file_to_s3_bucket
from src.utils.s3.get_file_from_s3_bucket import get_file_from_s3_bucket


@pytest.mark.describe("get_file_from_s3_bucket Utility Function Behaviour")
@mock_aws
class TestS3GetFunctionality:
    @pytest.mark.it(
        "Should check that a file is successfully retrieved from the S3 bucket"
    )
    def test_get_file_from_s3_success(self, s3_client):
        bucket = "test-bucket"
        key = "test_obj.txt"
        body = '{"test": "royal blue s3 bucket"}'

        s3_client.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        add_file_to_s3_bucket(client=s3_client, bucket_name=bucket, key=key, body=body)
        s3_obj = get_file_from_s3_bucket(s3_client, bucket_name=bucket, key=key)

        assert "File retrieved from s3" in s3_obj["success"]["message"]
        assert len(s3_obj["success"]["data"]) == len(body)

    @pytest.mark.parametrize(
        "error_code, message",
        [
            ("NoSuchBucket", "The specified bucket does not exist."),
            ("NoSuchKey", "The specified key does not exist."),
            ("InvalidBucketName", "The S3 bucket name provided is invalid."),
            ("AccessDenied", "Access denied when reading from the S3 bucket."),
            ("InternalError", "An internal AWS error occurred. Try again."),
            ("SlowDown", "Too many requests sent to S3. Try again later."),
        ],
    )
    @pytest.mark.it(
        "Should check errors are handled correctly when retrieving from an s3 bucket"
    )
    def test_get_file_error_responses(self, error_code, message):
        bucket = "non-existent-bucket"
        key = "test_obj"

        mock_client = Mock()
        mock_client.get_object.side_effect = ClientError(
            error_response={"Error": {"Message": message, "Code": error_code}},
            operation_name="GetObject",
        )

        response = get_file_from_s3_bucket(
            client=mock_client, bucket_name=bucket, key=key
        )

        assert "error" in response
        assert message in response["error"]["message"]
        assert error_code in response["error"]["message"]

    @pytest.mark.it("Should handle unexpected exceptions with generic error message")
    def test_get_file_unexpected_exception(self):
        mock_client = Mock()
        mock_client.get_object.side_effect = RuntimeError("unexpected failure")

        response = get_file_from_s3_bucket(
            client=mock_client, bucket_name="some-bucket", key="some-key"
        )

        assert "error" in response
        assert "unexpected failure" in response["error"]["message"]
