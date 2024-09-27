
from datetime import datetime
from sqlalchemy import Time, JSON
import uuid

from pydantic import EmailStr, condecimal
from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey
from typing import List, Dict, Optional


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] | None = Relationship(
        back_populates="owner", cascade_delete=True
    )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class UserProfile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str = Field(max_length=64)
    first_name: str = Field(max_length=64, nullable=True)
    last_name: str = Field(max_length=64, nullable=True)
    email: EmailStr = Field(unique=True, index=True, max_length=64)
    phone_number: str = Field(max_length=16, nullable=True)
    password: str = Field(min_length=8, max_length=32)
    contact_messages: list["ContactMessage"] = Relationship(
        back_populates="user_profile", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    courses: List["UserEnrollment"] = Relationship(back_populates="user")


class ContactMessage(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    message: str = Field(max_length=500)
    user_profile_id: uuid.UUID = Field(
        sa_column=Column(ForeignKey("userprofile.id", ondelete="CASCADE"), nullable=False)
    )
    user_profile: "UserProfile" = Relationship(back_populates="contact_messages")


class Course(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    course_name: str = Field(max_length=128, nullable=False)
    description: Optional[str] = Field(max_length=255, nullable=True)
    thumbnail_url: Optional[str] = Field(nullable=True)
    rating: Optional[float] = Field(default=None, ge=0, le=5, nullable=True)
    categories: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    content: Optional[List[Dict[str, str]]] = Field(default=None, sa_column=Column(JSON))
    duration: Optional[int] = Field(nullable=True)
    level: Optional[str] = Field(default=None)
    released_date: Optional[datetime] = Field(default=None, nullable=True)
    last_update: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=True)
    enrollment_count: int = Field(default=0)
    certification: bool = Field(default=False)
    discount_offers: Optional[str] = Field(max_length=255, nullable=True)
    syllabus: Optional[str] = Field(max_length=2000, nullable=True)
    progress_tracking: bool = Field(default=False)
    course_resource: Optional[str] = Field(max_length=500, nullable=True)
    faqs: Optional[str] = Field(max_length=2000, nullable=True)
    accessibility_features: Optional[str] = Field(max_length=255, nullable=True)
    course_preview: Optional[str] = Field(nullable=True)
    interactive_features: Optional[str] = Field(max_length=255, nullable=True)
    video_quality_option: Optional[str] = Field(max_length=255, nullable=True)

    authors: List["CourseAuthorLink"] = Relationship(back_populates="course")
    prices: List["Price"] = Relationship(back_populates="course")
    chapters: List["CourseChapter"] = Relationship(back_populates="course")
    thumbnail: List["Thumbnail"] = Relationship(back_populates="course")
    enrollments: List["UserEnrollment"] = Relationship(back_populates="course")
    resources: List["CourseResource"] = Relationship(back_populates="course")


class Author(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=64, nullable=False)
    bio: Optional[str] = Field(max_length=256, nullable=True)
    email: Optional[EmailStr] = Field(max_length=256, nullable=True)
    website: Optional[str] = Field(max_length=256, nullable=True)
    expertise: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    qualification: Optional[str] = Field(max_length=256, nullable=True)
    experience_years: Optional[int] = Field(nullable=True)
    certifications: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    location: Optional[str] = Field(max_length=32, nullable=True)
    languages: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    contact_number: Optional[str] = Field(max_length=12, nullable=True)
    join_date: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=True)
    last_active: Optional[datetime] = Field(nullable=True)

    courses: List["CourseAuthorLink"] = Relationship(back_populates="author")


class Price(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: condecimal(gt=0) = Field(nullable=False)
    currency: str = Field(max_length=3, nullable=False, default="USD")
    discount: Optional[str] = Field(ge=0, le=100, nullable=True)
    start_date: Optional[datetime] = Field(default=None, nullable=True)
    end_date: Optional[datetime] = Field(default=None, nullable=True)
    description: Optional[str] = Field(max_length=255, nullable=True)

    course_id: uuid.UUID = Field(foreign_key="course.id")
    course: Course = Relationship(back_populates="prices")


class CourseAuthorLink(SQLModel, table=True):
    course_id: uuid.UUID = Field(foreign_key="course.id", primary_key=True)
    author_id: uuid.UUID = Field(foreign_key="author.id", primary_key=True)

    course: Course = Relationship(back_populates="authors")
    author: Author = Relationship(back_populates="courses")


class CourseChapter(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=128, nullable=False)
    content: Optional[str] = Field(nullable=True)
    order: Optional[str] = Field(nullable=True)

    course_id: uuid.UUID = Field(foreign_key="course.id")
    course: Course = Relationship(back_populates="chapters")

    resources: List["CourseResource"] = Relationship(back_populates="chapter")


class Thumbnail(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(max_length=255, nullable=True)
    uploaded_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    thumbnail_id: uuid.UUID = Field(foreign_key="course.id")
    course: Course = Relationship(back_populates="thumbnail")


class UserEnrollment(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="userprofile.id", primary_key=True)
    course_id: uuid.UUID = Field(foreign_key="course.id", primary_key=True)
    enrollment_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    status: Optional[str] = Field(max_length=64, nullable=True)

    user: UserProfile = Relationship(back_populates="courses")
    course: Course = Relationship(back_populates="enrollments")


class CourseResource(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=128, nullable=False)
    resource_url: Optional[str] = Field(nullable=True)

    course_id: uuid.UUID = Field(foreign_key="course.id", nullable=False)
    chapter_id: uuid.UUID = Field(foreign_key="coursechapter.id", nullable=False)
    resource_type_id: uuid.UUID = Field(foreign_key="resourcetype.id", nullable=False)

    course: Course = Relationship(back_populates="resources")
    chapter: CourseChapter = Relationship(back_populates="resources")
    # resource_type: ResourceType = Relationship(back_populates="resources")


class ResourceType(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type_name: str = Field(max_length=64, nullable=False)
    description: Optional[str] = Field(nullable=True)
    # resources: List["CourseResource"] = Relationship(back_populates="resource_type")
