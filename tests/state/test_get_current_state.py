import pytest
from moto import mock_aws

from src.utils.pydantic_models import State, StateItem, StateTableItem
from src.utils.state.get_current_state import get_current_state, initialize_state


@pytest.mark.describe("Test initialize_state")
class TestInitializeState:
    # @pytest.mark.skip
    @pytest.mark.it(
        "check that it returns a State object with extract_state, transform_state, and load_state attributes with empty tables attribute"
    )
    def test_check_returns_state_obj(self):
        result = initialize_state([], [], [])
        assert isinstance(result, State)
        assert isinstance(result.extract_state, StateItem)
        assert isinstance(result.transform_state, StateItem)
        assert isinstance(result.load_state, StateItem)
        assert result.extract_state.last_updated is None
        assert result.transform_state.last_updated is None
        assert result.load_state.last_updated is None
        assert result.extract_state.tables == {}
        assert result.transform_state.tables == {}
        assert result.load_state.tables == {}

    # @pytest.mark.skip
    @pytest.mark.it(
        "check that each state object has a tables object with one table initialised"
    )
    def test_check_returns_state_obj_with_table_initialised(self):
        extract_table_name = "extract_table_1"
        transform_table_name = "transform_table_1"
        load_table_name = "load_table_1"
        result = initialize_state(
            [extract_table_name], [transform_table_name], [load_table_name]
        )

        initialised_tables_state = [
            (
                extract_table_name,
                result.extract_state.tables.get(extract_table_name),
            ),
            (
                transform_table_name,
                result.transform_state.tables.get(transform_table_name),
            ),
            (load_table_name, result.load_state.tables.get(load_table_name)),
        ]
        for table_name, table_state in initialised_tables_state:
            assert isinstance(table_state, StateTableItem)
            assert table_state.table_name == table_name
            assert table_state.log_items == []
            assert table_state.last_updated is None
        assert len(result.extract_state.tables.keys()) == 1
        assert len(result.transform_state.tables.keys()) == 1
        assert len(result.load_state.tables.keys()) == 1

    # @pytest.mark.skip
    @pytest.mark.it("check that multiple tables are initialised in each state object")
    def test_multiple_tables_initialised(self):
        extract_table_names = ["extract_table_1", "extract_table_2"]
        transform_table_names = ["transform_table_1", "transform_table_2"]
        load_table_names = ["load_table_1", "load_table_2"]
        result = initialize_state(
            extract_table_names, transform_table_names, load_table_names
        )
        assert len(result.extract_state.tables.keys()) == 2
        assert len(result.transform_state.tables.keys()) == 2
        assert len(result.load_state.tables.keys()) == 2
        for table_name in extract_table_names:
            table_object = result.extract_state.tables.get(table_name)
            assert table_object
            assert table_object.table_name == table_name
            assert isinstance(table_object, StateTableItem)

        for table_name in transform_table_names:
            table_object = result.transform_state.tables.get(table_name)
            assert table_object
            assert table_object.table_name == table_name
            assert isinstance(table_object, StateTableItem)

        for table_name in load_table_names:
            table_object = result.load_state.tables.get(table_name)
            assert table_object
            assert table_object.table_name == table_name
            assert isinstance(table_object, StateTableItem)


@pytest.mark.describe("get_current_state Behavior")
@mock_aws
class TestGetCurrentState:
    # @pytest.mark.skip
    @pytest.mark.it(
        "check that an empty state bucket returns an initialised State object"
    )
    def test_get_current_state_success(self, s3_client_with_empty_test_bucket):
        s3_client, bucket_name = s3_client_with_empty_test_bucket

        result = get_current_state(s3_client, bucket_name)
        assert isinstance(result, State)
        assert isinstance(result, State)
        assert isinstance(result.extract_state, StateItem)
        assert isinstance(result.transform_state, StateItem)
        assert isinstance(result.load_state, StateItem)
        assert result.extract_state.last_updated is None
        assert result.transform_state.last_updated is None
        assert result.load_state.last_updated is None
        assert len(result.extract_state.tables.keys())
        assert len(result.transform_state.tables.keys())
        assert len(result.load_state.tables.keys())

    # @pytest.mark.skip
    @pytest.mark.it(
        "check that it raises an exception if we look for an invalid file key for the state file"
    )
    def test_get_current_state_NoSuchKey_error(self, s3_client_with_empty_test_bucket):
        s3_client, _ = s3_client_with_empty_test_bucket
        with pytest.raises(Exception):
            get_current_state(s3_client, "invalid_name")

    @pytest.mark.skip
    @pytest.mark.it("Returns None for invalid JSON decoding error")
    def test_invalid_json_decode(self, s3_fixture):
        s3, bucket = s3_fixture

        s3.put_object(Bucket=bucket, Key="lambda_state.json", Body="hello")

        result = get_current_state(s3, bucket)
        assert result == {"ingest_state": {}}
