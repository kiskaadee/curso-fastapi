from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

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
    return {"message": "Don't tell anyone!"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/time")
async def time():
    current_time = datetime.now()
    return {
        "day": current_time.strftime("%d"),
        "month": current_time.strftime("%B"), # Full month name (e.g., "May")
        "year": current_time.strftime("%Y"),
        "hour": current_time.strftime("%H"),
        "minute": current_time.strftime("%M"),
        "second": current_time.strftime("%S"),
    }
