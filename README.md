# Candidate Finder

> A full-stack web app leveraging the OpenAI Agents SDK to automate candidate sourcing:
> parse intent → find LinkedIn profiles → score candidates → justify fit statements.

## Features

- FastAPI backend orchestrating a 4-step GPT-4 + Google CSE pipeline via the openai-agents SDK
- Interactive single-page frontend with job description input and dynamic sliders
- Docker and docker-compose support for reproducible environments
- Health check endpoint (`/healthz`) to verify configuration
- Structured logging and basic error handling

## Requirements

- Python 3.9+
- Docker (optional)
- Environment variables (copy `.env.example` to `.env`):

```bash
OPENAI_API_KEY=sk-...
GOOGLE_CSE_API_KEY=...
GOOGLE_CSE_ENGINE_ID=...
```

## Local Development

1. Copy `.env.example` to `.env` and fill in your API keys.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start FastAPI with autoreload:
   ```bash
   uvicorn src.main:app --reload
   ```
4. Open your browser to <http://localhost:8000> and test the UI.

Or, with Docker Compose:

```bash
docker-compose up --build
```

## API Endpoints

### POST /process

Submit a job description and criteria:

```json
{
  "request": "Job description text",
  "creativity": 0.5,
  "hospitality_expertise": 0.7,
  "experience": 3
}
```

Response:

```json
{
  "candidates": [
    {"name":"Alice","profile_url":"...","benefit":"..."},
    ...
  ]
}
```

### GET /healthz

Simple health check verifying required env vars:

```json
{ "status": "ok" }
```

## Configuration & Prompts

- Default prompts are defined in `src/prompts.py`.
- The company description lives in version control at `src/config.py` and can be overridden via `COMPANY_DESCRIPTION` env var.

## Logging & Observability

- Uses Python `logging` for structured logs (INFO+ level by default).
- Set `LOG_LEVEL=DEBUG` to see debug messages from the agent tools.
- Future: enable openai-agents SDK tracing (via `AGENT_TRACING_OUTPUT` env var) to capture span-level telemetry.

## Documentation Site

This project includes an [MkDocs] documentation site. To view:

```bash
pip install mkdocs
mkdocs serve
```

[MkDocs]: https://www.mkdocs.org/# spherical
