from sqlmodel import Session, select

from app.models import UserProfile


def get_user_profile_by_email(*, session: Session, email: str) -> UserProfile | None:
    query = select(UserProfile).where(UserProfile.email == email)
    user_profile = session.exec(query).one_or_none()
    return user_profile


def create_user_profile(session: Session, user: UserProfile):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(*, session: Session, email: str, password: str) -> UserProfile | None:
    user = get_user_profile_by_email(session=session, email=email)
    if user and user.password == password:
        return user
    return None
