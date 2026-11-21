from pydantic import BaseModel


class TransitionValidationRequest(BaseModel):
    current_node: str
    choice_id: str
    allowed_choices: list[str]


class TransitionValidationResponse(BaseModel):
    valid: bool
