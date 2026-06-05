# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies (uses UV package manager):**
```
uv sync
```

**Run database migrations:**
```
alembic upgrade head
```

**Start the development server:**
```
uvicorn main:app --reload
```

**Test workflows without live Gmail:**
```
# Asset request
curl -X POST http://localhost:8000/mock/asset-request

# Issue handling
curl -X POST http://localhost:8000/mock/issue-handling

# Software request
curl -X POST http://localhost:8000/mock/software-request
```

**Refresh Gmail Pub/Sub subscription:**
```
curl http://localhost:8000/refresh
```

## Architecture

This is a **FastAPI + LangGraph** email assistant that processes incoming Gmail messages, classifies them (asset request / software request / issue / ticket), and routes them through an AI-supervised agentic workflow using Groq LLM inference.

### Request Flow

```
Gmail Pub/Sub → POST /webhook → parse email → LangGraph workflow → reply email / create ticket
```

The workflow graph (`app/workflows/mail_assistant/graph/builder.py`):

```
START → user_verifier → thread_verifier → supervisor
                                               ↓ (conditional routing)
               issue_handler / software_request_handler / asset_request_handler
                                               ↓
                                          supervisor (loop)
                                               ↓
                                    email node  OR  ticket_generator
                                               ↓
                                              END
```

### Layer Structure

| Layer | Path | Responsibility |
|-------|------|----------------|
| Routers | `app/routers/` | FastAPI endpoints (webhook + mock routes) |
| Services | `app/services/` | Business logic + Gmail OAuth/watch integration |
| Workflows | `app/workflows/mail_assistant/` | LangGraph nodes, agents, prompts, graph builder |
| Repository | `app/repository/` | SQLAlchemy data access (users, assets, chat history) |
| Models | `app/models/` | ORM models — `User`, `AssetItem`, `AssetCategory`, `ChatHistory` |
| Config | `app/config/` | Env vars, LLM client setup (`langchain-groq`), shared agent `State` |
| Utils | `app/utils/` | Tool callables (asset/user/category lookups), enums, prompt strings |

### State Object

All LangGraph nodes share a single typed state defined in `app/config/state.py`. Nodes read/write fields on this state; the graph routes based on its values.

### Database

PostgreSQL via SQLAlchemy + Alembic. All tables use soft-delete (`deleted_at`) and audit columns (`created_by`, `updated_by`). Migration files live in `alembic/versions/`.

### LLM

Groq-hosted `meta-llama/llama-4-scout-17b-16e-instruct` configured in `app/config/groq/inference.py`. Temperature 0.5. Swap model constants in `app/utils/constants/llm.py`.

### Gmail Integration

OAuth2 credentials in `credentials.json` (gitignored); token cached in `token.json`. Gmail watch subscription pushes to a Google Cloud Pub/Sub topic. `app/services/gmail/parser.py` decodes the Pub/Sub message and extracts email content. `app/services/gmail/auth.py` handles the OAuth flow.

## Environment Variables

Required in `.env`:

```
GROQ_API_KEY=
DB_NAME=asset_langgraph_assignment
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=
PROJECT_ID=          # GCP project ID for Pub/Sub
SCOPE=https://mail.google.com/
```

Also requires `credentials.json` (Google OAuth app credentials) in the project root.
