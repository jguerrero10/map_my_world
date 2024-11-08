from fastapi import APIRouter, Body, HTTPException, status

from app.database import reviews_collection
from app.models import LocationCategoryReview, LocationCategoryReviewCreate, ResponseGeneral
from app.utils.enums import StatusEnum

review_router = APIRouter()


@review_router.post("/", response_model=ResponseGeneral, description="Create a location category review.")
async def create_location_with_tag(
    location_category_review: LocationCategoryReviewCreate = Body(
        ..., title="Location Category Review", description="The location and category to be reviewed"
    )
):
    try:
        result = await reviews_collection.insert_one(location_category_review.to_json())
        data = await reviews_collection.find_one({"_id": result.inserted_id})
        return ResponseGeneral(
            status=StatusEnum.SUCCESS,
            message="Location category review added successfully",
            data=[
                LocationCategoryReview(**data),
            ],
        )
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
