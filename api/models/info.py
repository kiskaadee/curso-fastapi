from pydantic import BaseModel

class TimeResponse(BaseModel):
    hour: str
    minute: str 
    seconds: str 
    meridian: str | None = None
