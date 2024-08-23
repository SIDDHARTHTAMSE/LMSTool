from fastapi import APIRouter, HTTPException
from app.crud import create_contact_message, get_contact_message
from app.schemas.contactus import ContactMessageRequest, ContactMessageResponse, to_contact_res
from app.api.deps import SessionDep
from fastapi import status
from app.models import ContactMessage
from fastapi.responses import JSONResponse
from typing import List


router = APIRouter()


@router.post("/contactus", response_model=ContactMessageResponse)
def send_message(session: SessionDep, contact_req: ContactMessageRequest):

    contact_message = ContactMessage()
    contact_message.first_name = contact_req.first_name
    contact_message.last_name = contact_req.last_name
    contact_message.email = contact_req.email
    contact_message.phone_number = contact_req.phone_number
    contact_message.message = contact_req.message

    contact_message = create_contact_message(session=session, contact_message=contact_message)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_contact_res(contact_message)
    )


@router.get("/", response_model=List[ContactMessageResponse])
def get_by_contact_message(session: SessionDep):
    message = get_contact_message(session=session)
    return [to_contact_res(m) for m in message]