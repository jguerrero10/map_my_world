from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest

from app.utils.recommender import get_unreviewed_combinations


@pytest.mark.asyncio
async def test_get_unreviewed_combinations_max_10():

    mock_locations = [{"_id": f"location{i}"} for i in range(3)]
    mock_categories = [{"_id": f"category{i}"} for i in range(5)]

    mock_reviews = None

    with patch("app.database.locations_collection.find") as mock_find_locations, patch(
        "app.database.categories_collection.find"
    ) as mock_find_categories, patch(
        "app.database.reviews_collection.find_one", new=AsyncMock(return_value=mock_reviews)
    ):
        mock_find_locations.return_value.to_list = AsyncMock(return_value=mock_locations)
        mock_find_categories.return_value.to_list = AsyncMock(return_value=mock_categories)

        unreviewed_combinations = await get_unreviewed_combinations()

        assert len(unreviewed_combinations) <= 10

        for combination in unreviewed_combinations:
            assert "location_id" in combination
            assert "category_id" in combination


@pytest.mark.asyncio
async def test_get_unreviewed_combinations_no_reviews():
    mock_locations = [{"_id": f"location{i}"} for i in range(2)]
    mock_categories = [{"_id": f"category{i}"} for i in range(2)]
    mock_reviews = None

    with patch("app.database.locations_collection.find") as mock_find_locations, patch(
        "app.database.categories_collection.find"
    ) as mock_find_categories, patch(
        "app.database.reviews_collection.find_one", new=AsyncMock(return_value=mock_reviews)
    ):

        mock_find_locations.return_value.to_list = AsyncMock(return_value=mock_locations)
        mock_find_categories.return_value.to_list = AsyncMock(return_value=mock_categories)

        unreviewed_combinations = await get_unreviewed_combinations()

        assert len(unreviewed_combinations) == 4
        for combination in unreviewed_combinations:
            assert "location_id" in combination
            assert "category_id" in combination


@pytest.mark.asyncio
async def test_get_unreviewed_combinations_with_recent_reviews():
    recent_threshold = datetime.now() - timedelta(days=30)
    mock_locations = [{"_id": "location1"}]
    mock_categories = [{"_id": "category1"}]
    mock_recent_review = {"last_reviewed": recent_threshold + timedelta(days=1)}

    with patch("app.database.locations_collection.find") as mock_find_locations, patch(
        "app.database.categories_collection.find"
    ) as mock_find_categories, patch(
        "app.database.reviews_collection.find_one", new=AsyncMock(return_value=mock_recent_review)
    ):

        mock_find_locations.return_value.to_list = AsyncMock(return_value=mock_locations)
        mock_find_categories.return_value.to_list = AsyncMock(return_value=mock_categories)

        unreviewed_combinations = await get_unreviewed_combinations()

        assert len(unreviewed_combinations) == 0


@pytest.mark.asyncio
async def test_get_unreviewed_combinations_with_old_reviews():
    recent_threshold = datetime.now() - timedelta(days=30)
    mock_locations = [{"_id": "location1"}]
    mock_categories = [{"_id": "category1"}]
    mock_old_review = {"last_reviewed": recent_threshold - timedelta(days=1)}

    with patch("app.database.locations_collection.find") as mock_find_locations, patch(
        "app.database.categories_collection.find"
    ) as mock_find_categories, patch(
        "app.database.reviews_collection.find_one", new=AsyncMock(return_value=mock_old_review)
    ):

        mock_find_locations.return_value.to_list = AsyncMock(return_value=mock_locations)
        mock_find_categories.return_value.to_list = AsyncMock(return_value=mock_categories)

        unreviewed_combinations = await get_unreviewed_combinations()

        assert len(unreviewed_combinations) == 1
        assert unreviewed_combinations[0]["location_id"] == "location1"
        assert unreviewed_combinations[0]["category_id"] == "category1"


@pytest.mark.asyncio
async def test_get_unreviewed_combinations_large_data():
    mock_locations = [{"_id": f"location{i}"} for i in range(10)]
    mock_categories = [{"_id": f"category{i}"} for i in range(10)]
    mock_reviews = None

    with patch("app.database.locations_collection.find") as mock_find_locations, patch(
        "app.database.categories_collection.find"
    ) as mock_find_categories, patch(
        "app.database.reviews_collection.find_one", new=AsyncMock(return_value=mock_reviews)
    ):

        mock_find_locations.return_value.to_list = AsyncMock(return_value=mock_locations)
        mock_find_categories.return_value.to_list = AsyncMock(return_value=mock_categories)

        unreviewed_combinations = await get_unreviewed_combinations()

        assert len(unreviewed_combinations) == 10
