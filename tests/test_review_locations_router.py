from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.main import app
from app.models import Category, Location, LocationCategoryReviewCreate
from app.utils.enums import StatusEnum

transport = httpx.ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_location_with_tag_success():
    location_data = LocationCategoryReviewCreate(
        location=Location(**{"latitude": 10.36288, "longitude": -74.119442}), category=Category(name="Test Category")
    )
    mock_inserted_id = "60f71876f0656d240846c124"

    # Mock de `insert_one` y `find_one`
    with patch("app.database.reviews_collection.insert_one", new_callable=AsyncMock) as mock_insert_one, patch(
        "app.database.reviews_collection.find_one", new_callable=AsyncMock
    ) as mock_find_one:
        mock_insert_one.return_value.inserted_id = mock_inserted_id
        mock_find_one.return_value = {
            "_id": mock_inserted_id,
            "location": {"latitude": 10.36288, "longitude": -74.119442},
            "category": {"name": "Test Category"},
            "last_reviewed": None,
        }

        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/review/", json=location_data.to_json())
            assert response.status_code == 200
            assert response.json() == {
                "status": StatusEnum.SUCCESS,
                "message": "Location category review added successfully",
                "data": [
                    {
                        "_id": mock_inserted_id,
                        "location": {"latitude": 10.36288, "longitude": -74.119442},
                        "category": {"name": "Test Category"},
                        "last_reviewed": None,
                    }
                ],
            }


@pytest.mark.asyncio
async def test_create_location_with_tag_validation_error():
    incomplete_location_data = {"category": {"name": "Test Category"}}

    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/review/", json=incomplete_location_data)
        assert response.status_code == 422
        assert "detail" in response.json()
        assert response.json()["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_create_location_with_tag_connection_error():
    location_data = LocationCategoryReviewCreate(
        location=Location(**{"latitude": 10.36288, "longitude": -74.119442}), category=Category(name="Test Category")
    )

    # Mock de `insert_one` para lanzar un `ConnectionError`
    with patch("app.database.reviews_collection.insert_one", new_callable=AsyncMock) as mock_insert_one:
        mock_insert_one.side_effect = ConnectionError("Database connection error")

        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/review/", json=location_data.to_json())
            assert response.status_code == 503
            assert response.json() == {"detail": "Database connection error"}


@pytest.mark.asyncio
async def test_create_location_with_tag_unexpected_error():
    location_data = LocationCategoryReviewCreate(
        location=Location(**{"latitude": 10.36288, "longitude": -74.119442}), category=Category(name="Test Category")
    )

    # Mock de `insert_one` para lanzar una excepción genérica
    with patch("app.database.reviews_collection.insert_one", new_callable=AsyncMock) as mock_insert_one:
        mock_insert_one.side_effect = Exception("Unexpected error")

        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/review/", json=location_data.to_json())
            assert response.status_code == 500
            assert response.json() == {"detail": "Unexpected error"}


@pytest.mark.asyncio
async def test_create_location_with_tag_out_of_range_location():
    out_of_range_location_data = {
        "location": {"latitude": 95.0, "longitude": -74.119442},
        "category": {"name": "Test Category"},
    }

    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/review/", json=out_of_range_location_data)
        assert response.status_code == 422
        assert "detail" in response.json()
        assert response.json()["detail"][0]["msg"] == "Input should be less than or equal to 90"
