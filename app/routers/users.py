from fastapi import APIRouter, Depends, HTTPException, status
#from app.auth import create_access_token, verify_password
from models.models import User, db  # Adjust this to your database setup
from pydantic import BaseModel

router = APIRouter()

# Define routers - APIs()
Register = APIRouter()
Login = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    age: int
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

@Register.post("/register", tags=["User Authentication"])
async def register_user(user: UserCreate):
    # Verify and hash password (you can add this step if required)
    # hashed_password = verify_password(user.password, user.password)
    # user.password = hashed_password
    
    # Insert user in database (assuming `db` is your database instance)
    new_user = await db.users.insert_one(user.dict())
    return {"id": str(new_user.inserted_id)}

# Route to log in and get a JWT token
@Login.post("/login", tags=["User Authentication"])
async def login_user(user: UserLogin):
    # Look for a user with the matching email and password
    db_user = await db.users.find_one({"email": user.email, "password": user.password})
    print("test" , db_user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # token = create_access_token({"user_id": str(db_user["_id"]), "role": db_user["role"]})
    return {"success": True, "message": "saha ya ghoul by legacy"}
