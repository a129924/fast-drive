from typing import Annotated

from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm

from ....core.user import get_current_active_user, get_current_user
from ....model.fake_model import fake_users_db
from ....schema.auth import Token, User

router = APIRouter(prefix="/auth")


@router.post("/token")
def login_access_token(from_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    from ....core.auth import authenticate_user

    user: User | None = authenticate_user(
        username=from_data.username,
        password=from_data.password,
        db=fake_users_db,
    )

    if not user:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail="Incorrect username or password")

    from ....core.auth import create_access_token, generate_toeken_expires

    access_token = create_access_token(
        data={
            "sub": user.username,
            "scope": from_data.scopes,
        },
        expires_delta=generate_toeken_expires(minutes=15),
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=User)
def read_users_me(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
) -> User:
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
