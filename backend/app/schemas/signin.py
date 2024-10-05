from pydantic import BaseModel
from typing import Optional
from app.schemas.signup import CreateSignUpRes
from app.models import UserProfile


class SigninRequest(BaseModel):
    full_name: Optional[str] = None
    email: str
    password: str


class SigninResponse(BaseModel):
    full_name: str
    email: str
    password: str


def to_signin_res(signin: UserProfile):
    return SigninResponse(
        full_name=signin.full_name,
        email=signin.email,
        password=signin.password
    ).dict()
