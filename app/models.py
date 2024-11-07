from pydantic import BaseModel, EmailStr
from bson import ObjectId
from app.database import db  # Import db from the database connection file

# Pydantic models for request and response
class User(BaseModel):
    username: str
    email: EmailStr  # Email validation is handled by EmailStr
    role: str  # 'user', 'doctor', 'admin', etc.

    class Config:
        # To allow the 'id' field in MongoDB to be converted to a string
        orm_mode = True



class UserInDB(BaseModel):
    id: str
    username: str
    email: EmailStr  # Ensuring email is validated as a valid email format
    role: str
