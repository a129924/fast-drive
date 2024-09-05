def test_login_access_token():
    from fastapi.testclient import TestClient

    from src.fast_drive import app

    client = TestClient(app)

    response = client.post(
        "/api/v1/auth/token",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "username": "johndoe",
            "password": "abcd",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


def test_login_access_token_incorrect_password():
    from fastapi.testclient import TestClient

    from src.fast_drive import app

    client = TestClient(app)

    response = client.post(
        "/api/v1/auth/token",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "username": "johndoe",
            "password": "error_password",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"
