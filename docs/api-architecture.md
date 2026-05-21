# API Architecture
> date: 2026-05-21
The `/api` directory follows a **Layered Architecture** designed to decouple presentation from business logic and configuration, facilitating independent testing and scalability.

## 🏗️ Directory Structure

```bash
api/
├── main.py            # Clean Orchestrator & App Factory
├── core/              # Configuration & Environment
│   └── config.py      # Pydantic-settings based configuration
├── models/            # Pure Pydantic Data Contracts (Schemas)
│   ├── info.py        # System and utility models
│   └── business.py    # Domain-specific models (Customer, Invoice, etc)
├── services/          # Pure Business Logic
│   └── timezone.py    # Timezone computations and lookups
├── routers/           # Presentation Layer (FastAPI APIRouters)
│   ├── info.py        # System info endpoints
│   └── business.py    # Business domain endpoints
└── tests/             # Automated Testing Suite (Pytest)
    ├── conftest.py    # Shared fixtures (TestClient)
    ├── test_services.py # Unit tests for business logic
    └── test_routes.py   # Integration tests for HTTP endpoints
```

## 🧩 Key Components

### 1. The Clean Orchestrator (`main.py`)
`main.py` is strictly used for bootstrapping the application. It uses a factory pattern to initialize the app and mount routers.

```python
from fastapi import FastAPI
from core.config import settings
from routers.info import info_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    # ... middleware setup ...
    app.include_router(info_router)
    return app

app = create_app()
```

### 2. Services Layer
The logic is extracted into pure Python functions that return standard types or Pydantic models. They raise standard Python exceptions which are then handled by the routers.

### 3. Testing Strategy
We use `pytest` for two levels of testing:
- **Unit Testing**: Testing the `services/` layer in isolation without an HTTP server.
- **Integration Testing**: Using FastAPI's `TestClient` to test the `routers/` layer end-to-end.

To run tests:
```bash
cd api
uv run pytest
```
