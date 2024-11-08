from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from bson import ObjectId

from app.database import get_reviews_collection
from app.main import app
from app.utils.enums import StatusEnum

transport = httpx.ASGITransport(app=app)


@pytest.mark.asyncio
async def test_exploration_recommendations():
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/exploration-recommendations/")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_exploration_recommendations_error():
    with patch("app.database.reviews_collection.find") as mock_find:
        mock_find.return_value = AsyncMock()
        mock_find.return_value.to_list = AsyncMock(return_value=[])

        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.get("/exploration-recommendations/")
            assert response.status_code == 200
            assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_exploration_recommendations_no_database_connection():
    app.dependency_overrides[get_reviews_collection] = lambda: None

    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/exploration-recommendations/")
        assert response.status_code == 503
        assert response.json()["detail"] == "Database connection not available."

    app.dependency_overrides.pop(get_reviews_collection)


@pytest.mark.asyncio
async def test_mock_collection_find_to_list():
    mock_data = [
        {
            "_id": str(ObjectId()),
            "location": {"latitude": 10.36288, "longitude": -74.119442},
            "category": {"name": "Foo"},
            "last_reviewed": None,
        },
        {
            "_id": str(ObjectId()),
            "location": {"latitude": 12.34, "longitude": -56.78},
            "category": {"name": "Bar"},
            "last_reviewed": (datetime.now(timezone.utc) - timedelta(days=40)).isoformat().replace("+00:00", "Z"),
        },
    ]

    with patch("app.database.reviews_collection.find") as mock_find_never:
        mock_find_never.return_value = AsyncMock()

        mock_find_never.return_value.to_list = AsyncMock(return_value=mock_data)

        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.get("/exploration-recommendations/")
            assert response.status_code == 200
            assert response.json()["data"] == (mock_data + mock_data)[:10]


@pytest.mark.asyncio
async def test_update_review_success():
    location_id = str(ObjectId())
    mock_review_data = {
        "_id": location_id,
        "location": {"latitude": 10.36288, "longitude": -74.119442},
        "category": {"name": "Test Category"},
        "last_reviewed": None,
    }

    # Mock para `find_one` y `update_one`
    with patch("app.database.reviews_collection.find_one", new_callable=AsyncMock) as mock_find_one, patch(
        "app.database.reviews_collection.update_one", new_callable=AsyncMock
    ) as mock_update_one:
        mock_find_one.return_value = mock_review_data
        mock_update_one.return_value = AsyncMock()

        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.patch(f"/exploration-recommendations/?location_id={location_id}")
            assert response.status_code == 200

            response_data = response.json()
            assert response_data["status"] == StatusEnum.SUCCESS.value
            assert response_data["message"] == "Review updated successfully."
            assert response_data["data"][0]["_id"] == location_id
            assert response_data["data"][0]["location"] == {"latitude": 10.36288, "longitude": -74.119442}
            assert response_data["data"][0]["category"] == {"name": "Test Category"}

            response_last_reviewed = datetime.fromisoformat(
                response_data["data"][0]["last_reviewed"].replace("Z", "+00:00")
            )
            expected_last_reviewed = datetime.now(timezone.utc).replace(microsecond=0)
            assert response_last_reviewed.replace(microsecond=0) == expected_last_reviewed


@pytest.mark.asyncio
async def test_update_review_no_database_connection():
    app.dependency_overrides[get_reviews_collection] = lambda: None

    location_id = str(ObjectId())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.patch(f"/exploration-recommendations/?location_id={location_id}")
        assert response.status_code == 503
        assert response.json()["detail"] == "Database connection not available."

    app.dependency_overrides.pop(get_reviews_collection)


@pytest.mark.asyncio
async def test_update_review_invalid_id():
    invalid_location_id = "invalid_object_id"

    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.patch(f"/exploration-recommendations/?location_id={invalid_location_id}")
        assert response.status_code == 422
        assert response.json()["detail"] == (
            "'invalid_object_id' is not a valid ObjectId, it must be a 12-byte input or a " "24-character hex string"
        )


@pytest.mark.asyncio
async def test_update_review_not_found():
    location_id = str(ObjectId())

    with patch("app.database.reviews_collection.find_one", new_callable=AsyncMock) as mock_find_one:
        mock_find_one.return_value = None

        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.patch(f"/exploration-recommendations/?location_id={location_id}")
            assert response.status_code == 404
            assert response.json()["detail"] == "Review not found."


@pytest.mark.asyncio
async def test_exploration_recommendations_with_database_error():
    with patch("app.database.reviews_collection.find", side_effect=Exception("Database error")):
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.get("/exploration-recommendations/")
            assert response.status_code == 500
            assert response.json()["detail"] == "Database error"


@pytest.mark.asyncio
async def test_exploration_recommendations_unexpected_error():
    with patch("app.database.reviews_collection.find", side_effect=Exception("Unexpected error")):
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.get("/exploration-recommendations/")
            assert response.status_code == 500
            assert response.json()["detail"] == "Unexpected error"


@pytest.mark.asyncio
async def test_update_review_unexpected_error():
    location_id = str(ObjectId())
    mock_review_data = {
        "_id": location_id,
        "location": {"latitude": 10.36288, "longitude": -74.119442},
        "category": {"name": "Test Category"},
        "last_reviewed": None,
    }

    with patch("app.database.reviews_collection.find_one", new_callable=AsyncMock) as mock_find_one, patch(
        "app.database.reviews_collection.update_one", side_effect=Exception("Unexpected update error")
    ):
        mock_find_one.return_value = mock_review_data

        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.patch(f"/exploration-recommendations/?location_id={location_id}")
            assert response.status_code == 500
            assert response.json()["detail"] == "Unexpected update error"
