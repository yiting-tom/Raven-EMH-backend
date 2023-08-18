"""
_base_repo.py

This module defines the abstract base class for the repository layer of the FastAPI application.
It provides a standardized way to interact with the underlying database.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - IdNotFoundError: Exception raised when the id of the data to be retrieved is not found.
    - BaseRepo: Abstract base class for the repository classes.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar
from pymongo.database import Database
from pymongo.collection import Collection
from utils.logger import logger

T = TypeVar("T")


class IdNotFoundError(Exception):
    """
    Raised when the id of the data to be retrieved is not found.
    """
    pass


class BaseRepo(ABC, Generic[T]):
    """
    Abstract base class for the repository classes.

    Each subclass should provide concrete implementations for the CRUD (Create, Read, Update, Delete) operations.

    Attributes:
        db (Database): The database connection object.
        collection (Collection): The MongoDB collection object associated with the repository.
    """
    
    def __init_subclass__(cls, **kwargs):
        """
        Ensure that subclasses define a COLLECTION_NAME class variable.
        """
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "COLLECTION_NAME"):
            raise NotImplementedError(
                f'{cls.__name__} must define a class variable named "COLLECTION_NAME"'
            )

    def __init__(self, db: Database, *args, **kwargs):
        """
        Initialize the repository with the given database.
        
        Args:
            db (Database): The database connection object.
        """
        self.db: Database = db
        if self.__class__.COLLECTION_NAME not in db.list_collection_names():
            db.create_collection(self.__class__.COLLECTION_NAME)
            logger.info(
                f'Collection "{self.__class__.COLLECTION_NAME}" created in database "{db.name}"'
            )
        else:
            logger.info(
                f'Collection "{self.__class__.COLLECTION_NAME}" already exists in database "{db.name}"'
            )
        self.collection: Collection = self.db[self.__class__.COLLECTION_NAME]

    @abstractmethod
    def create(self, data: T) -> Any:
        """
        Save the given data.
        
        Args:
            data (T): The data to be saved.
        
        Returns:
            Any: The saved data object.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: Any) -> Optional[T]:
        """
        Retrieve data by its id.
        
        Args:
            id (Any): The id of the data to be retrieved.
        
        Returns:
            Optional[T]: The retrieved data object, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[T]:
        """
        Retrieve all data.
        
        Returns:
            List[T]: A list of all the retrieved data objects.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, id: Any, updated_data: T) -> None:
        """
        Update data with the given id using the provided updated data.
        
        Args:
            id (Any): The id of the data to be updated.
            updated_data (T): The new data to update the existing data with.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: Any) -> None:
        """
        Delete data with the given id.
        
        Args:
            id (Any): The id of the data to be deleted.
        """
        raise NotImplementedError

    @staticmethod
    def _id2str(data: dict) -> dict:
        """
        Convert the _id field of the given data from ObjectId to str.
        
        Args:
            data (dict): The data object containing the _id field.
        
        Returns:
            dict: The updated data object with _id converted to a string and renamed to "id".
            
        Raises:
            Exception: If the data object does not have an _id field.
        """
        if "_id" in data:
            data["id"] = str(data.pop("_id"))
            return data
        raise Exception(f"Data {data} does not have an _id field")
