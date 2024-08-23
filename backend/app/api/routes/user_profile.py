from fastapi import APIRouter, HTTPException
from app.crud import user_profile_crud
from app.schemas.signup import CreateSignUp, CreateSignUpRes, to_signup_res
from app.schemas.signin import SigninRequest
from app.api.deps import SessionDep
from fastapi import status
from app.models import UserProfile
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post("/sign_up", response_model=CreateSignUpRes)
def create_by_signup(session: SessionDep, signup_req: CreateSignUp):
    existing_user_profile = user_profile_crud.get_user_profile_by_email(
        session=session, email=signup_req.email
    )

    if existing_user_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User Profile by given Email ID already exist"
        )

    new_user = UserProfile()
    new_user.full_name = signup_req.full_name
    new_user.email = signup_req.email
    new_user.password = signup_req.password
    new_user = user_profile_crud.create_user_profile(session=session, user=new_user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=to_signup_res(new_user)
    )


@router.post("/sign_in")
def sign_in(session: SessionDep, signin_req: SigninRequest):
    user = user_profile_crud.get_user_profile_by_email(
        session=session, email=signin_req.email
    )

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
        content="Successfully signed in"
    )
