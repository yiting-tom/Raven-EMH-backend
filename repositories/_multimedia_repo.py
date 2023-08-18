"""
_multimedia_repo.py

This module contains the MultimediaRepo class, which handles interactions between
the FastAPI application and the underlying database for multimedia objects.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - MultimediaRepo: Repository for handling database interactions related to multimedia objects.
"""

from typing import Any, List, Optional

from bson import ObjectId
from gridfs import GridFS
from pymongo.collection import Collection
from pymongo.database import Database

from models._multimedia import MultimediaCreate, MultimediaInDB
from repositories._base_repo import BaseRepo, IdNotFoundError
from utils.logger import logger


class MultimediaRepo(BaseRepo):
    """
    Repository for handling database interactions related to multimedia objects.

    Attributes:
        grid_fs (GridFS): An instance of GridFS for handling file storage.
    """
    COLLECTION_NAME = "multimedia"

    def __init__(self, database: Database, collection: Collection, grid_fs: GridFS):
        """
        Initialize the MultimediaRepo instance.

        Args:
            database (Database): The MongoDB database instance.
            collection (Collection): The MongoDB collection for storing multimedia objects.
            grid_fs (GridFS): The GridFS instance for handling file storage.
        """
        super().__init__(database, collection)
        self.grid_fs = grid_fs

    def create(self, data: MultimediaCreate) -> MultimediaInDB:
        """
        Create a new multimedia object in the database.

        Args:
            data (MultimediaCreate): The data of the multimedia object to be created.

        Returns:
            MultimediaInDB: The created multimedia object.
        """
        file_id = self.grid_fs.put(
            data=data.file_data,
        )
        multimedia = MultimediaInDB(
            id=str(file_id),
            **data.model_dump(),
        )
        out = self.collection.insert_one(multimedia.model_dump())
        logger.info(f"Multimedia {multimedia.id} created {out.inserted_id}")
        return multimedia

    def find_by_id(self, id: str) -> MultimediaInDB:
        """
        Retrieve a multimedia object by its id from the database.

        Args:
            id (str): The id of the multimedia object to be retrieved.

        Returns:
            MultimediaInDB: The found multimedia object.

        Raises:
            IdNotFoundError: If the multimedia object with the specified id is not found in the database.
        """
        multimedia_dict = self.collection.find_one({"_id": ObjectId(id)})
        if multimedia_dict:
            multimedia_in_db = MultimediaInDB(**self._id2str(multimedia_dict))
            logger.info(f"Multimedia found {multimedia_in_db.id}")
            return multimedia_in_db
        raise IdNotFoundError(f"Multimedia with id {id} not found")

    def find_all(self) -> List[MultimediaInDB]:
        """
        Retrieve all multimedia objects from the database.

        Returns:
            List[MultimediaInDB]: A list of found multimedia objects.
        """
        result = [
            MultimediaInDB(**self._id2str(multimedia_in_db))
            for multimedia_in_db in self.collection.find()
        ]
        logger.info(f"Multimedia found {len(result)}")
        return result

    def update(self, id: Any, updated_data: Any) -> None:
        """
        Update a multimedia object in the database. Currently not implemented.

        Args:
            id (Any): The id of the multimedia object to be updated.
            updated_data (Any): The new data for the multimedia object.

        Raises:
            NotImplementedError: If this method is invoked.
        """
        raise NotImplementedError

    def delete(self, id: Any):
        """
        Delete a multimedia object with the given id from the database.

        Args:
            id (Any): The id of the multimedia object to be deleted.
        """
        self.collection.delete_one({"_id": ObjectId(id)})
        self.grid_fs.delete(ObjectId(id))
        logger.info(f"Multimedia {id} deleted")
