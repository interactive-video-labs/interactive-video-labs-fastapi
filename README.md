# interactive-video-labs-fastapi 0.2.0

FastAPI adapter for [interactive-video-labs-core](https://github.com/interactive-video-labs/interactive-video-backend-core).

The wrapper exposes HTTP endpoints for saving interactive-video decisions, restoring session state, and validating node transitions.

## Installation

```bash
pip install interactive-video-labs-fastapi
```

## Quick Start

```python
from interactive_video_labs_fastapi import create_app

app = create_app(
    "sqlite+aiosqlite:///./interactive_video.db",
)
```

Run it with Uvicorn:

```bash
uvicorn interactive_video_labs_fastapi.main:app --reload
```

## Endpoints

### `GET /health`

Returns service availability.

### `POST /decisions`

Persists a decision submission.

```json
{
  "user_id": "user-123",
  "session_id": "session-456",
  "video_id": "video-789",
  "node_id": "question-1",
  "choice_id": "answer-b",
  "timestamp": 12.5,
  "metadata": {"source": "web"}
}
```

### `GET /sessions/{user_id}/{session_id}`

Reconstructs and returns the latest session state.

### `POST /transitions/validate`

Checks whether a choice is allowed for the current node.

```json
{
  "current_node": "question-1",
  "choice_id": "answer-b",
  "allowed_choices": ["answer-a", "answer-b"]
}
```
