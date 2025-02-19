from pydantic import BaseModel


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
