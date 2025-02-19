from nisystemlink.utilities.data_exporter._api_clients._models._status import Status

from typing import Dict, List

from pydantic import BaseModel, Field

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