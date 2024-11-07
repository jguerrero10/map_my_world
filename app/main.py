from fastapi import FastAPI

from app.routes.category import category_router
from app.routes.location import location_router
from app.routes.recommender import recommender_router

app = FastAPI()

app.include_router(category_router, prefix="/category", tags=["Category"])
app.include_router(location_router, prefix="/location", tags=["Location"])
app.include_router(recommender_router, prefix="/recommender", tags=["Recommender"])
