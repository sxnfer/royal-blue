from datetime import datetime

import pytest

from src.utils.pydantic_models import State
from src.utils.state.set_current_state import set_current_state


@pytest.mark.describe("Test set_current_state function")
class TestSetCurrentState:
    @pytest.mark.it("Successfully uploads the expected State file to S3")
    def test_set_current_state_success(self, s3_client_with_empty_test_bucket):
        s3_client, bucket_name = s3_client_with_empty_test_bucket
        file_name = "lambda_state.json"
        mock_state = State()

        set_current_state(
            new_state=mock_state,
            bucket_name=bucket_name,
            s3_client=s3_client,
            file_name=file_name,
        )

        s3_reponse = s3_client.get_object(Bucket=bucket_name, Key=file_name)

        content = s3_reponse["Body"].read()
        uploaded_state = State.model_validate_json(content)

        assert mock_state == uploaded_state

    # @pytest.mark.skip
    @pytest.mark.it(
        "check that it raises an exception if an invalid state object is passed"
    )
    def test_raises_exception_on_invalid_state(self, s3_client_with_empty_test_bucket):
        s3_client, bucket_name = s3_client_with_empty_test_bucket
        with pytest.raises(TypeError):
            set_current_state(
                new_state={"invalid": "state"},  # type: ignore
                bucket_name=bucket_name,
                s3_client=s3_client,
            )

    # @pytest.mark.skip
    @pytest.mark.it("check that a new state object replaces the previous one")
    def test_set_new_overwrites_current_state(self, s3_client_with_empty_test_bucket):
        s3_client, bucket = s3_client_with_empty_test_bucket
        current_state = State()
        current_state.extract_state.last_updated = datetime.now()
        new_state = State()

        s3_client.put_object(
            Bucket=bucket, Key="lambda_state.json", Body=current_state.model_dump_json()
        )

        set_current_state(new_state, bucket, s3_client)

        response = s3_client.get_object(Bucket=bucket, Key="lambda_state.json")

        content = response["Body"].read().decode("utf-8")
        data = State.model_validate_json(content)

        assert data == new_state
        assert data != current_state
