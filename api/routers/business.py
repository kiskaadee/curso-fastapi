from fastapi import APIRouter, Response
from models.business import Customer, Transaction, InvoiceCreate

business_router = APIRouter(tags=["Business"])

@business_router.post("/customer")
async def create_customer(customer_data: Customer):
    # to-do
    return Response(status_code=201)

@business_router.get("/customer/{customer_id}")
async def get_customer(customer_id: int):
    # to-do
    return Response(status_code=200)

@business_router.post("/transaction")
async def create_transaction(transaction_data: Transaction):
    # to-do
    return Response(status_code=201)

@business_router.post("/invoice")
async def create_invoice(invoice_data: InvoiceCreate):
    # to-do
    return Response(status_code=201)
