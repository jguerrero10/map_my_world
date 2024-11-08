import os

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.map_my_world
locations_collection = db.locations
categories_collection = db.categories
reviews_collection = db.location_category_reviews


def get_reviews_collection():
    return reviews_collection
