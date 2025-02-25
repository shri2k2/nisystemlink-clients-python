from typing import Dict, List, Union

from pydantic import BaseModel, Field


class NamedValue(BaseModel):
    name: str
    value: Union[str, float, int]


class StepData(BaseModel):
    text: str
    parameters: List[Dict[str, str]]


class Status(BaseModel):
    status_type: str = Field(..., alias="statusType")
    status_name: str = Field(..., alias="statusName")


class ResultResponse(BaseModel):
    status: Status
    started_at: str = Field(..., alias="startedAt")
    updated_at: str = Field(..., alias="updatedAt")
    program_name: str = Field(..., alias="programName")
    id: str
    system_id: str = Field(..., alias="systemId")
    host_name: str = Field(..., alias="hostName")
    operator: str
    part_number: str = Field(..., alias="partNumber")
    serial_number: str = Field(..., alias="serialNumber")
    total_time_in_seconds: float = Field(..., alias="totalTimeInSeconds")
    keywords: List[str]
    properties: Dict[str, str]
    file_ids: List[str] = Field(..., alias="fileIds")
    data_table_ids: List[str] = Field(..., alias="dataTableIds")
    status_type_summary: Dict[str, int] = Field(..., alias="statusTypeSummary")
    workspace: str


class StepResponse(BaseModel):
    name: str
    step_type: str = Field(..., alias="stepType")
    step_id: str = Field(..., alias="stepId")
    parent_id: str = Field(..., alias="parentId")
    result_id: str = Field(..., alias="resultId")
    path: str
    path_ids: List[str] = Field(..., alias="pathIds")
    status: Status
    total_time_in_seconds: float = Field(..., alias="totalTimeInSeconds")
    started_at: str = Field(..., alias="startedAt")
    updated_at: str = Field(..., alias="updatedAt")
    inputs: List[NamedValue]
    outputs: List[NamedValue]
    data_model: str = Field(..., alias="dataModel")
    data: StepData
    has_children: bool = Field(..., alias="hasChildren")
    workspace: str
    keywords: List[str]
    properties: Dict[str, str]


class WebappMetaData(BaseModel):
    created: str
    id: str
    name: str
    shared: str
    type: str
    updated: str
    userId: str
    workspace: str
    policyIds: List[str] = []
    properties: Dict[str, str] = {}
    sharedEmails: List[str] = []

    class Config:
        # This will allow extra fields in the input data to be ignored
        extra = "ignore"


class LinqQueryFilter(BaseModel):
    queryStepsLinqFilter: dict = {}


class DataSettings(BaseModel):
    linqQueryFilter: LinqQueryFilter = LinqQueryFilter()


class WebappContent(BaseModel):
    version: str
    dataSource: str
    dataSettings: DataSettings = DataSettings()

    class Config:
        # This will allow extra fields in the input data to be ignored
        extra = "ignore"
