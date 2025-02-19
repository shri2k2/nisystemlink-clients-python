from typing import Union

from pydantic import BaseModel

class NamedValue(BaseModel):
    name: str
    value: Union[str, float, int]