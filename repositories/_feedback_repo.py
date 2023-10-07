# _feedback_repo.py

from typing import Any, List, Optional

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from models import FeedbackCreate, FeedbackInDB
from repositories._base_repo import IdNotFoundError
from utils.logger import logger


class FeedbackRepo:
    """
    Repository for Feedback operations.
    """

    def __init__(self, db: Database, collection: Collection) -> None:
        self.db = db
        self.collection = collection

    def create(self, feedback: FeedbackCreate) -> Any:
        """
        Save the given feedback data.

        Args:
            feedback (FeedbackCreate): The feedback to be saved.

        Returns:
            FeedbackInDB: The saved feedback object.
        """
        try:
            result = self.collection.insert_one(feedback.model_dump())
            logger.debug(f"Created feedback with ID {result.inserted_id}")
            return self.find_by_id(result.inserted_id)
        except DuplicateKeyError:
            logger.error(f"Duplicate key error for feedback: {feedback.model_dump()}")
            raise

    @staticmethod
    def object_id_to_str(obj):
        obj["id"] = str(obj["_id"])
        del obj["_id"]
        return obj

    def find_by_id(self, feedback_id: str) -> Optional[FeedbackInDB]:
        """
        Retrieve feedback by its id.

        Args:
            feedback_id (str): The id of the feedback to be retrieved.

        Returns:
            FeedbackInDB: The retrieved feedback object, or None if not found.
        """
        feedback = self.collection.find_one({"_id": ObjectId(feedback_id)})
        if not feedback:
            raise IdNotFoundError(f"Feedback with ID {feedback_id} not found.")
        logger.info(f"Found feedback with ID {feedback_id}")
        return FeedbackInDB(**self.object_id_to_str(feedback))

    def find_by_user_id(self, user_id: str) -> List[FeedbackInDB]:
        """
        Retrieve all feedbacks by user id.

        Returns:
            List[FeedbackInDB]: A list of all the retrieved feedback objects.
        """
        feedbacks = self.collection.find({"user_id": user_id})
        result = [
            FeedbackInDB(**self.object_id_to_str(feedback)) for feedback in feedbacks
        ]
        logger.info(f"Found {len(result)} feedbacks by user ID {user_id}")
        return result

    def find_by_user_id_and_robot_id(
        self, user_id: str, robot_id: str
    ) -> List[FeedbackInDB]:
        """
        Retrieve all feedbacks by user id and robot id.

        Returns:
            List[FeedbackInDB]: A list of all the retrieved feedback objects.
        """
        feedbacks = self.collection.find({"user_id": user_id, "robot_id": robot_id})
        result = [
            FeedbackInDB(**self.object_id_to_str(feedback)) for feedback in feedbacks
        ]
        logger.info(
            f"Found {len(result)} feedbacks by user ID {user_id} and robot ID {robot_id}"
        )
        return result

    def update(self, feedback_id: str, updated_data: FeedbackCreate) -> None:
        """
        Update feedback with the given id using the provided updated data.

        Args:
            feedback_id (str): The id of the feedback to be updated.
            updated_data (FeedbackCreate): The new data to update the existing feedback with.
        """
        self.collection.update_one(
            {"_id": ObjectId(feedback_id)}, {"$set": updated_data.model_dump()}
        )
        logger.info(f"Updated feedback with ID {feedback_id}")

    def delete(self, feedback_id: str) -> None:
        """
        Delete feedback with the given id.

        Args:
            feedback_id (str): The id of the feedback to be deleted.
        """
        result = self.collection.delete_one({"_id": ObjectId(feedback_id)})
        logger.info(f"Deleted feedback with ID {feedback_id}")
