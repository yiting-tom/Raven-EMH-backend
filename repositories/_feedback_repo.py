# _feedback_repo.py

from typing import Any, List, Optional

from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from models import FeedbackCreate, FeedbackInDB
from repositories._base_repo import BaseRepo, IdNotFoundError

from bson import ObjectId
from utils.logger import logger


class FeedbackRepo(BaseRepo[FeedbackInDB]):
    """
    Repository for Feedback operations.
    """

    COLLECTION_NAME = "feedbacks"  # Name of the MongoDB collection

    def __init__(self, db: Database, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

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

    def find_by_id(self, feedback_id: Any) -> Optional[FeedbackInDB]:
        """
        Retrieve feedback by its id.

        Args:
            feedback_id (Any): The id of the feedback to be retrieved.

        Returns:
            FeedbackInDB: The retrieved feedback object, or None if not found.
        """
        feedback = self.collection.find_one({"_id": ObjectId(feedback_id)})
        if not feedback:
            raise IdNotFoundError(f"Feedback with ID {feedback_id} not found.")
        logger.info(f"Found feedback with ID {feedback_id}")
        return FeedbackInDB(**self._id2str(feedback))

    def find_all(self) -> List[FeedbackInDB]:
        """
        Retrieve all feedback.

        Returns:
            List[FeedbackInDB]: A list of all the retrieved feedback objects.
        """
        feedbacks = self.collection.find()
        result = [FeedbackInDB(**self._id2str(feedback)) for feedback in feedbacks]
        logger.info(f"Found {len(result)} feedbacks")
        return result

    def find_by_user_id(self, user_id: str) -> List[FeedbackInDB]:
        """
        Retrieve all feedbacks by user id.

        Returns:
            List[FeedbackInDB]: A list of all the retrieved feedback objects.
        """
        feedbacks = self.collection.find({"user_id": user_id})
        result = [FeedbackInDB(**self._id2str(feedback)) for feedback in feedbacks]
        logger.info(f"Found {len(result)} feedbacks by user ID {user_id}")
        return result

    def update(self, feedback_id: Any, updated_data: FeedbackCreate) -> None:
        """
        Update feedback with the given id using the provided updated data.

        Args:
            feedback_id (Any): The id of the feedback to be updated.
            updated_data (FeedbackCreate): The new data to update the existing feedback with.
        """
        result = self.collection.update_one(
            {"_id": ObjectId(feedback_id)}, {"$set": updated_data.dict()}
        )
        if result.matched_count == 0:
            raise IdNotFoundError(f"Feedback with ID {feedback_id} not found.")
        logger.info(f"Updated feedback with ID {feedback_id}")

    def delete(self, feedback_id: Any) -> None:
        """
        Delete feedback with the given id.

        Args:
            feedback_id (Any): The id of the feedback to be deleted.
        """
        result = self.collection.delete_one({"_id": ObjectId(feedback_id)})
        if result.deleted_count == 0:
            raise IdNotFoundError(f"Feedback with ID {feedback_id} not found.")
        logger.info(f"Deleted feedback with ID {feedback_id}")
