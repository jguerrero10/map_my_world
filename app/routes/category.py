from fastapi import APIRouter

from app.database import categories_collection
from app.models import Category

category_router = APIRouter()

@category_router.post("/")
async def create_category(category: Category):
    result = await categories_collection.insert_one(dict(category))
    return {"id": str(result.inserted_id)}

