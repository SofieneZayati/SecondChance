from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from models.models import User, UserInDB
from app.db.database import db
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from api.user_api import *
from app.routers.users import *

import uvicorn



tags_metadata = [
    {
        "name": "Users",
        "description": "All Users API",
    },
    {
        "name": "User Authentication",
        "description": "User Authentication API",
    },
]

app = FastAPI(
    title="Second Chance Project BACKEND PART",
    openapi_tags=tags_metadata,
    redoc_url=None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type"],
)


# Users Data Endpoints ------------------------------------------------------------- <-- Begin -->
app.include_router(PostUser)
app.include_router(GetUser)
app.include_router(DelUser)
app.include_router(UpdateUser)

app.include_router(Register)
app.include_router(Login)



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
    
@app.get("/")
@app.get("/home.html", tags=["UI"])
async def render_template(request: Request):
    try:
        template = templates.get_template("home.html")
        content = template.render(title="Home")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
    
@app.get("/")
@app.get("/chat.html", tags=["UI"])
async def render_template(request: Request):
    try:
        template = templates.get_template("chat.html")
        content = template.render(title="Chat")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
    
@app.get("/")
@app.get("/network.html", tags=["UI"])
async def render_template(request: Request):
    try:
        template = templates.get_template("network.html")
        content = template.render(title="Network")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
    
@app.get("/")
@app.get("/job.html", tags=["UI"])
async def render_template(request: Request):
    try:
        template = templates.get_template("job.html")
        content = template.render(title="Job")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
    
@app.get("/")
@app.get("/forms.html", tags=["UI"])
async def render_template(request: Request):
    try:
        template = templates.get_template("forms.html")
        content = template.render(title="Forms")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
    
@app.get("/")
@app.get("/profile.html", tags=["UI"])
async def render_template(request: Request):
    try:
        template = templates.get_template("profile.html")
        content = template.render(title="Profile")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
    








# APP Main Runner
if __name__ == "__main__":  
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=True)