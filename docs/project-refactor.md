# Project Refactor & Migration Guide

As the course progressed, the codebase became incremental. To maintain a clean and professional structure, the repository was refactored to separate concerns.

## 🏗️ New Architecture

- **`api/`**: The backend logic. Consolidated all previous lessons into a single, scalable FastAPI application.
- **`ui/`**: The frontend playground. Decoupled from the backend folders to allow independent testing.
- **`learn/`**: Centralized lesson notes, moved from scattered directories into a dedicated documentation hub.

## 🔄 Migration Steps

The following steps were taken to migrate from the lesson-specific directories to the consolidated structure:

1. **Initialize a new `uv` project**:
   ```bash
   mkdir api && cd api
   uv init --app 
   ```

2. **Consolidate Code**:
   Moved `main.py` and logic from `03-virtual-envs-config` into `api/`.

3. **Dependency Management**:
   - Used `uv add -r requirements.txt` to migrate dependencies and locked the Python version to **3.13** for maximum compatibility.

   Python version troubleshooting:

   ```bash
   sed -i 's/requires-python = ">=3.14"/requires-python = ">=3.13"/' pyproject.toml # update pyproject.toml
   uv python pin 3.13
   uv lock --upgrade
   ```


4. **Documentation Migration**:
   Renamed `learning-notes.md` from old directories and moved them to `/learn` as standalone files for better readability.

## 🛠️ Tooling
- **UV**: Selected as the primary package manager for its speed and native virtual environment handling.
- **Python 3.13**: Locked as the project standard despite 3.14 availability, ensuring alignment with current library documentation.
