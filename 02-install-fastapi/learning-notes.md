# Setting up with `uv` (The first try)
> Date: 2026-05-19

Starting the course, the first thing is getting the environment ready. Instead of the usual `pip` approach, I'm trying out `uv`. It's a Rust-based tool that's supposed to be much faster and handles everything (packages, venvs, and locks) in one go.

---

## 🛠️ Part 1: The Workflow
I used `uv` to scaffold the project. It's pretty straightforward:
1. **Initialize**: `uv init --app` creates the basic structure.
2. **Installation**: I went with `fastapi --extra standard`. This is important because the "slim" version doesn't include the development server or the CLI, so you'd end up installing those manually anyway.
3. **Running**: `uv run fastapi dev main.py`. 

**Note for later**: The `uv.lock` file is created automatically. It's basically a snapshot of the exact versions I'm using, which is good for avoiding "dependency hell" later on.

---

## 📦 Part 2: Standard vs. Slim
There was a bit of confusion at first about which version to install. 
- **`fastapi[standard]`**: This is the "batteries included" version. It comes with `uvicorn` (the server) and `pydantic`. 
- **`fastapi` (slim)**: Just the bare framework. 

I'm sticking with **standard** for this course because I want the `fastapi` CLI tool to work without extra configuration.

---

## 🚀 Part 3: Dev vs. Run
There's a distinction in how you start the server:
- **`fastapi dev`**: This is what I'll be using most of the time. It has hot-reload enabled, so the server restarts whenever I save a file.
- **`fastapi run`**: This is for production. No reload, just performance.

---

## 🧪 Bonus Track: Curiosity Corner
I ran `uv tree` just to see what happened. It shows a massive list of dependencies for something that's supposed to be "fast" and "minimal." It's interesting to see that FastAPI actually sits on top of `Starlette` (for the web parts) and uses `Pydantic` for all the data heavy-lifting.

---

## ✅ Summary / Takeaways
The setup with `uv` is definitely faster than the old `pip` way, but the main thing is that it handles the virtual environment and the lockfile for you. It's one less thing to worry about while learning the actual framework code.


