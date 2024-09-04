from functools import lru_cache


@lru_cache
def create_password_context():
    """
    Create a password context for password hashing and verification.
    """
    from passlib.context import CryptContext

    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.

    Args:
        password (str): The password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return create_password_context().verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Get the hashed password for a given password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return create_password_context().hash(password)


def create_oauth2_scheme(token_url: str, scopes: dict[str, str]):
    from fastapi.security import OAuth2PasswordBearer

    return OAuth2PasswordBearer(
        tokenUrl=token_url,
        scopes=scopes,
    )
