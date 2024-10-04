from fastapi import APIRouter, HTTPException, status
from app.crud import user_profile_crud
from app.schemas.signup import CreateSignUp, CreateSignUpRes, to_signup_res, UpdateUserProfile
from app.schemas.signin import SigninRequest
from app.api.deps import SessionDep
from app.models import UserProfile
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/sign_up", response_model=CreateSignUpRes)
def create_by_signup(session: SessionDep, signup_req: CreateSignUp):
    # Trim the input fields
    signup_req.full_name = signup_req.full_name.strip() if signup_req.full_name else None
    signup_req.email = signup_req.email.strip()
    signup_req.password = signup_req.password.strip()

    # Validate input fields
    if not signup_req.full_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Full name must not be null"
        )
    if not signup_req.email or "@" not in signup_req.email or not signup_req.email.endswith('gmail.com'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must be valid and contain '@' and end with 'gmail.com'."
        )
    if not signup_req.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not be null"
        )

    existing_user_profile = user_profile_crud.get_user_profile_by_email(
        session=session, email=signup_req.email
    )

    if existing_user_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User Profile by given Email ID already exists"
        )

    new_user = UserProfile(
        full_name=signup_req.full_name,
        first_name=signup_req.first_name.strip() if signup_req.first_name else None,
        last_name=signup_req.last_name.strip() if signup_req.last_name else None,
        phone_number=signup_req.phone_number.strip() if signup_req.phone_number else None,
        email=signup_req.email,
        password=signup_req.password
    )

    new_user = user_profile_crud.create_user_profile(session=session, user=new_user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=to_signup_res(new_user)
    )


@router.post("/sign_in")
def sign_in(session: SessionDep, signin_req: SigninRequest):
    signin_req.email = signin_req.email.strip()
    signin_req.password = signin_req.password.strip()

    # Validate input fields
    if not signin_req.email or "@" not in signin_req.email or not signin_req.email.endswith('gmail.com'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must be valid and contain '@' and end with 'gmail.com'."
        )
    if not signin_req.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not be null"
        )

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


@router.get("/{email_id}", response_model=CreateSignUpRes)
def get_user_profile(session: SessionDep, email_id: str):
    existing_email = user_profile_crud.get_user_profile_by_email(session=session, email=email_id)

    if not existing_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User email id not found"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_signup_res(existing_email)
    )


@router.delete("/{email_id}")
def delete_user_profile(session: SessionDep, email_id: str):
    user_to_delete = user_profile_crud.get_user_profile_by_email(session=session, email=email_id)

    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User email not found"
        )

    user_profile_crud.delete_by_user(session=session, user=user_to_delete)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="User profile deleted successfully"
    )


@router.put("/{email_id}", response_model=CreateSignUpRes)
def update_existing_user_profile(session: SessionDep, email_id: str, user_req: UpdateUserProfile):
    existing_email = user_profile_crud.get_user_profile_by_email(session=session, email=email_id)

    if not existing_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User email id not found"
        )

    # Trim the input fields
    user_req.full_name = user_req.full_name.strip() if user_req.full_name else None
    user_req.first_name = user_req.first_name.strip() if user_req.first_name else None
    user_req.last_name = user_req.last_name.strip() if user_req.last_name else None
    user_req.email = user_req.email.strip() if user_req.email else None
    user_req.phone_number = user_req.phone_number.strip() if user_req.phone_number else None
    user_req.password = user_req.password.strip() if user_req.password else None

    # Validate input fields
    if user_req.full_name is None and user_req.first_name is None and user_req.last_name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one of full_name, first_name, or last_name must be provided"
        )
    if user_req.email is None or "@" not in user_req.email or not user_req.email.endswith('gmail.com'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must be valid and contain '@' and end with 'gmail.com'."
        )
    if user_req.password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not be null"
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
