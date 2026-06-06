import re

from pydantic import EmailStr, SecretStr, field_validator
from sqlmodel import Field, SQLModel


class CustomerBase(SQLModel):
    """
    Base Model: Pure Data Contract to enforce Pydantic Validation
    SQLModel objects also inherit properties from BaseModel, and hence
    the Pydantic data validation capabilities
    """

    name: str
    description: str
    email: EmailStr
    age: int

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(email_pattern, value):
            raise ValueError("Invalid email address.")
        return value


class CustomerCreate(CustomerBase):
    """
    API Input: Expects a raw password.
    Uses SecretStr to prevent accidental logging of plain-text passwords.
    """

    password: SecretStr

    @field_validator("password")
    @classmethod
    def validate_password_strenght(cls, value: SecretStr) -> SecretStr:
        # Pydantic validation run on the SecretStr object, so we must extract the string first
        raw_password = value.get_secret_value()
        if len(raw_password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Additional validation walls if needed
        return value


class CustomerPublic(CustomerBase):
    """
    API Output: Hides sensitive DB columns, include ID
    """

    id: int


class Customer(CustomerBase, table=True):
    """
    Database Table (infrastructure): This is the ONLY model that knows about relational databases.
    """

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
