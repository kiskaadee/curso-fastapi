from fastapi import FastAPI
from random import randint as ri
app = FastAPI()

@app.get("/")
def read_root():
    return "FastAPI is installed"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: int | None = None):
    return {"item_id": item_id, "q": ri(1,10)}