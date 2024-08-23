from fastapi import APIRouter, HTTPException
from app.crud import get_email_by_signup, create_signup, authenticate_user
from app.schemas.signup import CreateSignUp, CreateSignUpRes, to_signup_res
from app.schemas.signin import SigninRequest, SigninResponse, to_signin_res
from app.api.deps import SessionDep
from fastapi import status
from app.models import SignUpCreate
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post("/signup", response_model=CreateSignUpRes)
def create_by_signup(session: SessionDep, signup_req: CreateSignUp):
    existing_email = get_email_by_signup(
        session=session, email=signup_req.email
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email id already exist"
        )

    signup = SignUpCreate()
    signup.full_name = signup_req.full_name
    signup.email = signup_req.email
    signup.password = signup_req.password
    signup = create_signup(session=session, signup=signup)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=to_signup_res(signup)
    )


@router.post("/signin")
def sign_in(session: SessionDep, signin_req: SigninRequest):
    user = get_email_by_signup(session=session, email=signin_req.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email"
        )

    if user.password != signin_req.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Password"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully signin"
    )
