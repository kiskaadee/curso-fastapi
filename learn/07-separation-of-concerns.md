# Clase 7: Separation of Concerns (Routers, Services & DTOs)
> Date: 2026-06-01

Building on the refactor from Lesson 6, we have now fully embraced a **Three-Layer Architecture**. This lesson is about drawing clear lines in the sand: where does validation end, and where does business logic begin?

---

## 🏗️ The Three Pillars of our API
Instead of stuffing everything into `main.py`, we've decoupled the application into specialized modules. This makes the code testable, maintainable, and "production-ready."

### 1. Models (The Contract) 📜
The **Contract Layer**. We use Pydantic to enforce data integrity at the door. If the data doesn't match our "blueprint," it never even reaches our business logic.
- **Pattern used**: **DTO (Data Transfer Object)**. We split schemas into `Base`, `Create`, and storage models (e.g., `Customer`).
- **Validation**: Using `@field_validator` for custom logic (like strict email regex) and `@model_validator` for cross-field checks (like ensuring `start_date < end_date`).

### 2. Services (The Logic) ⚙️
The **Domain Layer**. This is where the actual "work" happens (e.g., calculating totals, managing the in-memory "database").
- **Pure Python**: This layer knows *nothing* about HTTP, status codes, or FastAPI. It only cares about Python data structures and standard exceptions (`ValueError`, `KeyError`).
- **Simulated DB**: Since we aren't using a real database yet, we manage state using in-memory lists (e.g., `db_customers: list[Customer]`).

### 3. Routers (The Presentation) 🌐
The **Interface Layer**. These are the "gatekeepers" of our API.
- **Mapping**: Their only job is to receive HTTP requests, call the appropriate Service, and map the results (or errors) to the correct HTTP response.
- **Error Handling**: If a Service raises a `ValueError`, the Router catches it and translates it into a `400 Bad Request` or `404 Not Found`.

---

## 🛡️ Implementing Strict Email Validation
While Pydantic's `EmailStr` is great, sometimes you need even stricter rules. We implemented a custom validator to ensure emails don't contain "weird" characters, using the `@field_validator` decorator.

```python
@field_validator("email")
@classmethod
def enforce_strict_email(cls, value: str) -> str:
    strict_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(strict_pattern, value):
        raise ValueError("Invalid email format. Strict alphanumeric required.")
    return value
```

---

## 🔄 Separating Input from Output (`response_model`)
One of the most powerful features of FastAPI is the `response_model` parameter in the decorator. It allows us to receive one shape of data but return another.

```python
# The request body uses CustomerCreate (No ID required from the user)
# The response uses Customer (Includes the auto-generated ID)
@business_router.post("/customer", response_model=Customer, status_code=201)
async def create_customer(customer_data: CustomerCreate):
    # The router calls the service, which returns a model with an ID
    new_customer = customer_service.save(customer_data) 
    return new_customer
```

---

## ✅ Summary / Takeaways
1. **Contract Enforcement**: Pydantic isn't just "advice"—it's a runtime shield that rejects bad data before it hits your logic.
2. **Decoupling is Freedom**: By keeping Services ignorant of HTTP, you could technically run your logic in a CLI or a background script without changing a single line of business code.
3. **Routers are Translators**: Keep them thin. Their job is to translate "Web speak" (JSON/HTTP) into "Python speak" (Models/Exceptions) and back again.
