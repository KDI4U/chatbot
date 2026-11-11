from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:

    @staticmethod
    def create(db: Session, document: Document):
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def update(db: Session, document: Document):
        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Document)
            .filter(Document.is_active == True)
            .order_by(Document.document_id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, document_id: int):
        return (
            db.query(Document)
            .filter(
                Document.document_id == document_id,
                Document.is_active == True
            )
            .first()
        )

    @staticmethod
    def soft_delete(db: Session, document: Document):
        document.is_active = False
        db.commit()
        return document