from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):

    document_id: int
    file_name: str
    original_name: str
    file_size: int
    file_type: str
    is_indexed: bool
    is_active: bool
    uploaded_on: datetime

    model_config = ConfigDict(from_attributes=True)