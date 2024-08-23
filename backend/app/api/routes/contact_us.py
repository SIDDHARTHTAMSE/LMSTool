from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, status


from fastapi.responses import JSONResponse


from app.api.deps import SessionDep
from app.crud.user_item_crud import create_contact_message, get_contact_messages
from app.crud import user_profile_crud
from app.models import ContactMessage
from app.schemas.contactus import ContactMessageRequest, ContactMessageResponse

router = APIRouter()


@router.post("/contact_us", response_model=ContactMessageResponse)
def send_message(session: SessionDep, contact_req: ContactMessageRequest):
    new_msg_record = ContactMessage()
    new_msg_record.message = contact_req.message
    user_profile = user_profile_crud.get_user_profile_by_email(
        session=session,
        email=contact_req.email
    )
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found for given email ID"
        )
    new_msg_record.user_profile_id = user_profile.id
    new_msg_record = create_contact_message(session=session, contact_message=new_msg_record)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Thank you for sharing the feedback with us"
    )


@router.get("/", response_model=List[ContactMessageResponse])
def get_by_contact_message(session: SessionDep):
    messages = get_contact_messages(session=session)
    response_messages = []
    for msg in messages:
        user_id = msg.user_profile_id
        user_profile = user_profile_crud.get_user_profile_by_id(
            session=session, id=user_id
        )
        response_messages.append(
            ContactMessageResponse(
                first_name=user_profile.full_name,
                last_name=user_profile.last_name,
                email=user_profile.email,
                phone_number=user_profile.phone_number,
                message=msg.message
            )
        )
    return response_messages
