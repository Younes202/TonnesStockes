from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from beanie import Document


class Category(Document):
    name: str
    description: Optional[str]
    creation_date: datetime
    # parent_category: str
    # products: here i want retreive  a list of products which is in this category and make sure in insertion of  catgory when the user insert  category don't let the list of products as its necessery for the insertion  validation .

    class Config:
        json_schema_extra = {
            "example": {
                "name": "soso",
                "description": "lolo",
                "creation_date": "2022-01-01T12:00:00Z",
                # "parent_category": "parent_category_id",

            }
        }
        collection = "categories"


class CategoryUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    creation_date: Optional[str]
    # parent_category: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "creator": "soso",
                "name": "lolo",
                "description": "Category for electronic devices",
                "creation_date": "2022-01-01T12:00:00Z",
                # "parent_category": "parent_category_id",

            }
        }
