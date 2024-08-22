from pydantic import BaseModel

from app.models import SignUpCreate


class SigninRequest(BaseModel):
    email: str
    password: str


class SigninResponse(BaseModel):
    email: str
    password: str


def to_signin_res(signin: SignUpCreate):
    return SigninResponse(
        email=signin.email,
        password=signin.password
    ).dict()
