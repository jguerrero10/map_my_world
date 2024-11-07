from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app

transport = httpx.ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_location():
    mock_insert_result = AsyncMock()
    mock_insert_result.inserted_id = "mocked_id"

    with patch(
        "app.database.locations_collection.insert_one", new=AsyncMock(return_value=mock_insert_result)
    ) as mock_insert:
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/location/", json={"latitude": 1.0, "longitude": 1.0})
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert "id" in data
            assert data["id"] == "mocked_id"

        mock_insert.assert_called_once_with({"latitude": 1.0, "longitude": 1.0})


@pytest.mark.asyncio
async def test_create_location_missing_data():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/location/", json={"latitude": 1.0})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
