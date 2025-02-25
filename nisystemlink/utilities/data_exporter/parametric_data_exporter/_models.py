from pydantic import BaseModel


class QueryLinqFilter(BaseModel):
    filter: str
    result_filter: str
