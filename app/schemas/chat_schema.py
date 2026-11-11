from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    session_name: str
    user_id: int | None = None



class ChatRequest(BaseModel):
    session_key: str | None = None
    user_key: str
    message: str

class ChatResponse(BaseModel):
    success: bool
    session_key: str
    answer: str