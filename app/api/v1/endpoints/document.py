from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.document_schema import DocumentResponse
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    document = DocumentService.upload_document(
        db=db,
        file=file,
        uploaded_by=1
    )

    return {
        "success": True,
        "message": "Document uploaded successfully.",
        "data": DocumentResponse.model_validate(document)
    }


@router.get("")
def get_documents(
    db: Session = Depends(get_db)
):
    documents = DocumentService.get_documents(db)

    return {
        "success": True,
        "data": [
            DocumentResponse.model_validate(doc)
            for doc in documents
        ]
    }


@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = DocumentService.get_document(
        db,
        document_id
    )

    return {
        "success": True,
        "data": DocumentResponse.model_validate(document)
    }


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    result = DocumentService.delete_document(
        db,
        document_id
    )

    return {
        "success": True,
        "message": result["message"]
    }


@router.post("/{document_id}/reindex")
def reindex_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    result = DocumentService.reindex_document(
        db,
        document_id
    )

    return {
        "success": True,
        "message": result["message"]
    }