# Clase 6: Data Modeling & Connections
> Date: 2026-05-20

In this lesson, the course instructed us to take all our Pydantic `BaseModel` classes out of `main.py` and move them into a dedicated `models.py` file. I wanted to understand *why* we were doing this, so I did some digging. 

This led me to learn about **Layered (N-Tier) Architecture** and the importance of decoupling code.

---

## 🧹 Understanding Layered Architecture
By moving `Customer` and `TimeResponse` to `models.py`, we are organizing the codebase by responsibility. 

This decoupling is critical: now, `main.py` is strictly responsible for routing HTTP requests (the presentation layer), and `models.py` acts as the definitive "blueprint" for all data shapes. Keeping these concerns separate prevents tightly coupled code and makes the application much easier to maintain as it grows.

```python
# In api/main.py, we now just import what we need:
from models import TimeResponse, Customer, Transaction, InvoiceCreate, InvoiceResponse
```

---

## 📧 The `EmailStr` Upgrade
While looking at the `Customer` model, I realized that defining `email: str` isn't very safe. Someone could easily pass `"not-an-email"` and the API would accept it.

Because we are already using Pydantic, the fix was incredibly easy. By importing `EmailStr`, Pydantic handles all the complex regex validation for us!

```python
from pydantic import BaseModel, EmailStr

class Customer(BaseModel):
    name: str
    description: str | None = None
    email: EmailStr # 🛡️ Automatically rejects invalid email formats!
    age: int
```

---

## 🔗 Connecting Models (The DTO Pattern)
Next, I needed to create `Transaction` and `Invoice` models. This is where things get interesting because an Invoice needs to *relate* to a Customer and a list of Transactions.

I learned about the **DTO (Data Transfer Object)** pattern. Basically, the data we *receive* to create an invoice is different from the data we want to *return* to the user.

### 1. What we receive (`InvoiceCreate`)
When a client creates an invoice, they don't send the entire Customer object, just the ID.
```python
class InvoiceCreate(BaseModel):
    customer_id: int
    transactions: list[Transaction]
```

### 2. What we return (`InvoiceResponse`)
When we respond, we want to give the frontend the full picture, including the populated `Customer` object and the calculated total.
```python
class InvoiceResponse(BaseModel):
    id: int
    customer: Customer # Nested model!
    transactions: list[Transaction]
```

---

## 🧮 Computed Fields
An invoice isn't very useful without a total amount. Instead of forcing the frontend to add up the transactions, I added a calculated field directly to the `InvoiceResponse` model.

```python
from pydantic import computed_field

class InvoiceResponse(BaseModel):
    # ... previous fields ...

    @computed_field 
    @property
    def total_amount(self) -> int:
        return sum(t.amount for t in self.transactions)
```
- **`@property`**: This Python decorator makes the method act like a normal attribute. You can access it as `invoice.total_amount` instead of `invoice.total_amount()`.
- **`@computed_field`**: This tells Pydantic to include this calculated property when it converts the object into JSON for the API response.

---

## 🛠️ Gotchas & Operational Notes
* **Circularity Checks**: When nesting schemas (like placing `Customer` inside `InvoiceResponse`), ensure the dependent models are declared higher up in the same script or cleanly resolved via forward references to avoid `NameError` execution traps during module parsing.
* **Response Mapping**: Remember to explicitly attach `response_model=InvoiceResponse` to your future `/invoice` fetch implementations to ensure the `@computed_field` engine executes during serialization.

---

## ✅ Summary / Takeaways
1. **Organization matters**: Splitting routing (`main.py`) and data structures (`models.py`) makes the code much easier to read and maintain.
2. **Pydantic is powerful**: Features like `EmailStr` and `@computed_field` save us from writing dozens of lines of manual validation and serialization logic.
3. **Input != Output**: Using the DTO pattern (separating `Create` models from `Response` models) gives us total control over what data is required vs. what data is exposed.
