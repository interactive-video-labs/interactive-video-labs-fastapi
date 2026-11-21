# interactive-video-labs-fastapi 0.2.0

<p align="center">
  <img src="https://raw.githubusercontent.com/interactive-video-labs/docs/main/logo.svg" width="200" alt="Interactive Video Labs Logo" />
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/interactive-video-labs-fastapi" alt="PyPI Version" />
  <img src="https://img.shields.io/pypi/l/interactive-video-labs-fastapi" alt="License" />
  <img src="https://img.shields.io/pypi/dm/interactive-video-labs-fastapi" alt="PyPI Downloads" />
</p>

FastAPI adapter for [`interactive-video-labs-core`](https://pypi.org/project/interactive-video-labs-core/).

This package exposes HTTP endpoints for saving interactive-video decisions, restoring session state, and validating node transitions. It uses SQLAlchemy 2.x and request-scoped async database sessions.

The core decision ledger is designed to complement [`@interactive-video-labs/core`](https://github.com/interactive-video-labs/interactive-video-core), the framework-agnostic TypeScript player used by interactive video applications.

---

## Features

- **FastAPI application factory:** Create an app with a configurable async database URL.
- **Decision API:** Persist viewer choices through the core session repository.
- **Session resume API:** Reconstruct the latest node and playback position.
- **Transition validation:** Check whether a choice is allowed for the current node.
- **Typed request models:** Validate transition requests with Pydantic.
- **Async SQLAlchemy storage:** Use request-scoped async sessions and core SQLAlchemy models.
- **Automatic startup setup:** Create the core database tables in the application lifespan.
- **Framework composition:** Keep decision logic and persistence in the core package while the adapter handles HTTP concerns.

---

## Requirements

- Python 3.10 or newer
- FastAPI 0.115 or newer
- Pydantic 2.x
- SQLAlchemy 2.x
- `interactive-video-labs-core` 0.2.0 or newer

---

## Installation

### Poetry

```bash
poetry add interactive-video-labs-fastapi
```

### pip

```bash
pip install interactive-video-labs-fastapi
```

---

## Quick Start

### 1. Create the FastAPI app

```python
from interactive_video_labs_fastapi import create_app

app = create_app(
    "sqlite+aiosqlite:///./interactive_video.db",
)
```

The default database URL is `sqlite+aiosqlite:///./interactive_video.db`.

### 2. Run the server

```bash
uvicorn interactive_video_labs_fastapi.main:app --reload
```

The application creates the core ORM tables during startup and closes the database engine during shutdown.

### 3. Save a decision

```bash
curl -X POST http://127.0.0.1:8000/decisions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "session_id": "session-456",
    "video_id": "video-789",
    "node_id": "question-1",
    "choice_id": "answer-b",
    "timestamp": 12.5,
    "metadata": {"source": "web"}
  }'
```

Response:

```json
{
  "status": "saved"
}
```

### 4. Resume a session

```bash
curl http://127.0.0.1:8000/sessions/user-123/session-456
```

Example response:

```json
{
  "user_id": "user-123",
  "session_id": "session-456",
  "video_id": "video-789",
  "last_node_id": "question-1",
  "last_timestamp": 12.5,
  "decision_history": [
    {
      "user_id": "user-123",
      "session_id": "session-456",
      "video_id": "video-789",
      "node_id": "question-1",
      "choice_id": "answer-b",
      "timestamp": 12.5,
      "metadata": {
        "source": "web"
      }
    }
  ],
  "updated_at": "2026-11-21T18:13:43Z"
}
```

When no decision exists for the user and session, the endpoint returns `null`.

---

## API Endpoints

### `GET /health`

Returns service availability:

```json
{
  "status": "ok"
}
```

### `POST /decisions`

Persists a decision through `SQLAlchemySessionRepository`.

```json
{
  "user_id": "user-123",
  "session_id": "session-456",
  "video_id": "video-789",
  "node_id": "question-1",
  "choice_id": "answer-b",
  "timestamp": 12.5,
  "metadata": {
    "source": "web"
  }
}
```

Returns HTTP `201` with:

```json
{
  "status": "saved"
}
```

### `GET /sessions/{user_id}/{session_id}`

Reconstructs and returns the latest state for a viewing session.

The response includes the latest video, node, playback timestamp, chronological decision history, and latest update time.

### `POST /transitions/validate`

Checks whether a choice is allowed for the current node:

```json
{
  "current_node": "question-1",
  "choice_id": "answer-b",
  "allowed_choices": ["answer-a", "answer-b"]
}
```

Valid response:

```json
{
  "valid": true
}
```

Invalid response:

```json
{
  "valid": false
}
```

---

## Custom Application Setup

Use the application factory in a custom ASGI entry point:

```python
from interactive_video_labs_fastapi import create_app

app = create_app(
    "postgresql+asyncpg://user:password@localhost/interactive_video"
)
```

For testing, create an app with an in-memory SQLite database:

```python
from fastapi.testclient import TestClient

from interactive_video_labs_fastapi import create_app

app = create_app("sqlite+aiosqlite:///:memory:")

with TestClient(app) as client:
    response = client.get("/health")
    assert response.status_code == 200
```

Database table creation is designed for this adapter's simple default setup. Use your application's migration tooling for production database deployments.

---

## Request and Response Models

### `TransitionValidationRequest`

| Field | Type | Description |
| --- | --- | --- |
| `current_node` | `str` | Node currently being viewed |
| `choice_id` | `str` | Choice submitted by the viewer |
| `allowed_choices` | `list[str]` | Choices permitted for the current node |

### `TransitionValidationResponse`

| Field | Type | Description |
| --- | --- | --- |
| `valid` | `bool` | Whether the submitted choice is valid |

Decision submissions and session resume responses use the Pydantic models supplied by `interactive-video-labs-core`.

---

## Development

Clone the repository and install the development dependencies:

```bash
git clone https://github.com/interactive-video-labs/interactive-video-labs-fastapi.git
cd interactive-video-labs-fastapi
poetry install
```

Start the development server:

```bash
poetry run uvicorn interactive_video_labs_fastapi.main:app --reload
```

Run the test suite:

```bash
poetry run pytest
```

For setup details and project conventions, see [DEVELOPER.md](DEVELOPER.md).

---

## Project Structure

```text
interactive-video-labs-fastapi/
├── interactive_video_labs_fastapi/
│   ├── __init__.py
│   ├── app.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── routes.py
├── tests/
│   └── test_api.py
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome. Please review [DEVELOPER.md](DEVELOPER.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting an issue or pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).
