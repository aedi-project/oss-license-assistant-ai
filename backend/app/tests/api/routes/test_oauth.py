from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.security import create_access_token
from app.models import User
from app.tests.utils.utils import random_email, random_lower_string


def test_oauth_github(client: TestClient, db: Session) -> None:
    email = random_email()
    user = User(
        email=email, full_name=random_lower_string(), github_id=random_lower_string()
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    r = client.get("/auth/github", headers=headers)
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_oauth_google(client: TestClient, db: Session) -> None:
    email = random_email()
    user = User(
        email=email, full_name=random_lower_string(), google_id=random_lower_string()
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    r = client.get("/auth/google", headers=headers)
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_get_user_me(client: TestClient, db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    user = User(email=email, full_name=full_name, github_id=random_lower_string())
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    r = client.get("/users/me", headers=headers)
    result = r.json()
    assert r.status_code == 200
    assert result["email"] == email
    assert result["full_name"] == full_name
