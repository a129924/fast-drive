def test_string_io():
    from fastapi.testclient import TestClient

    from src.fast_drive import app

    client = TestClient(app)

    tasks = [client.get("/api/v1/test/") for _ in range(2)]

    for result in tasks:
        assert result.status_code == 200
