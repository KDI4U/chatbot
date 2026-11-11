from sqlalchemy.orm import Session
from fastapi import status

from app.ai.ollama import OllamaService
from app.repositories.chat_repository import ChatRepository
from app.core.exceptions import AppException

from app.rag.retriever import Retriever
from app.rag.prompt import PromptBuilder


class ChatService:

    @staticmethod
    def create_session(db: Session, session_name: str, user_key=None):
        return ChatRepository.create_session(
            db=db,
            session_name=session_name,
            user_key=user_key
        )

    @staticmethod
    def chat(
        db: Session,
        session_key: str | None,
        user_key: str,
        message: str
    ):

        # -----------------------------
        # Get Existing Session / Create New
        # -----------------------------
        if session_key:
            session = ChatRepository.get_session_by_key(
                db=db,
                session_key=session_key
            )

            if session is None:
                raise AppException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="Chat session not found."
                )

        else:
            session = ChatRepository.create_session(
                db=db,
                session_name="New Chat",
                user_key=user_key
            )

        session_id = session.session_id

        # -----------------------------
        # Save User Message
        # -----------------------------
        ChatRepository.save_message(
            db=db,
            session_id=session_id,
            role="user",
            message=message
        )

        # -----------------------------
        # Retrieve Context
        # -----------------------------
        documents = Retriever.search(
            question=message,
            top_k=8
        )

        context = "\n\n".join(documents)

        prompt = PromptBuilder.build(
            context=context,
            question=message
        )

        answer = OllamaService.generate_response(prompt)

        # -----------------------------
        # Save AI Response
        # -----------------------------
        ChatRepository.save_message(
            db=db,
            session_id=session_id,
            role="assistant",
            message=answer
        )

        return {
            "success": True,
            "session_key": session.session_key,
            "answer": answer
        }

    @staticmethod
    def history(db: Session, session_key: str):
        session = ChatRepository.get_session_by_key(
            db=db,
            session_key=session_key
        )

        if session is None:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Chat session not found."
            )

        return ChatRepository.get_history(
            db=db,
            session_id=session.session_id
        )

    @staticmethod
    def delete_session(db: Session, session_key: str):
        session = ChatRepository.get_session_by_key(
            db=db,
            session_key=session_key
        )

        if session is None:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Chat session not found."
            )

        return ChatRepository.delete_session(
            db=db,
            session_id=session.session_id
        )