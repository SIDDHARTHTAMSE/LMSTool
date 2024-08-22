from pydantic import BaseModel

from app.models import SignUpCreate


class CreateSignUp(BaseModel):
    full_name: str
    email: str
    password: str


class CreateSignUpRes(BaseModel):
    full_name: str
    email: str
    password: str


def to_signup_res(signup: SignUpCreate):
    return CreateSignUpRes(
        full_name=signup.full_name,
        email=signup.email,
        password=signup.password
    ).dict()
