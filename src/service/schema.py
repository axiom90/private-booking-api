from pydantic import (
    BaseModel, EmailStr, HttpUrl, constr
)
from datetime import datetime


# -- auth schemas --

class AuthPayload(BaseModel):
    email: EmailStr
    password: constr(min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    id: str
    email: str | None = None


# -- link schemas --

class LinkCreate(BaseModel):
    title: str
    url: HttpUrl


class LinkOut(BaseModel):
    id: str
    title: str
    url: HttpUrl
    created_at: datetime
