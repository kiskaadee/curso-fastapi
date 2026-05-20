# Lesson 4: Dynamic Endpoints (Path Parameters)
> Date: 2026-05-20

Static endpoints are easy, but real APIs need to be dynamic. We evolved our time endpoint to handle different countries using **Path Parameters**.

---

## 🌎 The "What Time Is It?" Challenge
*Goal: Create an endpoint that returns the time for a specific country.*

### 🛠️ The Implementation
Instead of just `/time`, we use `/time/{iso_code}`.

**Python Side (`main.py`):**
```python
@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper().strip()
    
    # Using pytz to find the timezone for that country
    timezones = pytz.country_timezones.get(iso)
    
    if not timezones:
        raise HTTPException(status_code=404, detail="Country code not found")
    
    target_tz = timezones[0]
    current_time = datetime.now(ZoneInfo(target_tz))
    
    return {
        "iso": iso,
        "timezone": target_tz,
        "day": current_time.strftime("%d"),
        "hour": current_time.strftime("%H"),
        # ...
    }
```

### 🧠 Key Takeaways
1. **The `{}` trick**: Putting a variable in the route makes it dynamic. It's like passing an argument to a function through the URL.
2. **Typing matters**: Adding `: str` gives us autocompletion and lets FastAPI handle basic validation.
3. **Normalization**: Using `.upper().strip()` makes the API robust against messy user input.
4. **`strftime` is a lifesaver**: It's really easy to extract exactly the part of the date you want.
5. **JSON is still automatic**: No manual conversion needed!

---

## 🧪 Bonus Track: Curiosity Corner
I updated `/msg` to return a greeting from an astronomical object based on the day of the week. It was a fun way to practice dictionary lookups and f-strings!

---

## ✅ Summary / Takeaways
Path parameters open the door to building flexible APIs. FastAPI handles the heavy lifting of turning URL variables into Python arguments seamlessly.


## 🏆 Challenge: Formatting the Time
*Goal: Create an endpoint that receives a query parameter (like `?format=24h`) so the user can choose the time format.*

### 🛠️ The Resolution: Query Parameters & Better Code
We added **Query Parameters** and used **Pydantic** to keep our data organized.

**Python Side (`api/main.py`):**
```python
class TimeResponse(BaseModel):
    hour: str
    minute: str 
    seconds: str 
    meridian: str | None = None

@app.get("/time/{iso_code}", response_model=TimeResponse)
async def time(iso_code: str, format: str = "12h"):
    # ... logic ...
```

### 🧠 Key Takeaways
1. **Path vs. Query**:
   - **Path (`/time/CO`)**: Identifies "Where".
   - **Query (`?format=24h`)**: Configures "How".
2. **Pydantic Models**: Using `BaseModel` makes the API safer and generates better documentation.
3. **Error Codes are communication**:
   - `400`: Bad request (wrong format).
   - `404`: Not found (wrong country).
   - `500`: Server error (missing data).
4. **Type Checking**: Clean code leads to a happy developer.

---

## ✅ Summary / Takeaways
Type hints in FastAPI aren't just for show—they drive validation and documentation. Switching to Pydantic makes our API professional and reliable.
