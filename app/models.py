from datetime import datetime
from typing import Annotated, Any, List

from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Optional

from app.utils.enums import StatusEnum

PyObjectId = Annotated[str, BeforeValidator(str)]


class Location(BaseModel):
    latitude: float = Field(..., title="Latitude", description="The latitude of the location", ge=-90, le=90)
    longitude: float = Field(..., title="Longitude", description="The longitude of the location", ge=-180, le=180)
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

    def to_json(self):
        return {"latitude": self.latitude, "longitude": self.longitude}


class Category(BaseModel):
    name: str = Field(..., title="Category name", description="The name of the category")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                }
            ]
        }
    }

    def to_json(self):
        return {"name": self.name}


class LocationCategoryReviewCreate(BaseModel):
    location: Location = Field(..., title="Location", description="The location being reviewed")
    category: Category = Field(..., title="Category", description="The category being reviewed")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": {
                        "latitude": 10.36288,
                        "longitude": -74.119442,
                    },
                    "category": {
                        "name": "Foo",
                    },
                }
            ]
        }
    }

    def to_json(self):
        return {"location": self.location.to_json(), "category": self.category.to_json()}


class LocationCategoryReview(LocationCategoryReviewCreate):
    id: Optional[PyObjectId] = Field(
        alias="_id", default=None, title="Category ID", description="The ID of the category"
    )
    last_reviewed: Optional[datetime] = Field(
        None, title="Last Reviewed", description="The last time the category was reviewed"
    )

    def to_json(self):
        return {
            "_id": self.id,
            "location": self.location.to_json(),
            "category": self.category.to_json(),
            "last_reviewed": self.last_reviewed,
        }


class ResponseGeneral(BaseModel):
    status: StatusEnum = Field(..., title="Status", description="The response status")
    data: Optional[List[Any]] = Field(None, title="Data", description="The response data")
    message: str = Field(..., title="Message", description="The response message")
    model_config = {
        "json_schema_extra": {
            "examples": [{"status": "Success", "data": [], "message": "Request processed successfully"}]
        }
    }
