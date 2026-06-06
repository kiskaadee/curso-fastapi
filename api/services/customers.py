from typing import Dict, List

from models.customers import Customer, CustomerCreate, CustomerPublic
from models.types import Envelope
from services.utils import generate_unique_id

# TO-DO: replace dummy logic with actual SQLite3 implementation
mock_customer_db: Dict[int, Customer] = {}


def get_password_hash(password: str) -> str:
    """Dummy hashing function for educational purposes"""
    return f"hashed_{password}123"


## --- Customer controllers ---
def new_customer(customer_data: CustomerCreate) -> CustomerPublic:

    customer_id: int = generate_unique_id(mock_customer_db, 100000, 999999)
    # 1 - Extract raw password from SecretStr
    raw_password: str = customer_data.password.get_secret_value()

    # 2 - Hash it securely on the server
    hashed_wp: str = get_password_hash(raw_password)

    # 3 - Create the Database Model
    # We must exclude the raw password from the model_dump,
    # and manually inject the hashed one
    db_customer = Customer(
        id=customer_id,
        hashed_password=hashed_wp,
        **customer_data.model_dump(exclude={"password"}),
    )

    mock_customer_db[customer_id] = db_customer
    return CustomerPublic.model_validate(db_customer)


def fetch_customer(customer_id: int) -> CustomerPublic:
    db_customer: Customer | None = mock_customer_db.get(customer_id)

    if not db_customer:
        raise KeyError(f"Customer with ID {customer_id} not found.")

    return CustomerPublic.model_validate(db_customer)


def list_customers() -> Envelope[CustomerPublic]:
    data: List[CustomerPublic] = [
        CustomerPublic.model_validate(customer)
        for customer in mock_customer_db.values()
    ]

    return Envelope(data=data, total_count=len(data))
