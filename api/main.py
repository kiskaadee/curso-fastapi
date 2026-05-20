from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from pydantic import BaseModel
import pytz

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)

class TimeResponse(BaseModel):
    hour: str
    minute: str 
    seconds: str 
    meridian: str | None = None
    
def lookup_timezone(iso_code: str)->ZoneInfo:
    if len(iso_code) != 2:
        raise HTTPException(status_code=400, detail="Invalid ISO code format.")
    iso:str = iso_code.upper().strip()
    
    timezones: list[str] | None = pytz.country_timezones.get(iso)
    
    if not timezones:
        raise HTTPException(status_code=404, detail="Country code not found or has no timezones.")

    target_timezone_name: str = timezones[0]
    
    try:
        return ZoneInfo(target_timezone_name)
    except ZoneInfoNotFoundError:
        raise HTTPException(status_code=500, detail="Timezone data missing on server.")

@app.get("/")
async def root():
    return {"message": "Hello from Root!"}

@app.get("/msg")
def message():
    weekday = datetime.now().strftime("%A")
    
    astronomical_objects = {
        "Sunday": "the Sun",
        "Monday": "the Moon",
        "Tuesday": "Mars",
        "Wednesday": "Mercury",
        "Thursday": "Jupiter",
        "Friday": "Venus",
        "Saturday": "Saturn"
    }
            
    msg: str = f"Greetings from {astronomical_objects[weekday]}!"
    return {"message": msg}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/date/{iso_code}")
async def date(iso_code: str) -> dict[str, str]:
    timezone_object: ZoneInfo = lookup_timezone(iso_code)
    current_time: datetime = datetime.now(timezone_object)
    return {
        "iso": iso_code.upper(),
        "day": current_time.strftime("%d"),
        "month": current_time.strftime("%B"),
        "year": current_time.strftime("%Y"),
    }

@app.get("/time/{iso_code}", response_model=TimeResponse)
async def time(iso_code: str, format: str = "12h"):
    allowed_timeformat = ["12h", "24h"]
    if format not in allowed_timeformat:
        raise HTTPException(
            status_code=400,
            detail="Time format not supported. Enter '12h' or '24h'",
        )

    timezone_object: ZoneInfo = lookup_timezone(iso_code)
    current_time: datetime = datetime.now(timezone_object)

    match format:
        case "12h":
            return TimeResponse(
                hour=current_time.strftime("%I"),
                minute=current_time.strftime("%M"),
                seconds=current_time.strftime("%S"),
                meridian=current_time.strftime("%p")
            )
        case "24h":
            return TimeResponse(
                hour=current_time.strftime("%H"),
                minute=current_time.strftime("%M"),
                seconds=current_time.strftime("%S"),
                meridian=None
            )
        case _:
            raise HTTPException(status_code=400, detail="Invalid time format reached structural match.")
