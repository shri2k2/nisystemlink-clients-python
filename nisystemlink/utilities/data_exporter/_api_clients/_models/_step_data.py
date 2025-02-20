from typing import Dict, List

from pydantic import BaseModel


class StepData(BaseModel):
    text: str
    parameters: List[Dict[str, str]]
