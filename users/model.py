from beanie import Document, init_beanie
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings


class User(Document):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }
        collection = "users"


# Initialize beanie


class TokenResponse(BaseModel):
    access_token: str
    token_type: str