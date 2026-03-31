from pydantic import BaseModel
from typing import Optional

class ExtractionResult(BaseModel):

    DocumentType: Optional[str] = None
    Name: Optional[str] = None
    DateOfBirth: Optional[str] = None
    Address: Optional[str] = None
    Phone: Optional[str] = None
    Email: Optional[str] = None
    DocumentNumber: Optional[str] = None
    ExpiryDate: Optional[str] = None
    RawText: Optional[str] = None