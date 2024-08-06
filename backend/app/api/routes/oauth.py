from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select
from authlib.integrations.starlette_client import OAuth

from app.models import User
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token

oauth = OAuth()

# GitHub OAuth 설정
oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    client_kwargs={"scope": "user:email"},
)

# Google OAuth 설정
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    client_kwargs={"scope": "openid email profile"},
)

router = APIRouter()


@router.get("/login/github")
async def login_github(request: Request):
    redirect_uri = request.url_for("auth_github")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/auth/github")
async def auth_github(request: Request, session: Session = Depends(get_db)):
    token = await oauth.github.authorize_access_token(request)
    user_info = await oauth.github.userinfo(token=token)
    email = user_info["email"]
    github_id = user_info["id"]

    user = session.exec(select(User).where(User.github_id == github_id)).first()
    if not user:
        user = User(
            email=email, full_name=user_info.get("name", ""), github_id=github_id
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_google")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google")
async def auth_google(request: Request, session: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)
    email = user_info["email"]
    google_id = user_info["sub"]

    user = session.exec(select(User).where(User.google_id == google_id)).first()
    if not user:
        user = User(
            email=email, full_name=user_info.get("name", ""), google_id=google_id
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}
