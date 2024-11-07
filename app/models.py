from datetime import datetime

from pydantic import BaseModel, Field
from typing_extensions import Optional


class Location(BaseModel):
    latitude: float = Field(
        ...,
        title="Latitude",
        description="The latitude of the location",
        ge=-90,
        le=90
    )
    longitude: float = Field(
        ...,
        title="Longitude",
        description="The longitude of the location",
        ge=-180,
        le=180
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "latitude": 10.36288,
                    "longitude": -74.119442,
                }
            ]
        }
    }

class Category(BaseModel):
    name: str = Field(
        ...,
        title="Category name",
        description="The name of the category"
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                }
            ]
        }
    }

class LocationCategoryReview(BaseModel):
    location_id: str = Field(
        ...,
        title="Location ID",
        description="The ID of the location"
    )
    category_id: str = Field(
        ...,
        title="Category ID",
        description="The ID of the category"
    )
    last_reviewed: Optional[datetime] = Field(None, title="Last Reviewed", description="The last time the category was reviewed")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                    "category_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                    "last_reviewed": "2022-01-01T00:00:00"
                }
            ]
        }
    }