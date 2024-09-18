from fastapi.testclient import TestClient
from httpx import Response as HTTPXResponse


def get_token_response(
    client: TestClient,
    version: str,
    username: str,
    password: str,
    scopes: list[str] | str = "",
) -> HTTPXResponse:
    """
    Get the token response.

    Args:
        client (TestClient): The test client.
        version (str): The API version.
        username (str): The username.
        password (str): The password.
        scopes (list[str] | str): The scopes.
    Returns:
        HTTPXResponse: The token response.
    """

    response = client.post(
        f"/api/v{version}/auth/token",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": " ".join(scopes) if isinstance(scopes, list) else scopes,
            "client_id": "string",
            "client_secret": "string",
        },
    )

    return response


def get_user_token(
    client: TestClient,
    version: str,
    username: str,
    password: str,
    scopes: list[str] | str = "",
) -> str:
    """
    Get the user token.

    Args:
        client (TestClient): The test client.
        version (str): The API version.
        username (str): The username.
        password (str): The password.
        scopes (list[str] | str): The scopes.
    Returns:
        str: The user token.
    """

    response = get_token_response(
        client=client,
        version=version,
        username=username,
        password=password,
        scopes=scopes,
    )

    return response.json()["access_token"]
