"""
services/_multimedia_service.py

This module contains the MultimediaService class, which is responsible for implementing
the business logic related to multimedia files. The class interacts with the MultimediaRepo
for data access, which isolates the service layer from the direct data manipulation logic.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - MultimediaService: A service class for managing multimedia files.
"""

from typing import Any, Dict, List, Optional

from loguru import logger

from models import MultimediaCreate, MultimediaInDB, MultimediaInDBOutput
from repositories import IdNotFoundError, MultimediaRepo
from utils import converter


class MultimediaService:
    """
    A service class for managing multimedia files.

    This class is responsible for implementing the business logic
    related to multimedia files and interacts with the MultimediaRepo for data access.
    """

    def __init__(self, repository: MultimediaRepo):
        """
        Initializes the MultimediaService instance with a given repository.

        Args:
            repository (MultimediaRepo): The repository instance for data access.
        """
        self.repo = repository

    def create_multimedia(self, data: MultimediaCreate) -> MultimediaInDBOutput:
        """
        Upload a multimedia multimedia and save its metadata.

        Args:
            data (MultimediaCreate): The multimedia multimedia data and metadata.

        Returns:
            MultimediaInDB: The created multimedia multimedia's metadata with its PyObjectId.
        """
        multimedia_in_db: MultimediaInDB = self.repo.create(data)
        logger.info(f"Multimedia created: {multimedia_in_db.keys()}")
        return self.__convert_indb_to_indboutput(multimedia_in_db)

    def get_multimedia_by_id(self, id: str) -> Optional[MultimediaInDBOutput]:
        """
        Retrieve a multimedia multimedia's metadata by its PyObjectId.

        Args:
            id (PyObjectId): The PyObjectId of the multimedia multimedia.

        Returns:
            Optional[MultimediaInDB]: The metadata of the multimedia, or None if not found.
        """
        try:
            multimedia_in_db: MultimediaInDB = self.repo.find_by_id(id)
        except IdNotFoundError:
            return None
        return self.__convert_indb_to_indboutput(multimedia_in_db)

    def get_all_multimedias(self) -> List[MultimediaInDB]:
        """
        Retrieve all multimedia files' metadata.

        Returns:
            List[MultimediaInDB]: The list of metadata for all multimedias.
        """
        multimedias_in_db: List[MultimediaInDB] = self.repo.find_all()

        return [
            self.__convert_indb_to_indboutput(multimedia_in_db)
            for multimedia_in_db in multimedias_in_db
        ]

    def delete_multimedia(self, id: str) -> None:
        """
        Delete a multimedia multimedia and its metadata from the collection.

        Args:
            id (PyObjectId): The PyObjectId of the multimedia multimedia to delete.
        """
        self.repo.delete(id)

    @staticmethod
    def __convert_indb_to_indboutput(
        multimedia_in_db: MultimediaInDB,
    ) -> MultimediaInDBOutput:
        ...
        # Prepare the dictionary representation of the MultimediaInDB instance
        multimedia_dict: Dict[str, Any] = multimedia_in_db.model_dump()

        # Convert the "_id" field to "id"
        multimedia_dict["id"] = str(multimedia_dict["_id"])

        # Convert the binary file data to a base64 encoded string
        multimedia_dict["file_data"] = converter.bytes2base64(
            multimedia_dict["file_data"]
        )

        # Create and return a MultimediaInDBOutput instance from the prepared dictionary
        return MultimediaInDBOutput(**multimedia_dict)
