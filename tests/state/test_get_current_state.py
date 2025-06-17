import json

import boto3
import pytest
from moto import mock_aws

from src.utils.state.get_current_state import get_current_state


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


@pytest.mark.describe("get_current_state Behavior")
@mock_aws
class TestGetCurrentState:
    @pytest.mark.it("Returns a Python dict with expected variables on success")
    def test_get_current_state_success(self, s3_fixture):
        s3, bucket = s3_fixture
        mock_state = {"ingest_state": [{"table_name": "test_table"}]}

        s3.put_object(
            Bucket=bucket,
            Key="lambda_state.json",
            Body=json.dumps(mock_state).encode("utf-8"),
        )

        result = get_current_state(s3, bucket)
        assert isinstance(result, dict)
        assert "ingest_state" in result
        assert isinstance(result["ingest_state"], list)
        assert result["ingest_state"][0]["table_name"] == "test_table"

    @pytest.mark.it("Returns correct error message for non-existent JSON (NoSuchKey")
    def test_get_current_state_NoSuchKey_error(self, s3_fixture):
        s3, bucket = s3_fixture

        result = get_current_state(s3, bucket)
        assert result == {
            "ingest_state": {"last_updated": None, "tables": {}},
            "transform_state": {"last_updated": None, "tables": {}},
            "load_state": {"last_updated": None, "tables": {}},
        }

    @pytest.mark.it("Returns None for invalid JSON decoding error")
    def test_invalid_json_decode(self, s3_fixture):
        s3, bucket = s3_fixture

        s3.put_object(Bucket=bucket, Key="lambda_state.json", Body="hello")

        result = get_current_state(s3, bucket)
        assert result == {"ingest_state": {}}
