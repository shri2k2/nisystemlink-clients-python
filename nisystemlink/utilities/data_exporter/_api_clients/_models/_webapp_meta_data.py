from typing import Dict, List

from pydantic import BaseModel


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
