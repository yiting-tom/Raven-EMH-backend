from typing import List, Optional

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database

from models import ChatInDB, ChatInDBCreate, ChatInDBUpdate
from loguru import logger


class ChatRepo:
    def __init__(self, db: Database, collection: Collection):
        # Create a MongoClient and specify the database and collection
        self.db: Database = db
        self.collection: Collection = collection

    def create_chat(self, chat: ChatInDBCreate) -> str:
        # Insert a new chat document into the database and return its id
        result = self.collection.insert_one(chat.model_dump())
        logger.info(f"Created chat with id {result.inserted_id}")
        return str(result.inserted_id)

    def get_chat(self, chat_id: str) -> Optional[ChatInDB]:
        # Find a chat document by its id
        chat_data = self.collection.find_one({"_id": ObjectId(chat_id)})
        if chat_data:
            logger.info(f"Found chat with id {chat_id}")
            return ChatInDB(**self.object_id_to_str(chat_data))
        return None

    def update_chat(self, chat_id: str, chat: ChatInDBUpdate) -> Optional[ChatInDB]:
        # Find a chat document by its id
        chat_data = self.collection.find_one_and_update(
            filter={"_id": ObjectId(chat_id)},
            update={"$set": chat.model_dump(exclude_none=True)},
        )
        if chat_data:
            logger.info(f"Updated chat with id {chat_id}")
            return ChatInDB(**self.object_id_to_str(chat_data))
        return None

    def get_chat_by_user_id_and_robot_id(
        self,
        user_id: str,
        robot_id: str,
    ) -> Optional[ChatInDB]:
        # Find a chat document by its id
        chat_data = self.collection.find_one({"user_id": user_id, "robot_id": robot_id})
        if chat_data:
            logger.info(f"Found chat with user_id {user_id} and robot_id {robot_id}")
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

        logger.info(
            f"Found {len(result)} chats with user_id {user_id} and robot_id {robot_id}"
        )
        return result  # Ensure a list is always returned

    def delete_chat(self, chat_id: str) -> bool:
        # Delete a chat document by its id and return whether the operation was successful
        result = self.collection.delete_one({"_id": ObjectId(chat_id)})
        logger.info(f"Deleted chat with id {chat_id}")
        return result.deleted_count > 0

    def delete_chats(self, chat_ids: list[str]) -> bool:
        # Delete a chat document by its id and return whether the operation was successful
        result = self.collection.delete_many(
            {"_id": {"$in": [ObjectId(_id) for _id in chat_ids]}}
        )
        logger.info(f"Deleted chats with ids {chat_ids}")
        return result.deleted_count > 0
