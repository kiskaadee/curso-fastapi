from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
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
