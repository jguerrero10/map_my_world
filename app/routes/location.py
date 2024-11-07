from fastapi import APIRouter

from app.database import locations_collection
from app.models import Location

location_router = APIRouter()

@location_router.post("/")
async def create_location(location: Location):
    result = await locations_collection.insert_one(dict(location))
    return {"id": str(result.inserted_id)}
