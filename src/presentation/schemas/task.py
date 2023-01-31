from pydantic import BaseModel, root_validator


class TaskFilterQuerySchema(BaseModel):
    long: float | None = None
    lat: float | None = None

    @root_validator(pre=True)
    def check_values(cls, values: dict) -> dict:  # noqa
        long, lat = values.get("long"), values.get("lat")
        if (long and not lat) or (lat and not long):
            raise ValueError("lat и long должны передаваться вместе")
        return values
