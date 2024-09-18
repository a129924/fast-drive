def test_login_access_token():
    from fastapi.testclient import TestClient

    from src.fast_drive import app
    from tests.api.utils import get_token_response

    client = TestClient(app)

    response = get_token_response(
        client=client, version="1", username="johndoe", password="abcd"
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


def test_login_access_token_incorrect_password():
    from fastapi.testclient import TestClient

    from src.fast_drive import app
    from tests.api.utils import get_token_response

    client = TestClient(app)

    response = get_token_response(
        client=client, version="1", username="johndoe", password="error_password"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_access_token_scopes():
    from fastapi.testclient import TestClient

    from src.fast_drive import app
    from tests.api.utils import get_token_response

    client = TestClient(app)

    response = get_token_response(
        client=client,
        version="1",
        username="johndoe",
        password="abcd",
        scopes=["me", "items"],
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"
