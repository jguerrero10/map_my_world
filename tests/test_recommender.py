import pytest
from fastapi.testclient import TestClient

from app.routes.recommendations_router import recommender_router


# Mock the get_unreviewed_combinations function
@pytest.fixture
def mock_get_unreviewed_combinations(monkeypatch):
    async def mock_return():
        return [{"location_id": 1, "category_id": 101}, {"location_id": 2, "category_id": 102}]

    monkeypatch.setattr("app.utils.recommender.get_unreviewed_combinations", mock_return)


client = TestClient(recommender_router)


@pytest.mark.asyncio
def test_recommend_locations_success(mock_get_unreviewed_combinations):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "recommendations": [{"location_id": "1", "category_id": "101"}, {"location_id": "2", "category_id": "102"}]
    }


@pytest.mark.asyncio
def test_recommend_locations_empty(mock_get_unreviewed_combinations, monkeypatch):
    async def mock_return_empty():
        return []

    monkeypatch.setattr("app.utils.recommender.get_unreviewed_combinations", mock_return_empty)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"recommendations": []}


@pytest.mark.asyncio
def test_recommend_locations_error(monkeypatch):
    async def mock_return_error():
        raise Exception("Database error")

    monkeypatch.setattr("app.utils.recommender.get_unreviewed_combinations", mock_return_error)
    response = client.get("/")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
