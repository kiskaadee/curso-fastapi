# Virtual Environments & Your First Endpoint (The "Classic" Way)
> Date: 2026-05-19

In the last chapter, we cheated a bit using `uv` (the fancy new Rust tool). But in the real world, you'll run into plenty of projects using the "classic" `pip` and `venv` combo. This chapter is all about getting your hands dirty with the standard Linux workflow and finally seeing some JSON in the browser.

---

## 🐍 Part 1: The "Stay Clean" Workflow (Pip & Venv)

Modern Linux distros are picky. If you try to `pip install` something globally, you'll get hit with a **PEP 668** error ("externally-managed-environment"). Basically, your OS is saying: *"Don't mess with my Python, use a sandbox!"*

### 🛠️ The Setup
1. **Create the sandbox**: We're using `.curso-fastapi` as the folder name.
   ```bash
   python -m venv .curso-fastapi
   ```
2. **Step inside**: You have to "activate" it so your terminal knows which Python to use.
   ```bash
   source .curso-fastapi/bin/activate
   ```
3. **Install the goods**: 
   ```bash
   pip install "fastapi[standard]"
   ```
4. **Take a snapshot**: This creates the "recipe" for anyone else to replicate your setup.
   ```bash
   pip freeze > requirements.txt
   ```

**💡 Pro-tip**: You'll know you're "in" because your terminal prompt will usually show `(.curso-fastapi)`. If you close the terminal, you have to run the `source` command again!

---

## 🚀 Part 2: Hello, FastAPI!

We moved our code into a subfolder `curso_fastapi_project/` to keep things tidy. Here is the bare-bones version of an endpoint:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Root!"}
```

### How to run it?
Inside the folder, fire up the server:
```bash
fastapi dev main.py
```
Go to `http://127.0.0.1:8000` and boom! You've got your first API.

---

## 📖 Part 3: The "Magic" Documentation (OpenAPI)

One of the coolest things about FastAPI is that it writes the documentation **for you**. While your server is running, try these URLs:

1.  **Swagger UI** (`/docs`): An interactive page where you can actually "Try it out" and test your endpoints without leaving the browser.
2.  **Redoc** (`/redoc`): A cleaner, more "corporate" looking documentation.

Everything is generated automatically based on your code (this is thanks to the **OpenAPI** standard).

---

## 🧪 Bonus Track: The "Curiosity" Corner
*Things I added that weren't in the tutorial (yet), but made the demo cooler.*

### 1. The Frontend & The CORS "Wall"
I built a tiny `index.html` to fetch data from the API. But browsers have a security feature called **CORS** (Cross-Origin Resource Sharing). If your HTML file tries to talk to a server on a different port/address, the browser blocks it by default.

**The Fix**: I had to add some "CORS middleware" to `main.py` to tell the server: *"It's okay, let my local HTML file talk to you."* I used `"*"` to keep it simple for now, but I'll need to be more careful about security later!
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"],
    # ...
)
```

### 2. The Favicon Hack
Every time a browser hits your API, it asks for a `favicon.ico`. If you don't have one, your terminal gets spammed with `404 Not Found` errors.
I added a "silent" endpoint to handle this:
```python
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204) # 204 = "No Content", keeps it quiet.
```
*Note: `include_in_schema=False` hides this "utility" endpoint from your fancy Swagger docs.*

---

## ✅ Summary / Takeaways
The classic way is a bit more manual (**Create -> Activate -> Install**), but it's the bread and butter of Python development. Plus, we learned that FastAPI isn't just a server—it's an auto-documenting, frontend-friendly beast.

---

## 🏆 Challenge: The "What Time Is It?" Endpoint
*Goal: Create an endpoint that returns the current date and time.*

### 🛠️ The Implementation
I decided to go beyond a simple string and return a **structured JSON object**. This gives the frontend more freedom to display the information.

**Python Side (`main.py`):**
Used the `datetime` module and defined the endpoint as `async def`. It's better to get used to the async way early on!
```python
@app.get("/time")
async def time():
    current_time = datetime.now()
    return {
        "day": current_time.strftime("%d"),
        "month": current_time.strftime("%B"),
        "year": current_time.strftime("%Y"),
        "hour": current_time.strftime("%H"),
        "minute": current_time.strftime("%M"),
        "second": current_time.strftime("%S"),
    }
```

**Frontend Side (`index.html`):**
Keeping the JS minimal since we're focusing on the backend. The important part is how we fetch our new endpoint and pick the fields we need:
```javascript
// Fetching the time and formatting the display
await fetchAndDisplay('clock', 'time', (data) => {
    return `${data.day}/${data.month}/${data.year} - ${data.hour}:${data.minute}:${data.second}`;
});
```

### 🧠 Key Takeaways
1. **JSON is Automatic**: In FastAPI, if you return a Python `dict`, it's automatically converted to a JSON object. No manual `json.dumps()` needed!
2. **Give the frontend options**: Sending separate fields (day, month, hour) is much better than sending one big string. It lets whoever is using the API choose what to show and how.
3. **`strftime` is a lifesaver**: Python's `strftime` codes make it really easy to extract exactly the part of the date you want.
4. **FastAPI ❤️ Async**: Even for simple things, it's good practice to use `async def` to keep the server snappy.

