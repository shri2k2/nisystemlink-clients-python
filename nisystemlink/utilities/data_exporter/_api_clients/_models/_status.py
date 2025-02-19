from pydantic import BaseModel, Field

class Status(BaseModel):
    status_type: str = Field(..., alias="statusType")
    status_name: str = Field(..., alias="statusName")