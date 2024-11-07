from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import create_access_token, verify_password
from app.models import User, db  # Adjust this to your database setup
from pydantic import BaseModel

router = APIRouter()

# Request models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str  # e.g., "normal", "doctor", "legal_assistant", "admin"

class UserLogin(BaseModel):
    email: str
    password: str

# Route to register a new user
@router.post("/register")
async def register_user(user: UserCreate):
    hashed_password = verify_password(user.password, user.password)
    user.password = hashed_password
    new_user = await db.users.insert_one(user.dict())
    return {"id": str(new_user.inserted_id)}

# Route to log in and get a JWT token
@router.post("/login")
async def login_user(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token({"user_id": str(db_user["_id"]), "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}
