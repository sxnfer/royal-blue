import json
from unittest.mock import patch

import boto3
import pytest
from moto import mock_aws

from src.utils.state.set_current_state import set_current_state


@pytest.mark.describe("set_current_state Behaviour")
@pytest.fixture
def s3_fixture():
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-west-2")
        bucket = "test-bucket"
        s3.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        yield s3, bucket


class TestSetCurrentState:
    @pytest.mark.it("Successfully uploads the expected JSON to S3")
    def test_set_current_state_success(self, s3_fixture):
        s3, bucket = s3_fixture
        mock_state = {"ingest_state": [{"table_name": "test_table"}]}

        set_current_state(mock_state, bucket, s3)

        response = s3.get_object(Bucket=bucket, Key="lambda_state.json")

        content = response["Body"].read().decode("utf-8")
        data = json.loads(content)

        assert data == mock_state

    def test_set_new_overwrites_current_state(self, s3_fixture):
        s3, bucket = s3_fixture
        current_state = {"json data": "old"}
        new_state = {"json data": "new"}

        s3.put_object(
            Bucket=bucket, Key="lambda_state.json", Body=json.dumps(current_state)
        )

        set_current_state(new_state, bucket, s3)

        response = s3.get_object(Bucket=bucket, Key="lambda_state.json")

        content = response["Body"].read().decode("utf-8")
        data = json.loads(content)

        assert data == new_state

    @pytest.mark.it("Raises an exception when add_file_to_s3_bucket returns an error.")
    def test_add_file_returns_error(self, s3_fixture):
        s3, bucket = s3_fixture
        mock_state = {"some": "state"}

        with patch(
            "src.utils.state.set_current_state.add_file_to_s3_bucket"
        ) as mock_upload:
            mock_upload.return_value = {"error": "Upload failed"}
            with pytest.raises(Exception, match="Failed to upload current state to S3"):
                set_current_state(mock_state, bucket, s3)
