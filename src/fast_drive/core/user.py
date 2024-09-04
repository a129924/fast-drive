from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import SecurityScopes
from jwt import InvalidTokenError
from pydantic import ValidationError

from ..core.auth import OAUTH2_SCHEME
from ..model.fake_model import fake_users_db
from ..schema.auth import User


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(OAUTH2_SCHEME)],
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scopes}"'
    else:
        authenticate_value = "Bearer"

    from fastapi import HTTPException, status

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
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

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
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
