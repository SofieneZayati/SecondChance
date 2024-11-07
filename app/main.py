from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from app.models import User, UserInDB
from app.database import db
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

app = FastAPI()
templates = Environment(loader=FileSystemLoader("templates"))

# Web Endpoint using JINJA ------------------------------------------------------------------------------------ <-- Begin -->
@app.get("/")
@app.get("/index.html", tags=["UI"])
async def render_template(request: Request):
    try:
        template = templates.get_template("index.html")
        content = template.render(title="Login")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
    
@app.get("/")
@app.get("/register.html", tags=["UI"])
async def render_template(request: Request):
    try:
        template = templates.get_template("register.html")
        content = template.render(title="Register")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
    
@app.get("/")
@app.get("/dashboard.html", tags=["UI"])
async def render_template(request: Request):
    try:
        template = templates.get_template("dashboard.html")
        content = template.render(title="Dashboard")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")

# POST endpoint to create a new user
@app.post("/users", response_model=UserInDB)
async def create_user(user: User):
    # Check if the email already exists in the database
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use")

    # Create user data
    user_data = {
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

    # Insert the user into the database
    inserted_user = await db.users.insert_one(user_data)

    # Return the newly created user with its MongoDB ID
    new_user = {**user_data, "id": str(inserted_user.inserted_id)}
    return new_user


# GET endpoint to fetch all users or a specific user by email
@app.get("/users", response_model=List[UserInDB])
async def get_users(email: Optional[EmailStr] = Query(None)):
    if email:
        # If email is provided, fetch the specific user by email
        user = await db.users.find_one({"email": email})
        if user:
            # Convert MongoDB ObjectId to a string and return the user
            return [{**user, "id": str(user["_id"])}]
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        # If email is not provided, fetch all users
        users = await db.users.find().to_list(100)  # Adjust the limit as needed

        # Map users to include the id as a string
        valid_users = [{**user, "id": str(user["_id"])} for user in users]

        return valid_users

# PUT endpoint to update an existing user by their email
@app.put("/users/{user_email}", response_model=UserInDB)
async def update_user(user_email: str, user: User):
    # Find the user in the database by email
    existing_user = await db.users.find_one({"email": user_email})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user data in the database
    updated_data = {
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

    await db.users.update_one({"email": user_email}, {"$set": updated_data})

    # Return the updated user with the same email and MongoDB ID
    updated_user = {**updated_data, "id": str(existing_user["_id"])}
    return updated_user


# DELETE endpoint to remove a user by their email
@app.delete("/users/{user_email}", response_model=dict)
async def delete_user(user_email: str):
    # Find the user by email to ensure they exist
    user = await db.users.find_one({"email": user_email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user from the database
    await db.users.delete_one({"email": user_email})

    # Return a success message
    return {"message": f"User with email {user_email} has been deleted."}
