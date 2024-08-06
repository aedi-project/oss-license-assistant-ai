import uuid
from typing import Any, Optional

from sqlmodel import Session, select

from app.models import Item, ItemCreate, User


def create_user(
    *,
    session: Session,
    email: str,
    full_name: str,
    github_id: Optional[int] = None,
    google_id: Optional[str] = None
) -> User:
    db_obj = User(
        email=email, full_name=full_name, github_id=github_id, google_id=google_id
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(
    *,
    session: Session,
    db_user: User,
    full_name: Optional[str] = None,
    email: Optional[str] = None
) -> Any:
    if full_name is not None:
        db_user.full_name = full_name
    if email is not None:
        db_user.email = email
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_user_by_github_id(*, session: Session, github_id: int) -> User | None:
    statement = select(User).where(User.github_id == github_id)
    session_user = session.exec(statement).first()
    return session_user


def get_user_by_google_id(*, session: Session, google_id: str) -> User | None:
    statement = select(User).where(User.google_id == google_id)
    session_user = session.exec(statement).first()
    return session_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
