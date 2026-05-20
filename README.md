# Platzi: Curso de FastAPI - Personal Implementation

This repository contains my personal implementation and learning notes for the **FastAPI Development Course** from Platzi.

## 📂 Repository Structure

The project is organized into several key directories to separate the application code, the playground, and the learning documentation:

- **[`/api`](./api)**: The core FastAPI backend. This contains the consolidated API implementation with all endpoints developed during the course.
- **[`/ui`](./ui)**: A minimalist "playground" (HTML/JS) used to test and interact with the API endpoints.
- **[`/learn`](./learn)**: My step-by-step learning notes and worklogs for each lesson, documenting key concepts, challenges, and implementation details.
- **[`/docs`](./docs)**: Architectural decisions, migration guides, and more in-depth documentation.

## 🚀 Getting Started

### Backend (API)
The API uses `uv` for dependency management.
```bash
cd api
uv run fastapi dev main.py
```

### Frontend (Playground)
Simply open [`ui/index.html`](./ui/index.html) in your browser.

## 🛠️ Tech Stack
- **FastAPI**: Modern, high-performance web framework for building APIs.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **UV**: An extremely fast Python package and project manager.
- **Vanilla JS & CSS**: For the lightweight testing playground.
