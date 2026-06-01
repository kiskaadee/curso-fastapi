from datetime import datetime

from fastapi import APIRouter, HTTPException, Response

from models.info import TimeResponse
from services.timezone import compute_date_data, compute_time_data, greet

info_router = APIRouter(tags=["System info"])


@info_router.get("/")
async def root():
    return {"message": "Server is running!"}


@info_router.get("/msg")
def message():
    return {"message": greet(datetime.now().weekday())}


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
        return compute_time_data(iso_code, format)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
