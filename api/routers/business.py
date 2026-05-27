from fastapi import APIRouter, Response
import models.business as bsch # import all business schemas

business_router = APIRouter(tags=["Business"])

#        --- CUSTOMERS ---
@business_router.post("/customer", response_model=bsch.Customer, status_code=201)
async def create_customer(customer_data: bsch.CustomerCreate):
    """
    
    """
    # to-do
    return customer_data

@business_router.get("/customer/{customer_id}")
async def get_customer(customer_id: int):
    # to-do
    return Response(status_code=200)


#       --- TRANSACTIONS ---
@business_router.post("/transaction")
async def create_transaction(transaction_data: bsch.Transaction):
    # to-do
    return Response(status_code=201)



#       --- INVOICES ---
@business_router.post("/invoice")
async def create_invoice(invoice_data: bsch.InvoiceCreate):
    # to-do
    return Response(status_code=201)
