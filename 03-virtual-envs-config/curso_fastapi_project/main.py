from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import pytz
app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)

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
        "Thursday": "Jupyter",
        "Friday": "Venus",
        "Saturday": "Saturn"
    }
            
    message: str = f"Greetings from {astronomical_objects[weekday]}!"
    return {"message": message}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/time/{iso_code}")
async def time(iso_code: str)->dict[str, str]:

    iso = iso_code.upper().strip()
    
    # lookup timezones for country
    timezones: list[str]|None = pytz.country_timezones.get(iso)
    
    if not timezones:
        raise HTTPException(status_code=404, detail="Country code not found or has no timezones")
    
    # 3- Select a Specific Timezone
    target_timezone_name:str = timezones[0]
    
    try:
        # 4. Convert time using ZoneInfo
        # get the server time, then project it into target timezone
        current_time = datetime.now(ZoneInfo(target_timezone_name))
        
        return {
            "iso": iso,
            "timezone": target_timezone_name, # time zone name: e.g., America/Bogotá
            "day": current_time.strftime("%d"), # day of the month (01-31)
            "month": current_time.strftime("%B"), # Full month name (January)
            "year": current_time.strftime("%Y"), # year with century - 2026
            "hour": current_time.strftime("%H"), #  hour of the day, 24-hour clock (00 - 23)
            "minute": current_time.strftime("%M"), # minute of the hour 
            "second": current_time.strftime("%S"), # second of the minute
        }
    except ZoneInfoNotFoundError:
        raise HTTPException(status_code=404, detail="Timezone data missing from system")
