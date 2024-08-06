import random
import string

from fastapi.testclient import TestClient

from app.core.security import create_access_token


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_user_token_headers(client: TestClient, user_id: str) -> dict[str, str]:
    """
    Generate token headers for a user with a given user_id.
    """
    access_token = create_access_token(user_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
