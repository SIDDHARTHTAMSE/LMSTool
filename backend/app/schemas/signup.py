from typing import Optional

from pydantic import BaseModel

from app.models import UserProfile


class CreateSignUp(BaseModel):
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[int] = None
    email: str
    password: str


class CreateSignUpRes(CreateSignUp):
    pass


def to_signup_res(signup: UserProfile):
    return CreateSignUpRes(
        full_name=signup.full_name,
        first_name=signup.first_name,
        last_name=signup.last_name,
        phone_number=signup.phone_number,
        email=signup.email,
        password=signup.password
    ).dict()
