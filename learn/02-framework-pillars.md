# Lesson 2: Framework Pillars & Modern Tooling
> Date: 2026-05-19

FastAPI isn't built from scratch; it stands on the shoulders of giants. This makes it fast, reliable, and easy to use.

---

## 🏛️ The Two Pillars
1.  **Starlette**: Handles all the HTTP requests and async magic.
2.  **Pydantic**: Handles the data modeling and validation.

## 🛠️ Modern Tooling: `uv` (The first try)
Instead of the usual `pip`, I'm trying out `uv`. It's a Rust-based tool that handles everything—packages, venvs, and locks—much faster.

- **`uv init --app`**: Scaffolds the basic project.
- **`fastapi[standard]`**: The "batteries included" version with `uvicorn` and the CLI.
- **`fastapi` (slim)**: Just the bare framework.

## 🚀 Dev vs. Run
- **`fastapi dev`**: For local coding (has hot-reload).
- **`fastapi run`**: For production (maximum performance).

## 📖 OpenAPI & Documentation
FastAPI generates an **OpenAPI** JSON file automatically. This powers:
- **Swagger UI** (`/docs`): Where you can "Try it out" interactively.
- **Redoc** (`/redoc`): A cleaner, corporate view.

---

## 🧪 Bonus Track: Curiosity Corner
I ran `uv tree` and saw that FastAPI sits on top of `Starlette` and `Pydantic`. It's interesting to see how these libraries work together to make our lives easier.

---

## ✅ Summary / Takeaways
The setup is fast, and the automatic documentation is a lifesaver. Using modern tools like `uv` makes the developer experience much smoother.
