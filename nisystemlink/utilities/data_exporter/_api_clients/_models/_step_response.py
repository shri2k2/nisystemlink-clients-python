from nisystemlink.utilities.data_exporter._api_clients._models._status import Status
from nisystemlink.utilities.data_exporter._api_clients._models._named_value import NamedValue
from nisystemlink.utilities.data_exporter._api_clients._models._step_data import StepData

from typing import Dict, List

from pydantic import BaseModel, Field

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