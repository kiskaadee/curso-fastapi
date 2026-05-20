# Lesson 3: Virtual Environments & First Endpoint
> Date: 2026-05-19

While `uv` is cool, knowing the "classic" `pip` and `venv` workflow is essential for most real-world projects.

---

## 🐍 Part 1: The "Classic" Workflow (Pip & Venv)
Modern Linux distros block global `pip install` to protect the OS (**PEP 668**). We must use a sandbox!

1. **Create**: `python -m venv .venv`
2. **Activate**: `source .venv/bin/activate`
3. **Install**: `pip install "fastapi[standard]"`
4. **Snapshot**: `pip freeze > requirements.txt`

## 🚀 Part 2: Hello, FastAPI!
The bare-bones code for our first API:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Root!"}
```

---

## 🧪 Bonus Track: The "Curiosity" Corner
### 1. The CORS "Wall"
I built a tiny `index.html` to fetch data. Browsers block different origins by default.
**The Fix**: Adding CORS middleware. *"It's okay, let my local HTML file talk to you."*

### 2. The Favicon Hack
Browsers ask for `favicon.ico` on every hit. To avoid `404` spam in the logs, I added a silent `204 No Content` endpoint.

---

## ✅ Summary / Takeaways
The classic way is a bit more manual, but it's the bread and butter of Python development. We learned that FastAPI isn't just a server—it's a frontend-friendly beast.
