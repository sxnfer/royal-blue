import os
from datetime import datetime
from typing import Generator, Tuple

import boto3
import pandas as pd
import pytest
from moto import mock_aws
from types_boto3_s3.client import S3Client


@pytest.fixture(scope="module", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3_client(aws_credentials) -> Generator[S3Client, None, None]:
    with mock_aws():
        client: S3Client = boto3.client("s3", region_name="eu-west-2")
        yield client


@pytest.fixture(scope="function")
def s3_client_with_empty_test_bucket(
    s3_client: S3Client, aws_credentials
) -> Generator[Tuple[S3Client, str], None, None]:
    bucket_name = "test-bucket"
    s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    yield (s3_client, bucket_name)


@pytest.fixture(scope="function")
def valid_data_frame_data():
    return [
        {
            "table_name": "test_table",
            "last_updated": "2025-05-27 01:23:45.678910",
            "data_frame": pd.DataFrame(
                {
                    "name": ["Charley", "Oliver"],
                    "age": [27, 28],
                }
            ),
        },
        {
            "table_name": "test_table_2",
            "last_updated": "2025-05-27 02:34:56.798101",
            "data_frame": pd.DataFrame(
                {
                    "country": ["Lancashire", "Greater Manchester"],
                    "city": ["Preston", "Manchester"],
                    "road": ["Victoria", "Oxford Road"],
                }
            ),
        },
    ]


@pytest.fixture(scope="module")
def test_table_data_list():
    return [
        {
            "currency_id": 1,
            "currency_code": "GBP",
            "created_at": datetime.fromisoformat("2022-11-03 14:20:49.962"),
            "last_updated": datetime.fromisoformat("2022-11-03 14:20:49.962"),
        },
        {
            "currency_id": 2,
            "currency_code": "USD",
            "created_at": datetime.fromisoformat("2022-11-03 14:20:49.962"),
            "last_updated": datetime.fromisoformat("2022-11-03 14:20:49.962"),
        },
        {
            "currency_id": 3,
            "currency_code": "EUR",
            "created_at": datetime.fromisoformat("2022-11-03 14:20:49.962"),
            "last_updated": datetime.fromisoformat("2022-11-03 14:20:49.962"),
        },
    ]


@pytest.fixture(scope="module")
def test_data_frame(test_table_data_list):
    data_frame = pd.DataFrame(test_table_data_list)

    return data_frame
