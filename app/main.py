from fastapi import FastAPI

from app.routes.exploration_recommender_router import recommender_router
from app.routes.review_locations_router import review_router

app = FastAPI(
    title="Exploration Recommender API",
    description="API for exploration recommendations and location reviews.",
    version="2.0.0",
)

app.include_router(recommender_router, prefix="/exploration-recommendations", tags=["Exploration Recommender"])
app.include_router(review_router, prefix="/review", tags=["Review"])
