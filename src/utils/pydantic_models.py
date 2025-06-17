from datetime import datetime
from typing import List

from pydantic import BaseModel, TypeAdapter


class EnvironmentVariables(BaseModel):
    environment_variable: str


class FilesToProcessItem(BaseModel):
    table_name: str
    extraction_timestamp: datetime
    last_updated: datetime
    file_name: str
    key: str


FilesToProcessList = TypeAdapter(List[FilesToProcessItem])


class FilesToProcess(BaseModel):
    files_to_process: List[FilesToProcessItem]


class ProcessState(BaseModel):
    last_updated: datetime | None
    tables: dict


class State(BaseModel):
    ingest_state: dict
    transform_state: ProcessState
