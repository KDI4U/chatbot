from sqlalchemy.orm import Session
import uuid

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage


class ChatRepository:

    @staticmethod
    def create_session(
        db: Session,
        session_name: str,
        user_key: str | None = None
    ):

        session = ChatSession(
            session_name=session_name,
            user_key=user_key,
            session_key=f"LIB-{uuid.uuid4().hex[:8].upper()}"
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        return session

    @staticmethod
    def get_session_by_key(
        db: Session,
        session_key: str
    ):
        return (
            db.query(ChatSession)
            .filter(
                ChatSession.session_key == session_key,
                ChatSession.is_active == True
            )
            .first()
        )

    @staticmethod
    def get_session(
        db: Session,
        session_id: int
    ):
        return (
            db.query(ChatSession)
            .filter(
                ChatSession.session_id == session_id
            )
            .first()
        )

    @staticmethod
    def save_message(
        db: Session,
        session_id: int,
        role: str,
        message: str
    ):

        chat = ChatMessage(
            session_id=session_id,
            role=role,
            message=message
        )

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return chat

    @staticmethod
    def get_history(
        db: Session,
        session_id: int
    ):
        return (
            db.query(ChatMessage)
            .filter(
                ChatMessage.session_id == session_id
            )
            .order_by(ChatMessage.message_id)
            .all()
        )

    @staticmethod
    def get_recent_history(
        db: Session,
        session_id: int,
        limit: int = 10
    ):
        return (
            db.query(ChatMessage)
            .filter(
                ChatMessage.session_id == session_id
            )
            .order_by(ChatMessage.message_id.desc())
            .limit(limit)
            .all()[::-1]
        )

    @staticmethod
    def delete_session(
        db: Session,
        session_id: int
    ):

        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.session_id == session_id
            )
            .first()
        )

        if session is None:
            return None

        db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).delete()

        db.delete(session)
        db.commit()

        return session