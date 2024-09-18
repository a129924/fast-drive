from typing import Annotated

from fastapi import Depends, HTTPException, Security
from fastapi.security import SecurityScopes
from jwt import InvalidTokenError
from pydantic import ValidationError

from ..core.auth import OAUTH2_SCHEME
from ..model.fake_model import fake_users_db
from ..schema.auth import User


def create_authenticate_value(security_scopes: SecurityScopes) -> str:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scopes}"'
    else:
        authenticate_value = "Bearer"

    return authenticate_value


def create_credentials_exception(authenticate_value):
    from fastapi import HTTPException, status

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )


def check_scope(
    user_scopes: list[str],
    security_spoces: list[str],
) -> bool:
    user_scopes_set = set(user_scopes)

    for security_spoce in security_spoces:
        if security_spoce not in user_scopes_set:
            return False

    return True


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(OAUTH2_SCHEME)],
) -> User:
    authenticate_value = create_authenticate_value(security_scopes=security_scopes)
    credentials_exception = create_credentials_exception(
        authenticate_value=authenticate_value
    )

    try:
        from ..core.auth import decode_token
        from ..schema.auth import TokenData

        payload = decode_token(token=token)

        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_scopes: list[str] = payload.get("scope", [])

        token_data = TokenData(username=username, scopes=token_scopes)

    except (InvalidTokenError, ValidationError) as errors:
        raise credentials_exception from errors

    user = fake_users_db.get(token_data.username)

    if user is None:
        raise credentials_exception

    if (
        check_scope(
            user_scopes=token_data.scopes,
            security_spoces=security_scopes.scopes,
        )
        is False
    ):
        raise HTTPException(
            status_code=401,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
) -> User:
    """
    Get the current active user.
    """
    if current_user.disabled is False:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
