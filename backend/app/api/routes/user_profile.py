from fastapi import APIRouter, HTTPException
from app.crud import user_profile_crud
from app.schemas.signup import CreateSignUp, CreateSignUpRes, to_signup_res, UpdateUserProfile
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
    new_user.first_name = signup_req.first_name
    new_user.last_name = signup_req.last_name
    new_user.phone_number = str(signup_req.phone_number)
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


@router.get("{email_id}", response_model=CreateSignUpRes)
def get_user_profile(session: SessionDep, email_id: str):
    existing_email = user_profile_crud.get_user_profile_by_email(session=session, email=email_id)

    if not existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User email id not found"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_signup_res(existing_email)
    )


@router.delete("{email_id}")
def delete_user_profile(session: SessionDep, email_id: str):
    user_to_delete = user_profile_crud.get_user_profile_by_email(session=session, email=email_id)

    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User email not found"
        )

    user_profile_crud.delete_by_user(session=session, user=user_to_delete)
    return JSONResponse(
        content="User profile deleted successfully"
    )


@router.put("/email_id", response_model=CreateSignUpRes)
def update_existing_user_profile(session: SessionDep, email_id: str, user_req: UpdateUserProfile):
    existing_email = user_profile_crud.get_user_profile_by_email(session=session, email=email_id)

    if not existing_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User email id not found"
        )

    existing_email.full_name = user_req.full_name or existing_email.full_name
    existing_email.first_name = user_req.first_name or existing_email.first_name
    existing_email.last_name = user_req.last_name or existing_email.last_name
    existing_email.email = user_req.email or existing_email.email
    existing_email.phone_number = user_req.phone_number or existing_email.phone_number
    existing_email.password = user_req.password or existing_email.password

    existing_email = user_profile_crud.update_user_profile(session=session, user=existing_email)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_signup_res(existing_email)
    )

