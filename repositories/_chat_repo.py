"""
_chat_repo.py

This module contains the ChatRepo class, which handles interactions between
the FastAPI application and the underlying database for chat objects.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - ChatRepo: Repository for handling database interactions related to chat objects.
"""

from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database

from models._chat import ChatCreate, ChatInDB, ChatUpdate
from repositories._base_repo import BaseRepo, IdNotFoundError
from utils.logger import logger


class ChatRepo(BaseRepo):
    """
    Repository for handling database interactions related to chat objects.

    Attributes:
        COLLECTION_NAME (str): The name of the MongoDB collection for storing chat objects.
    """

    COLLECTION_NAME = "chat"

    def __init__(self, database: Database, collection: Collection):
        """
        Initialize the ChatRepo instance.

        Args:
            database (Database): The MongoDB database instance.
            collection (Collection): The MongoDB collection for storing chat objects.
        """
        super().__init__(database, collection)

    def create(self, data: ChatCreate) -> ChatInDB:
        """
        Create a new chat object in the database.

        Args:
            data (ChatCreate): The data of the chat object to be created.

        Returns:
            ChatInDB: The created chat object.
        """
        chat = self.collection.insert_one(data.model_dump())
        logger.info(f"Chat created {chat.inserted_id}")
        return ChatInDB(
            id=str(chat.inserted_id),
            **data.model_dump(),
        )

    def find_by_id(self, id: str) -> ChatInDB:
        """
        Retrieve a chat object by its id from the database.

        Args:
            id (str): The id of the chat object to be retrieved.

        Returns:
            ChatInDB: The found chat object.

        Raises:
            IdNotFoundError: If the chat object with the specified id is not found in the database.
        """
        chat_dict = self.collection.find_one({"_id": ObjectId(id)})
        if chat_dict:
            chat_in_db = ChatInDB(**self._id2str(chat_dict))
            logger.info(f"Chat found {chat_in_db.id}")
            return chat_in_db
        raise IdNotFoundError(f"Chat with id {id} not found")

    def find_all(self) -> List[ChatInDB]:
        """
        Retrieve all chat objects from the database.

        Returns:
            List[ChatInDB]: A list of found chat objects.
        """
        result = [
            ChatInDB(**self._id2str(chat_in_db))
            for chat_in_db in self.collection.find()
        ]
        logger.info(f"Chat found {len(result)}")
        return result

    def update(self, id: Any, updated_data: ChatUpdate) -> ChatInDB:
        """
        Update a chat object in the database.

        Args:
            id (Any): The id of the chat object to be updated.
            updated_data (ChatUpdate): The new data for the chat object.

        Returns:
            ChatInDB: The updated chat object.
        """
        self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_data.model_dump(exclude_unset=True)},
        )
        chat_in_db = self.find_by_id(id)
        logger.info(f"Chat {id} updated")
        return chat_in_db

    def delete(self, id: Any):
        """
        Delete a chat object with the given id from the database.

        Args:
            id (Any): The id of the chat object to be deleted.
        """
        self.collection.delete_one({"_id": ObjectId(id)})
        logger.info(f"Chat {id} deleted")

    def find_by_user_id(self, user_id: str, query: Optional[Dict] = None):
        """
        Retrieve all chat objects by user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            List[ChatInDB]: A list of all chat objects by user ID.
        """
        query = query or {}
        query["user_id"] = user_id
        result = [
            ChatInDB(**self._id2str(chat_in_db))
            for chat_in_db in self.collection.find(query)
        ]
        logger.info(f"Chat found {len(result)}")
        return result
