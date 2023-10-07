from typing import List, Optional

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database

from models import ChatInDB, ChatInDBCreate


class ChatRepo:
    def __init__(self, db: Database, collection: Collection):
        # Create a MongoClient and specify the database and collection
        self.db: Database = db
        self.collection: Collection = collection

    def create_chat(self, chat: ChatInDBCreate) -> str:
        # Insert a new chat document into the database and return its id
        result = self.collection.insert_one(chat.model_dump())
        return str(result.inserted_id)

    def get_chat(self, chat_id: str) -> Optional[ChatInDB]:
        # Find a chat document by its id
        chat_data = self.collection.find_one({"_id": ObjectId(chat_id)})
        if chat_data:
            return ChatInDB(**chat_data)
        return None

    def get_chat_by_user_id_and_robot_id(
        self,
        user_id: str,
        robot_id: str,
    ) -> Optional[ChatInDB]:
        # Find a chat document by its id
        chat_data = self.collection.find_one({"user_id": user_id, "robot_id": robot_id})
        if chat_data:
            return ChatInDB(**self.object_id_to_str(chat_data))
        return None

    @staticmethod
    def object_id_to_str(obj):
        obj["id"] = str(obj["_id"])
        del obj["_id"]
        return obj

    def get_chats_by_user_id_and_robot_id(
        self,
        user_id: str,
        robot_id: str,
        order_by: Optional[str] = "created_at",
    ) -> List[ChatInDB]:
        # Find a chat document by its id
        chat_data = self.collection.find({"user_id": user_id, "robot_id": robot_id})

        if chat_data is None:
            return []

        result = [ChatInDB(**self.object_id_to_str(chat)) for chat in chat_data]
        if order_by:
            result.sort(key=lambda x: getattr(x, order_by))

        return result  # Ensure a list is always returned

    def delete_chat(self, chat_id: str) -> bool:
        # Delete a chat document by its id and return whether the operation was successful
        result = self.collection.delete_one({"_id": ObjectId(chat_id)})
        return result.deleted_count > 0
