from typing import Optional

from pydantic import BaseModel
from app.models import ContactMessage


class ContactMessageRequest(BaseModel):
    email: str
    message: str


class ContactMessageResponse(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    phone_number: Optional[str]
    message: str

