from fastapi import Depends

from interactive_video_backend_core.logic import DecisionLedgerEngine
from interactive_video_backend_core.models import (
    DecisionSubmission,
    SessionResumeResponse,
)
from interactive_video_backend_core.storage import AbstractSessionRepository

from .dependencies import get_repository
from .models import TransitionValidationRequest, TransitionValidationResponse


async def save_decision(
    decision: DecisionSubmission,
    repository: AbstractSessionRepository = Depends(get_repository),
) -> dict[str, str]:
    await repository.save_decision(decision)
    return {"status": "saved"}


async def resume_session(
    user_id: str,
    session_id: str,
    repository: AbstractSessionRepository = Depends(get_repository),
) -> SessionResumeResponse | None:
    return await repository.get_session_state(user_id, session_id)


async def validate_transition(
    request: TransitionValidationRequest,
) -> TransitionValidationResponse:
    try:
        DecisionLedgerEngine.validate_transition(
            request.current_node,
            request.choice_id,
            request.allowed_choices,
        )
    except ValueError:
        return TransitionValidationResponse(valid=False)
    return TransitionValidationResponse(valid=True)
