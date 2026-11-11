from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    CreateSessionRequest,
)
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/session", status_code=status.HTTP_201_CREATED)
def create_session(
    request: CreateSessionRequest,
    db: Session = Depends(get_db),
):
    session = ChatService.create_session(
        db=db,
        session_name=request.session_name,
        user_id=request.user_id,
    )

    return {
        "success": True,
        "message": "Chat session created successfully.",
        "data": {
            "session_key": session.session_key,
            "session_name": session.session_name,
            "user_id": session.user_id,
            "created_on": session.created_on,
        },
    }


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    return ChatService.chat(
        db=db,
        session_key=request.session_key,
        user_key=request.user_key,
        message=request.message,
    )


@router.get("/history/{session_key}")
def get_chat_history(
    session_key: str,
    db: Session = Depends(get_db),
):
    history = ChatService.history(
        db=db,
        session_key=session_key,
    )

    if not history:
        return {
            "success": False,
            "message": "No chat history found.",
            "session_key": session_key,
            "total_messages": 0,
            "data": [],
        }

    return {
        "success": True,
        "message": "Chat history fetched successfully.",
        "session_key": session_key,
        "total_messages": len(history),
        "data": [
            {
                "message_id": item.message_id,
                "role": item.role,
                "message": item.message,
                "created_on": item.created_on,
            }
            for item in history
        ],
    }


@router.delete("/session/{session_key}")
def delete_session(
    session_key: str,
    db: Session = Depends(get_db),
):
    session = ChatService.delete_session(
        db=db,
        session_key=session_key,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )

    return {
        "success": True,
        "message": "Chat session deleted successfully.",
        "data": {
            "session_key": session_key,
        },
    }