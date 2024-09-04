from datetime import datetime, timedelta, timezone
from typing import Any

from ..schema.auth import User
from .security import create_oauth2_scheme, verify_password

# OAuth2 scheme
OAUTH2_SCHEME = create_oauth2_scheme(
    token_url="/api/v1/auth/token",
    scopes={
        "me": "Read information about the current user.",
        "items": "Read items.",
        "files": "Upload and download files.",
    },
)


def authenticate_user(
    username: str,
    password: str,
    db: dict[
        str,  # username
        User,  # user info
    ],
) -> User | bool:
    """
    Authenticate a user.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        db (dict[str, User]): The database containing user information.

    Returns:
        User | bool: The user information if authentication is successful, False otherwise.
    """
    user = db.get(username)

    if user and verify_password(password, user.hashed_password):
        return user

    return False


def generate_toeken_expires(minutes: int) -> timedelta:
    """
    Generate a token expiration time.

    Args:
        minutes (int): The number of minutes to expire the token.

    Returns:
        timedelta: The token expiration time.
    """
    return timedelta(minutes=minutes)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create an access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta | None): The expiration time of the token.

    Returns:
        str: The access token.
    """
    from jwt import encode

    from .config import ALGORITHM, SECRET_KEY

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    from jwt import decode

    from .config import ALGORITHM, SECRET_KEY

    return decode(token, SECRET_KEY, algorithms=[ALGORITHM])
