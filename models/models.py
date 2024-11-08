from pydantic import BaseModel, EmailStr,validator
#from bson import ObjectId
from app.db.database import db  # Import db from the database connection file
from typing import List, Optional

# Pydantic models for request and response
class User(BaseModel):
    username: str
    email: EmailStr  # Email validation is handled by EmailStr
    role: str  # 'user', 'doctor', 'admin', etc.

    class Config:
        # To allow the 'id' field in MongoDB to be converted to a string
        orm_mode = True


# Pydantic model for the user data (ensure this matches the MongoDB fields)
class UserInDB(BaseModel):
    id: str
    name: Optional[str] = None
    email: str  # Email field as EmailStr
    password: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    role: str

    @validator("email")
    def validate_email(cls, v):
        return v

    class Config:
        orm_mode = True