from pydantic import BaseModel, EmailStr, computed_field, field_validator
from datetime import datetime
import re

class CustomerBase(BaseModel):
    name: str
    description: str | None = None
    email: EmailStr
    age: int
    
    @field_validator("email")
    @classmethod
    def enforce_strict_email(cls, value: str) -> str:
        strict_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        
        if not re.match(strict_pattern, value):
            raise ValueError("Invalid email format. Only standard alphanumeric characters are permitted.")
        
        return value

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int | None = None

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
