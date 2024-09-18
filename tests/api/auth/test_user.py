def test_get_user():
    """
    Test the GET /users/me endpoint.
    """
    from fastapi.testclient import TestClient

    from src.fast_drive import app
    from tests.api.utils import get_user_token

    client = TestClient(app)
    token = get_user_token(
        client=client,
        version="1",
        username="johndoe",
        password="abcd",
        scopes=["me", "files"],
    )

    response = client.get(
        "/api/v1/auth/users/me",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"
