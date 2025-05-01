# database.py

import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from app.shared_tools import get_clients_data
from app.config import MONGODB_URI_LOCAL, MONGODB_URI_REMOTE

# MongoDB setup
client = AsyncIOMotorClient(MONGODB_URI_LOCAL) # Uncomment this line to use local MongoDB
# client = AsyncIOMotorClient(MONGODB_URI_REMOTE)  # Uncomment this line to use remote MongoDB
db = client["Notification"]
collection = db["NOTY"]  # collection name

async def insert_notification(message: str):
    clients_data = await get_clients_data()
    await collection.insert_one({
        "_id": str(uuid.uuid4()),  # Use UUID for unique ID generation
        "type": "notification",
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subscribed_clients": clients_data["subscribers"]
    })


async def get_notifications():
    notifications = await collection.find().to_list(length=None)
    return notifications