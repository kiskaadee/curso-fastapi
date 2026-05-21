from fastapi import APIRouter, HTTPException, Response
from datetime import datetime
from models.info import TimeResponse
from services.timezone import compute_date_data, compute_time_data

info_router = APIRouter(tags=["System info"])

@info_router.get("/")
async def root():
    return {"message": "Hello from Root!"}

@info_router.get("/msg")
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

@info_router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@info_router.get("/date/{iso_code}")
async def date(iso_code: str) -> dict[str, str]:
    try:
        return compute_date_data(iso_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@info_router.get("/time/{iso_code}", response_model=TimeResponse)
async def time(iso_code: str, format: str = "12h"):
    try:
        data = compute_time_data(iso_code, format)
        return TimeResponse(**data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
