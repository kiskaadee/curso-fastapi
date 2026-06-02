import random
from datetime import datetime, timezone
from typing import Any, Dict, List

from models.business import (
    Customer,
    CustomerCreate,
    Envelope,
    Invoice,
    InvoiceCreate,
    Transaction,
    TransactionCreate,
)

mock_customer_db: Dict[int, Customer] = {}
mock_transaction_db: Dict[int, Transaction] = {}
mock_invoice_db: Dict[int, Invoice] = {}


## --- Customer controllers ---
def new_customer(customer_data: CustomerCreate) -> Customer:
    customer_id: int = generate_unique_id(mock_customer_db, 100000, 999999)
    customer = Customer(id=customer_id, **customer_data.model_dump())
    mock_customer_db[customer_id] = customer
    return customer


def fetch_customer(customer_id: int) -> Customer:
    customer: Customer | None = mock_customer_db.get(customer_id)
    if not customer:
        raise KeyError(f"Customer with ID {customer_id} not found")
    return customer


def list_customers() -> Envelope[Customer]:
    data: List[Customer] = list(mock_customer_db.values())
    return Envelope(data=data, total_count=len(data))


## --- Transaction controllers ---
def new_transaction(transaction_data: TransactionCreate):

    transaction_id: int = generate_unique_id(mock_transaction_db, 100000, 999999)
    timestamp: datetime = datetime.now(timezone.utc)
    transaction = Transaction(
        id=transaction_id, timestamp=timestamp, **transaction_data.model_dump()
    )

    if transaction.customer_id not in mock_customer_db:
        raise KeyError(f"Customer with ID {transaction.customer_id} not found")

    mock_transaction_db[transaction_id] = transaction
    return transaction


def fetch_transaction_list(customer_id: int) -> Envelope[Transaction]:

    if customer_id not in mock_customer_db:
        raise KeyError(f"Customer with id: {customer_id} not found.")

    data: List[Transaction] = [
        t for t in mock_transaction_db.values() if t.customer_id == customer_id
    ]

    return Envelope(data=data, total_count=len(data))


def fetch_transaction(customer_id: int, transaction_id: int) -> Transaction:
    transaction: Transaction | None = mock_transaction_db.get(transaction_id)

    if not transaction or transaction.customer_id != customer_id:
        raise KeyError(f"Transaction with ID {transaction_id} not found.")

    return transaction


### --- Invoice Controllers ---
def generate_invoice(invoice_data: InvoiceCreate) -> Invoice:
    customer: Customer = fetch_customer(invoice_data.customer_id)

    billing_transactions = [
        transaction
        for transaction in mock_transaction_db.values()
        if transaction.customer_id == invoice_data.customer_id
        and invoice_data.start_date <= transaction.timestamp <= invoice_data.end_date
    ]

    # this prevents empty invoices
    if not billing_transactions:
        raise ValueError(
            f"No transactions found by Customer id: {invoice_data.customer_id} in the specified range"
        )
    invoice_id: int = generate_unique_id(mock_invoice_db, 1000, 9999)

    # building the invoice object
    invoice = Invoice(
        id=invoice_id,
        customer=customer,
        transactions=billing_transactions,
        date_generated=datetime.now(timezone.utc),
        paid=False,
    )
    # database insertion
    mock_invoice_db[invoice_id] = invoice
    return invoice


def fetch_invoice(invoice_id: int, customer_id: int) -> Invoice:
    invoice: Invoice | None = mock_invoice_db.get(invoice_id)

    if not invoice or invoice.customer.id != customer_id:
        raise KeyError(
            f"Invoice with ID {invoice_id} not found or does not belong to this customer."
        )
    return invoice


# def generate_customer_id(db: Dict[int, Any]):
#     while True:
#         transaction_id: int = random.randint(100, 999)
#         if transaction_id not in db:
#             return transaction_id


# def generate_transaction_id(db: Dict[int, Any]):
#     while True:
#         transaction_id: int = random.randint(100, 999)
#         if transaction_id not in db:
#             return transaction_id


def generate_unique_id(database: Dict[int, Any], start: int, end: int):
    while True:
        new_id: int = random.randint(start, end)
        if new_id not in database:
            return new_id
