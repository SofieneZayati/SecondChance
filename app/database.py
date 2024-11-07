from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

# Database setup
client = AsyncIOMotorClient("mongodb://localhost:27017")  # Use your actual MongoDB URI
db = client.secondchance  # Replace with your actual database name
