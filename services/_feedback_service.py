# _feedback_service.py

from typing import List, Optional

from pymongo.database import Database

from models import FeedbackCreate, FeedbackInDB, FeedbackUpdate
from repositories import FeedbackRepo, IdNotFoundError
from utils.logger import logger


class FeedbackService:
    """
    Service for Feedback operations.
    """

    def __init__(self, repository: FeedbackRepo):
        self.repo = repository

    def create_feedback(self, feedback: FeedbackCreate) -> FeedbackInDB:
        """
        Create a new feedback.

        Args:
            feedback (FeedbackCreate): The feedback data to be created.

        Returns:
            FeedbackInDB: The created feedback object.
        """
        return self.repo.create(feedback)

    def get_feedback_by_id(self, feedback_id: str) -> Optional[FeedbackInDB]:
        """
        Retrieve feedback by its id.

        Args:
            feedback_id (str): The id of the feedback to be retrieved.

        Returns:
            Optional[FeedbackInDB]: The retrieved feedback object, or None if not found.
        """
        try:
            return self.repo.find_by_id(feedback_id)
        except IdNotFoundError:
            logger.warning(f"Feedback with ID {feedback_id} not found.")
            return None

    def get_all_feedbacks(self) -> List[FeedbackInDB]:
        """
        Retrieve all feedback.

        Returns:
            List[FeedbackInDB]: A list of all the retrieved feedback objects.
        """
        return self.repo.find_all()

    def get_feedback_by_user_id(self, user_id: str) -> List[FeedbackInDB]:
        """
        Retrieve feedback by its user id.

        Args:
            user_id (str): The id of the user whose feedback is to be retrieved.

        Returns:
            List[FeedbackInDB]: A list of all the retrieved feedback objects.
        """
        return self.repo.find_by_user_id(user_id)

    def update_feedback(self, feedback_id: str, updated_data: FeedbackUpdate) -> bool:
        """
        Update feedback with the given id using the provided updated data.

        Args:
            feedback_id (str): The id of the feedback to be updated.
            updated_data (FeedbackUpdate): The new data to update the existing feedback with.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            self.repo.update(feedback_id, updated_data)
            return True
        except IdNotFoundError:
            logger.warning(f"Feedback with ID {feedback_id} not found.")
            return False

    def delete_feedback(self, feedback_id: str) -> bool:
        """
        Delete feedback with the given id.

        Args:
            feedback_id (str): The id of the feedback to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            self.repo.delete(feedback_id)
            return True
        except IdNotFoundError:
            logger.warning(f"Feedback with ID {feedback_id} not found.")
            return False
