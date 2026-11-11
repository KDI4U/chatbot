from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)
from sqlalchemy.sql import func

from app.database.base import Base


class Document(Base):

    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)

    file_name = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)

    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)

    uploaded_by = Column(Integer, nullable=True)

    is_indexed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    uploaded_on = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )