# Clase 8: Database Integration, SQLModel & Lifecycle Management

> Date: 2026-06-06

This lesson marked the transition from in-memory dictionaries to persistent database architecture. We explored how FastAPI manages resource lifecycles, how to bridge the gap between data validation and database schemas using SQLModel, and how to handle sensitive data securely.

---

## ⏸️ 1. Lifecycle Management: `with` and `yield`

Coming from Express/Node.js, resource management (like database connections) often relies on manual setup/teardown or complex middleware. Python and FastAPI solve this elegantly using **Context Managers** and **Generators**.

* **`with` (The Context Manager):** A wrapper that guarantees safe setup and teardown. When the execution leaves the `with` block, the resource is automatically closed, preventing memory leaks and exhausted connection pools.
* **`yield` (The Pause Button):** Turns a standard function into a Generator. Instead of `return` (which hands over data and destroys the function's state), `yield` hands over data and **pauses** execution.

### FastAPI Dependency Injection (`SessionDependency`):
By combining these two, we created a bulletproof database session manager:

1. `with Session()` opens the database connection.
2. `yield session` hands the connection to the FastAPI router and *pauses*.
3. The router does its work and sends the HTTP response.
4. The generator *unpauses*, the `with` block ends, and the database connection closes automatically.

---

## 🧬 2. SQLModel: The Single Source of Truth (SSOT)

Created by the author of FastAPI, `SQLModel` solves the code duplication problem between Pydantic (data validation) and SQLAlchemy (database ORM).

* **The Magic:** Under the hood, every `SQLModel` class inherits from Pydantic's `BaseModel`.
* **Validation intact:** We do not lose runtime validation. Custom `@field_validator` decorators work exactly as they did before.
* **Dual-Nature:** By simply adding `table=True` to the class definition, the exact same model that validates HTTP requests can generate `CREATE TABLE` SQL statements.

---

## 🏗️ 3. The Multiple Models Pattern

While `SQLModel` reduces boilerplate, using a single class for everything couples the API HTTP contract directly to the database infrastructure, risking violations of the Single Responsibility Principle (SRP). To maintain clean architecture, we implemented the **Multiple Models Pattern** via inheritance:

1. **`CustomerBase`**: The pure data contract (no `table=True`).
2. **`CustomerCreate` & `CustomerPublic`**: The API schemas (Input/Output).
3. **`Customer(table=True)`**: The infrastructure schema. This is the *only* model that interacts with the database or knows about primary keys and hashed passwords.

This pattern ensures that if we migrate from SQLite to MongoDB in the future, our API schemas and routers remain completely untouched.

---

## 🔐 4. Security: `SecretStr` and Safe Serialization

Handling user passwords requires strict defensive programming to prevent accidental leaks in terminal logs, error traces, or API responses.

* **Pydantic's `SecretStr`:** By typing the password as `SecretStr` in `CustomerCreate`, Pydantic masks the value (e.g., `**********`) when the object is printed or logged. To run validation or hash it, we must explicitly call `.get_secret_value()`.
* **Safe Database Injection:** In the service layer, we must separate the raw API payload from the database object. We exclude the raw password from the dump and inject the hashed version:

```python
db_customer = Customer(
    hashed_password=get_password_hash(raw_password),
    **customer_data.model_dump(exclude={"password"})
)
```

* **Safe Serialization (`.model_validate`)**: To return data to the user, we pass the raw database object into `CustomerPublic.model_validate(db_customer)`. Because `CustomerPublic` does not contain a `hashed_password` attribute, Pydantic automatically strips the sensitive data before generating the JSON response.

---

## ✅ Summary / Takeaways
1. **Lifecycle Control**: `yield` is more than just a return; it's a way to manage resources safely across the entire request/response cycle.
2. **Reduced Duplication**: `SQLModel` bridges Pydantic and SQLAlchemy, but we still use inheritance to keep API and DB concerns separate.
3. **Security by Default**: Using `SecretStr` and explicit serialization patterns prevents sensitive data from ever leaking into logs or responses.
