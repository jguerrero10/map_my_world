from datetime import datetime, timedelta, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_reviews_collection
from app.models import LocationCategoryReview, ResponseGeneral
from app.utils.enums import StatusEnum

recommender_router = APIRouter()


@recommender_router.get("/", response_model=ResponseGeneral, description="Get exploration recommendations.")
async def exploration_recommendations(reviews_collection=Depends(get_reviews_collection)):
    if reviews_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database connection not available."
        )
    try:
        date_threshold = datetime.now(timezone.utc) - timedelta(days=30)

        never_reviewed = await reviews_collection.find({"last_reviewed": None}).to_list(length=None)
        older_reviews = await reviews_collection.find({"last_reviewed": {"$lt": date_threshold}}).to_list(length=None)

        if not never_reviewed and not older_reviews:
            return ResponseGeneral(
                status=StatusEnum.SUCCESS, message="No exploration recommendations available.", data=[]
            )

        recommendations = never_reviewed + older_reviews
        recommendations = recommendations[:10]

        recommendations_json = [LocationCategoryReview(**review).to_json() for review in recommendations]

        return ResponseGeneral(
            status=StatusEnum.SUCCESS,
            message="Exploration recommendations retrieved successfully.",
            data=recommendations_json,
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@recommender_router.patch("/", response_model=ResponseGeneral, description="Update review.")
async def update_review(location_id: str, reviews_collection=Depends(get_reviews_collection)):
    if reviews_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database connection not available."
        )
    try:
        location_id = ObjectId(location_id)
    except InvalidId as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    review = await reviews_collection.find_one({"_id": location_id})
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found.")
    try:

        review["last_reviewed"] = datetime.now(timezone.utc)
        await reviews_collection.update_one({"_id": location_id}, {"$set": review})

        return ResponseGeneral(
            status=StatusEnum.SUCCESS,
            message="Review updated successfully.",
            data=[
                LocationCategoryReview(**review),
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
