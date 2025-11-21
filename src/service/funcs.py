from typing import List
from fastapi import HTTPException, status
from supabase import Client
from math import ceil

from .schema import (
    AuthPayload,
    TokenResponse,
    UserInfo,
    LinkCreate,
    LinkOut,
)
from .types import Paginated


# -- auth logic --

def signup_user(
    payload: AuthPayload, 
    supabase: Client
) -> dict:
 
    try:
        session = supabase.auth.sign_up(
            {
                "email": payload.email,
                "password": payload.password,
            }
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup failed",
        )

    return {
        "message": "Signup successful. Check your email if confirmation is required."
    }


def login_user(
    payload: AuthPayload,
    supabase: Client
) -> TokenResponse:

    try:
        session = supabase.auth.sign_in_with_password(
            {
                "email": payload.email,
                "password": payload.password,
            }
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if session is None or session.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = session.session.access_token

    return TokenResponse(access_token=access_token)


def get_user_from_token(
    token: str, 
    supabase: Client
) -> UserInfo:
    resp = supabase.auth.get_user(token)

    if not resp or not resp.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = resp.user

    return UserInfo(
        id=user.id,
        email=user.email,
    )

# -- Links logic --

def create_link_for_user(
    user: UserInfo, 
    payload: LinkCreate, 
    supabase: Client
) -> LinkOut:

    data = {
        "user_id": user.id,
        "title": payload.title,
        "url": str(payload.url),
    }

    resp = supabase.table("links").insert(data).execute()

    if not resp.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create link",
        )

    row = resp.data[0]
    return LinkOut(
        id=row["id"],
        title=row["title"],
        url=row["url"],
        created_at=row["created_at"],
    )


def list_links_for_user(
    user: UserInfo,
    supabase: Client,
    page: int,
    page_size: int,
) -> Paginated[LinkOut]:

    offset = (page - 1) * page_size
    start = offset
    end = offset + page_size - 1

    resp = (
        supabase.table("links")
        .select("*", count="exact")
        .eq("user_id", user.id)
        .order("created_at", desc=True)
        .range(start, end)
        .execute()
    )

    rows = resp.data or []
    total_items = resp.count or 0
    total_pages = ceil(total_items / page_size) if total_items else 0

    items = [
        LinkOut(
            id=row["id"],
            title=row["title"],
            url=row["url"],
            created_at=row["created_at"],
        )
        for row in rows
    ]

    return Paginated[LinkOut](
        items=items,
        total_items=total_items,
        total_pages=total_pages,
    )