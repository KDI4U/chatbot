from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    message_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_sessions.session_id")
    )

    role: Mapped[str] = mapped_column(
        String(30)
    )

    message: Mapped[str] = mapped_column(
        Text
    )

    created_on: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )