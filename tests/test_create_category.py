from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app

transport = httpx.ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_category():
    mock_insert_result = AsyncMock()
    mock_insert_result.inserted_id = "mocked_id"

    with patch(
        "app.database.categories_collection.insert_one", new=AsyncMock(return_value=mock_insert_result)
    ) as mock_insert:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/category/", json={"name": "Restaurante"})
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert "id" in data
            assert data["id"] == "mocked_id"

        mock_insert.assert_called_once_with({"name": "Restaurante"})


@pytest.mark.asyncio
async def test_create_category_missing_data():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/category/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_category_response_format():
    mock_insert_result = AsyncMock()
    mock_insert_result.inserted_id = "mocked_id"

    with patch(
        "app.database.categories_collection.insert_one", new=AsyncMock(return_value=mock_insert_result)
    ) as mock_insert:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/category/", json={"name": "Parque"})
            data = response.json()

            assert response.status_code == status.HTTP_201_CREATED
            assert "id" in data
            assert data["id"] == "mocked_id"
            assert isinstance(data["id"], str)

        mock_insert.assert_called_once_with({"name": "Parque"})


@pytest.mark.asyncio
async def test_create_category_invalid_data_type():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/category/", json={"name": 123})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
