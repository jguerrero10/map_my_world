from fastapi import APIRouter

from app.utils.recommender import get_unreviewed_combinations

recommender_router = APIRouter()

@recommender_router.get("/")
async def recommend_locations():
    recommendations = await get_unreviewed_combinations()
    formatted_recommendations = [
        {
            "location_id": str(rec["location_id"]),
            "category_id": str(rec["category_id"])
        }
        for rec in recommendations
    ]
    return {"recommendations": formatted_recommendations}



