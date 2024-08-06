import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app import crud
from app.core.config import Settings
from app.core.security import create_access_token
from app.models import User
from app.tests.utils.utils import (
    random_email,
    random_lower_string,
    get_user_token_headers,
)


def test_get_user_me(client: TestClient, db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    user = crud.create_user(session=db, email=email, full_name=full_name)

    access_token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    r = client.get(f"{Settings.API_V1_STR}/users/me", headers=headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["email"] == email


def test_create_user_new_email(client: TestClient, db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    data = {"email": email, "full_name": full_name}
    r = client.post(f"{Settings.API_V1_STR}/users/", json=data)
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.get_user_by_email(session=db, email=email)
    assert user
    assert user.email == created_user["email"]


def test_get_existing_user(client: TestClient, db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    user = crud.create_user(session=db, email=email, full_name=full_name)
    user_id = user.id
    headers = get_user_token_headers(client=client, user_id=str(user_id))

    r = client.get(f"{Settings.API_V1_STR}/users/{user_id}", headers=headers)
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.get_user_by_email(session=db, email=email)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_update_user_me(client: TestClient, db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    user = crud.create_user(session=db, email=email, full_name=full_name)

    access_token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    new_full_name = "Updated Name"
    new_email = random_email()
    data = {"full_name": new_full_name, "email": new_email}
    r = client.patch(f"{Settings.API_V1_STR}/users/me", headers=headers, json=data)
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["email"] == new_email
    assert updated_user["full_name"] == new_full_name

    user_query = select(User).where(User.email == new_email)
    user_db = db.exec(user_query).first()
    assert user_db
    assert user_db.email == new_email
    assert user_db.full_name == new_full_name


def test_update_user_me_email_exists(client: TestClient, db: Session) -> None:
    email1 = random_email()
    full_name1 = random_lower_string()
    user1 = crud.create_user(session=db, email=email1, full_name=full_name1)

    email2 = random_email()
    full_name2 = random_lower_string()
    user2 = crud.create_user(session=db, email=email2, full_name=full_name2)

    access_token = create_access_token(user1.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    data = {"email": email2}
    r = client.patch(f"{Settings.API_V1_STR}/users/me", headers=headers, json=data)
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"


def test_delete_user_me(client: TestClient, db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    user = crud.create_user(session=db, email=email, full_name=full_name)
    user_id = user.id

    access_token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    r = client.delete(f"{Settings.API_V1_STR}/users/me", headers=headers)
    assert r.status_code == 200
    deleted_user = r.json()
    assert deleted_user["message"] == "User deleted successfully"
    result = db.exec(select(User).where(User.id == user_id)).first()
    assert result is None
