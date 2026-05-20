# Clase 5: Pydantic Schemas & POST Endpoints
> Date: 2026-05-20

To build dynamic and secure endpoints, it's essential to validate the information we receive—especially when it's sent in the request body. Users can easily enter incorrect or malformed data (like a typo in an email address), and catching those errors early is crucial for keeping the API running smoothly. 

FastAPI makes this really easy through **Pydantic**, which lets us build robust data models to act as a shield for our server.

---

## 🏗️ Creating a Data Model
When a user sends us information (like creating a new account), we can't just trust that they'll send the right stuff. We use a **Schema** to define exactly what we expect.

I created a `Customer` model using Pydantic's `BaseModel`:
```python
from pydantic import BaseModel

class Customer(BaseModel):
    name: str
    description: str | None = None # This one is optional!
    email: str
    age: int
```

## 📮 The POST Endpoint
To create a new resource, the REST standard says we should use the **POST** method. 

**Python Side (`api/main.py`):**
```python
@app.post("/customer")
async def create_customer(customer_data: Customer):
    # For now, we just acknowledge receipt
    # In the future, we'll save this to a database!
    return Response(status_code=201)
```

## 🧪 Testing and Validation
FastAPI's `/docs` page is a lifesaver here. 
1.  **Try it out**: You can fill in the JSON fields directly.
2.  **Automatic Validation**: If I try to send a string where an integer should be (like `"old"` for `age`), FastAPI automatically stops the request and sends back a `422 Unprocessable Entity` error. It even tells the user exactly which field they messed up!

---

## 🧠 Key Takeaways
1.  **Pydantic = Security**: By defining a `BaseModel`, we ensure that our code never touches "dirty" or malformed data.
2.  **Status Codes**: 
    - `201 Created`: The correct response for a successful POST request.
    - `422 Unprocessable Entity`: What FastAPI sends when the user's data doesn't match our schema.
3.  **Optional Fields**: Using `str | None = None` lets us have fields that the user doesn't *have* to provide.
4.  **Documentation is Free**: Since we used a Pydantic model, the Swagger UI shows the exact JSON structure the user needs to send. No more guessing!

---

## ✅ Summary / Takeaways
Moving from URL parameters to Request Bodies is a big step. Pydantic makes it feel natural and safe by handling all the boring validation logic for us.
