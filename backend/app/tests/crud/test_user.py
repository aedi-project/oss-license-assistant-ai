from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.models import User
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    user = crud.create_user(session=db, email=email, full_name=full_name)
    assert user.email == email
    assert user.full_name == full_name


def test_get_user(db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    user = crud.create_user(session=db, email=email, full_name=full_name)
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    user = crud.create_user(session=db, email=email, full_name=full_name)
    new_full_name = random_lower_string()
    user_in_update = {"full_name": new_full_name}
    if user.id is not None:
        crud.update_user(session=db, db_user=user, **user_in_update)
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert user_2.full_name == new_full_name


def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    full_name = random_lower_string()
    user = crud.create_user(session=db, email=email, full_name=full_name)
    assert user.is_active is True
