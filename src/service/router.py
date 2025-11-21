from fastapi import (
    APIRouter, Depends, HTTPException, Query, status
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .db import get_supabase_client
from .schema import (
    AuthPayload, TokenResponse, LinkCreate, LinkOut, UserInfo
)
from .types import Paginated
from . import funcs

router = APIRouter()

security = HTTPBearer(auto_error=False)


# -- route dependencies --

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = credentials.credentials
    supabase = get_supabase_client()
    return funcs.get_user_from_token(token, supabase)


# -- auth routes --

@router.post(
    "/auth/signup",
    status_code=status.HTTP_201_CREATED
)
def signup(
    payload: AuthPayload
):
    supabase = get_supabase_client()
    return funcs.signup_user(payload, supabase)


@router.post("/auth/login", response_model=TokenResponse)
def login(
    payload: AuthPayload
):
    supabase = get_supabase_client()
    return funcs.login_user(payload, supabase)


@router.get("/me", response_model=UserInfo)
def me(
    user: UserInfo = Depends(get_current_user)
):
    return user


# -- Links routes --

@router.post(
    "/api/links", 
    response_model=LinkOut, 
    status_code=status.HTTP_201_CREATED
)
def create_link(
    payload: LinkCreate, 
    user: UserInfo = Depends(get_current_user)
):
    supabase = get_supabase_client()
    return funcs.create_link_for_user(user, payload, supabase)


@router.get(
    "/api/links", 
    response_model=Paginated[LinkOut]
)
def get_links(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user: UserInfo = Depends(get_current_user),
):
    supabase = get_supabase_client()
    return funcs.list_links_for_user(user, supabase, page, page_size)