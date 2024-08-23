from pydantic import BaseModel
from app.models import ContactMessage


class ContactMessageRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    message: str


class ContactMessageResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    message: str


def to_contact_res(contact_message: ContactMessage):
    return ContactMessageResponse(
        first_name=contact_message.first_name,
        last_name=contact_message.last_name,
        email=contact_message.email,
        phone_number=contact_message.phone_number,
        message=contact_message.message
    ).dict()
