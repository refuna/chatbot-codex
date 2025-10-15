# Repository Guidelines

## Project Structure & Module Organization
- `backend/` houses the FastAPI service: `app.py` exposes routes, `rag_system.py` orchestrates retrieval + generation, while helpers such as `document_processor.py`, `vector_store.py`, `search_tools.py`, and `ai_generator.py` encapsulate ingestion, storage, and model calls. The persisted Chroma index lives under `backend/chroma_db/`.
- `frontend/` delivers the static chat client (`index.html`, `style.css`, `script.js`) that interacts with the API.
- `docs/` stores the course transcripts; keep filenames stable so existing embeddings remain valid.
- Root utilities include `pyproject.toml` and `uv.lock` for dependency management, `run.sh` for one-step startup, and `main.py` as a minimal placeholder entry point.

## Build, Test, and Development Commands
- `uv sync` installs or updates all Python dependencies declared in `pyproject.toml`.
- `./run.sh` prepares required directories and launches `uvicorn app:app --reload --port 8000`; use this for the typical development loop.
- `uv run uvicorn app:app --reload --port 8000` starts the backend manually when you need to adjust ports or flags.
- Static assets reload automatically in most browsers; hard-refresh (`Cmd+Shift+R`) if cached styles/scripts linger.

## Coding Style & Naming Conventions
- Python code follows PEP 8: 4-space indentation, snake_case for functions and module-level variables, PascalCase for classes, and explicit docstrings for public methods (see `DocumentProcessor` for tone).
- Prefer descriptive module names that mirror their responsibilities (`session_manager.py`, `search_tools.py`). New files should live beside related functionality under `backend/`.
- Frontend scripts keep modern ES style (const/let, arrow functions where appropriate) and use camelCase for DOM references; keep API paths as relative strings to support reverse proxies.

## Testing Guidelines
- Automated tests are not yet present; add `pytest` suites under `backend/tests/` with filenames in the `test_*.py` pattern so they are auto-discovered.
- Run suites with `uv run pytest` once `pytest` is added to the dependency list. Include regression fixtures for critical flows such as document ingestion, vector search, and AI response formatting.
- Until coverage tooling is introduced, treat smoke-testing via the running app (query common prompts, verify source listings) as part of every change set.

## Commit & Pull Request Guidelines
- Commit history uses short imperative subjects (`updated lab files`); continue with concise present-tense summaries and group related changes per commit.
- Reference issue IDs when available and keep body text focused on rationale or follow-up tasks.
- Pull requests should describe the user-facing impact, list backend/frontend touchpoints, note any migration steps (new env vars, re-ingestion), and include UI screenshots or curl examples for API changes.

## Configuration & Secrets
- Store secrets in a root `.env` file; at minimum set `OPENAI_API_KEY` before running the backend.
- Do not commit `.env`, API keys, or anything under `backend/chroma_db/`. Provide redacted samples in PRs when discussing configuration.
