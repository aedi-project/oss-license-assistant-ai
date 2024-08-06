from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import create_access_token
from app.models import User
from app.tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(client: TestClient, user: User) -> dict[str, str]:
    """
    Generate authentication headers for a given user.
    """
    access_token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    full_name = random_lower_string()
    user = crud.create_user(session=db, email=email, full_name=full_name)
    return user


def authentication_token_from_email(
    client: TestClient, email: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    user = crud.get_user_by_email(session=db, email=email)
    if not user:
        full_name = random_lower_string()
        user = crud.create_user(session=db, email=email, full_name=full_name)

    return user_authentication_headers(client=client, user=user)
