from fastapi.testclient import TestClient

from interactive_video_labs_fastapi import create_app


def test_health():
    app = create_app("sqlite+aiosqlite:///:memory:")

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_validate_transition():
    app = create_app("sqlite+aiosqlite:///:memory:")

    with TestClient(app) as client:
        valid = client.post(
            "/transitions/validate",
            json={
                "current_node": "question-1",
                "choice_id": "answer-b",
                "allowed_choices": ["answer-a", "answer-b"],
            },
        )
        invalid = client.post(
            "/transitions/validate",
            json={
                "current_node": "question-1",
                "choice_id": "answer-c",
                "allowed_choices": ["answer-a", "answer-b"],
            },
        )

    assert valid.status_code == 200
    assert valid.json() == {"valid": True}
    assert invalid.status_code == 200
    assert invalid.json() == {"valid": False}


def test_save_and_resume_decision():
    app = create_app("sqlite+aiosqlite:///:memory:")

    with TestClient(app) as client:
        saved = client.post(
            "/decisions",
            json={
                "user_id": "user-123",
                "session_id": "session-456",
                "video_id": "video-789",
                "node_id": "question-1",
                "choice_id": "answer-b",
                "timestamp": 12.5,
                "metadata": {"source": "web"},
            },
        )
        resumed = client.get("/sessions/user-123/session-456")

    assert saved.status_code == 201
    assert saved.json() == {"status": "saved"}
    assert resumed.status_code == 200
    assert resumed.json()["last_node_id"] == "question-1"
    assert resumed.json()["last_timestamp"] == 12.5
