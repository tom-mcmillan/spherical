from fastapi.testclient import TestClient
from app.main import app

def test_process_returns_candidates():
    client = TestClient(app)
    response = client.post("/process", json={"request": "Find AI consultants for strategy"})
    assert response.status_code == 200
    data = response.json()
    # Expect at least 3 fallback candidates
    assert "candidates" in data
    assert isinstance(data["candidates"], list)
    assert len(data["candidates"]) >= 3
    first = data["candidates"][0]
    assert "name" in first and "profile_url" in first and "benefit" in first