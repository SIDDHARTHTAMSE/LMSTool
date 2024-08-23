from pydantic import BaseModel

from app.models import UserProfile


class SigninRequest(BaseModel):
    email: str
    password: str


class SigninResponse(BaseModel):
    email: str
    password: str


def to_signin_res(signin: UserProfile):
    return SigninResponse(
        email=signin.email,
        password=signin.password
    ).dict()
