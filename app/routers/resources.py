from fastapi import APIRouter, Depends
from app.auth import require_admin, get_current_user

router = APIRouter()

# Admin route to manage all users
@router.get("/users", dependencies=[Depends(require_admin)])
async def list_users():
    users = await db.users.find().to_list(100)
    return users

# Shared resource route accessible to all authenticated roles
@router.get("/resources")
async def get_resources(current_user: dict = Depends(get_current_user)):
    resources = await db.resources.find().to_list(100)
    return resources

# Admin-only route to create a new resource
@router.post("/resources", dependencies=[Depends(require_admin)])
async def create_resource(data: dict):
    new_resource = await db.resources.insert_one(data)
    return {"id": str(new_resource.inserted_id)}
