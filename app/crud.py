from app.database import db
from app.models import UserInDB, UserBase
from bson import ObjectId
from typing import List

# Utility function to convert ObjectId to string (for serialization)
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }

# Create a new user in the database
async def create_user(user: UserBase):
    user_dict = user.dict()
    result = await db.users.insert_one(user_dict)
    new_user = await db.users.find_one({"_id": result.inserted_id})
    return user_helper(new_user)

# Get all users from the database
async def get_users() -> List[UserInDB]:
    users = await db.users.find().to_list(100)
    return [user_helper(user) for user in users]
