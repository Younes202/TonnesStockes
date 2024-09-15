import uuid
from typing import Optional
import logging

from beanie import init_beanie, PydanticObjectId
from users.model import User
from categories.model import Category
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from fastapi import UploadFile, HTTPException
import os

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    SECRET_KEY: Optional[str] = os.environ["SECRET_KEY"]

    async def initialize_database(self):
        try:
            # Connect to the database
            client = AsyncIOMotorClient(self.DATABASE_URL)
            database = client.get_default_database()

            # Initialize Beanie with document models
            await init_beanie(database=database,
                              document_models=[User, Category])

            # Log collection names
            collection_names = await database.list_collection_names()
            print(collection_names)
            logger.info(f"Collections in the database: {collection_names}")

            return database  # Corrected line

        except Exception as e:
            logger.exception(f"Exception during database initialization: {e}")
            raise


async def get_database():
    settings = Settings()
    database = await settings.initialize_database()
    return Database(database=database)  # Use the 'database' attribute


class Config:
    env_file = ".env"


class Database:
    def __init__(self, database=None):
        self.database = database

    async def save(self, document) -> None:
        await document.create()

    async def count_documents_number(self, name_document: str) -> int:
        try:
            count = await self.database[name_document].count_documents({})
            return int(count)  # Convert count to an integer        except Exception:
        except Exception:
            logger.exception("Exception during counting documents : ")
            raise

    async def get(self, idd: str) -> any:
        doc = await self.database.get(PydanticObjectId(idd))
        if doc:
            return doc
        return False

    async def get_last_creation(self, field: str):
        try:
            cursor = self.database.find().sort([("creation_date", -1)]).limit(1)
            async for document in cursor:
                return getattr(document, field, None)
        except Exception as e:
            print(f"Error in get_last_creation: {e}")
            raise

    async def get_all(self) -> list[any]:
        docs = await self.database.find_all().to_list()
        return docs

    async def update(self, idd: PydanticObjectId, body: BaseModel) -> any:
        doc_id = idd
        des_body = body.dict()

        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {field: value for field, value in des_body.items()}}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def find_one(self, collection_name: str, query: str):
        collection = self.database[collection_name]
        document = await collection.find_one(PydanticObjectId(query))
        return document

    async def delete(self, idd: PydanticObjectId) -> bool:
        doc = await self.get(idd)
        if doc:
            await doc.delete()
            return True
        else:
            return False