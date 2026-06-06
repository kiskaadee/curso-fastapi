from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from config.database import SessionDependency
from models.customers import CustomerCreate, CustomerPublic
from models.types import Envelope
from services.customers import fetch_customer, list_customers, new_customer

customer_router = APIRouter(tags=["Customers"])
# --- CUSTOMERS ---


@customer_router.post("/customers", response_model=CustomerPublic, status_code=201)
async def create_customer(customer_data: CustomerCreate, session: SessionDependency):
    return new_customer(customer_data)


@customer_router.get("/customers", response_model=Envelope[CustomerPublic])
async def get_all_customers():
    return list_customers()


@customer_router.get("/customers/{customer_id}", response_model=CustomerPublic)
async def get_customer_by_id(customer_id: int):
    try:
        return fetch_customer(customer_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
