from datetime import datetime, timedelta

from app.database import categories_collection, locations_collection, reviews_collection


async def get_unreviewed_combinations():
    unreviewed = []
    recent_threshold = datetime.now() - timedelta(days=30)

    locations = await locations_collection.find({}).to_list(None)
    categories = await categories_collection.find({}).to_list(None)

    for location in locations:
        for category in categories:
            review = await reviews_collection.find_one({"location_id": location["_id"], "category_id": category["_id"]})
            if not review or (review["last_reviewed"] < recent_threshold):
                unreviewed.append({"location_id": location["_id"], "category_id": category["_id"]})

            if len(unreviewed) >= 10:
                return unreviewed

    return unreviewed
