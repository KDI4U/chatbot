import os
import shutil
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.rag.ingest import DocumentIngestor


UPLOAD_FOLDER = "uploads/documents"


class DocumentService:

    @staticmethod
    def upload_document(
        db: Session,
        file: UploadFile,
        uploaded_by: int = None
    ):

        # Validate file
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed."
            )

        # Create upload directory
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Generate unique filename
        extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid4()}{extension}"

        file_path = os.path.join(
            UPLOAD_FOLDER,
            unique_filename
        )

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create DB record
        document = Document(
            file_name=unique_filename,
            original_name=file.filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            file_type=extension.replace(".", "").lower(),
            uploaded_by=uploaded_by,
            is_indexed=False,
            is_active=True
        )

        document = DocumentRepository.create(
            db=db,
            document=document
        )

        # Index document
        try:

            DocumentIngestor.ingest(file_path)

            document.is_indexed = True

        except Exception as ex:

            print(f"Indexing Error : {ex}")

            document.is_indexed = False

        DocumentRepository.update(
            db=db,
            document=document
        )

        return document

    @staticmethod
    def get_documents(db: Session):

        return DocumentRepository.get_all(db)

    @staticmethod
    def get_document(
        db: Session,
        document_id: int
    ):

        document = DocumentRepository.get_by_id(
            db,
            document_id
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found."
            )

        return document

    @staticmethod
    def delete_document(
        db: Session,
        document_id: int
    ):

        document = DocumentRepository.get_by_id(
            db,
            document_id
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found."
            )

        # Delete physical file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        DocumentRepository.soft_delete(
            db,
            document
        )

        return {
            "message": "Document deleted successfully."
        }

    @staticmethod
    def reindex_document(
        db: Session,
        document_id: int
    ):

        document = DocumentRepository.get_by_id(
            db,
            document_id
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found."
            )

        try:

            DocumentIngestor.ingest(
                document.file_path
            )

            document.is_indexed = True

            DocumentRepository.update(
                db,
                document
            )

            return {
                "message": "Document indexed successfully."
            }

        except Exception as ex:

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            )