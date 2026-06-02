import re
from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    computed_field,
    field_validator,
    model_validator,
)
from pydantic.fields import Field


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
            raise ValueError(
                "Invalid email format. Only standard alphanumeric characters are permitted."
            )

        return value


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int


## --- Transaction Models ---
class TransactionBase(BaseModel):
    # id: int  # enforced
    amount: int = Field(gt=0)
    customer_id: int
    description: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    timestamp: datetime
    id: int


## --- Invoice Models ---
class InvoiceBase(BaseModel):
    customer_id: int
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def check_date_order(self) -> "InvoiceBase":
        if self.start_date >= self.end_date:
            raise ValueError("The start date must be strictly before the end date.")
        return self


class InvoiceCreate(InvoiceBase):
    pass


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    date_generated: datetime
    paid: bool

    @property
    @computed_field
    def total_amount(self) -> int:
        return sum(t.amount for t in self.transactions)
