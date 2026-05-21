from pydantic import BaseModel, EmailStr, computed_field
from datetime import datetime

class Customer(BaseModel):
    name: str
    description: str | None = None
    email: EmailStr
    age: int
   
class Transaction(BaseModel):
    id: int
    amount: int
    description: str
    timestamp: datetime

class InvoiceCreate(BaseModel):
    customer_id: int
    transactions: list[Transaction]

class InvoiceResponse(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]

    @computed_field
    @property
    def total_amount(self)-> int:
        return sum(t.amount for t in self.transactions)
