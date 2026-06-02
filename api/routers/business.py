from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from models.business import (
    Customer,
    CustomerCreate,
    Envelope,
    Invoice,
    InvoiceCreate,
    Transaction,
    TransactionCreate,
)
from services.business import (
    fetch_customer,
    fetch_invoice,
    fetch_transaction,
    fetch_transaction_list,
    generate_invoice,
    list_customers,
    new_customer,
    new_transaction,
)

business_router = APIRouter(tags=["Business"])


#        --- CUSTOMERS ---
# --- CUSTOMERS ---
@business_router.post("/customers", response_model=Customer, status_code=201)
async def create_customer(customer_data: CustomerCreate):
    return new_customer(customer_data)


@business_router.get("/customers", response_model=Envelope[Customer])
async def get_all_customers():
    return list_customers()


@business_router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer_by_id(customer_id: int):
    try:
        return fetch_customer(customer_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=e.args[0])


#       --- TRANSACTIONS ---
@business_router.post("/transactions", response_model=Transaction, status_code=201)
async def create_transaction(transaction_data: TransactionCreate):
    try:
        return new_transaction(transaction_data)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@business_router.get(
    "/customers/{customer_id}/transactions", response_model=Envelope[Transaction]
)
async def get_all_customer_transactions(customer_id: int):
    try:
        return fetch_transaction_list(customer_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@business_router.get(
    "/customers/{customer_id}/transactions/{transaction_id}",
    response_model=Transaction,
)
async def get_transaction_by_id(customer_id: int, transaction_id: int):
    try:
        return fetch_transaction(customer_id, transaction_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=e.args[0])


#       --- INVOICES ---
@business_router.post("/invoices", response_model=Invoice, status_code=201)
async def create_invoice(invoice_data: InvoiceCreate):
    try:
        return generate_invoice(invoice_data)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@business_router.get(
    "/customers/{customer_id}/invoices/{invoice_id}", response_model=Invoice
)
async def get_invoice_by_id(customer_id: int, invoice_id: int):
    try:
        return fetch_invoice(invoice_id, customer_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
