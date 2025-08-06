from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_plan():
    response = client.post("/api/plan", data={
        "wall_width": 5,
        "wall_height": 5,
        "obs_x": 2,
        "obs_y": 2,
        "obs_w": 1,
        "obs_h": 1
    })
    assert response.status_code == 200
    assert response.json()["steps"] == 24  # 5x5 = 25 - 1 obstacle
