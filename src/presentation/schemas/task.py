from pydantic import BaseModel


class TaskFilterByGeoQuerySchema(BaseModel):
    long: float
    lat: float
