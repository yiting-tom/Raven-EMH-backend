# feedback_routes.py

from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException
from database.mongodb import MongoDB

from models import FeedbackCreate, FeedbackInDB, FeedbackUpdate
from services import FeedbackService
from repositories import FeedbackRepo

router = APIRouter()

db = MongoDB()
feedback_repo = FeedbackRepo(
    db.get_database,
    db.get_collection(FeedbackRepo.COLLECTION_NAME),
)
feedback_service = FeedbackService(feedback_repo)


@router.post("/", response_model=FeedbackInDB)
async def create_feedback(feedback: FeedbackCreate) -> FeedbackInDB:
    """
    Create a new feedback.
    """
    return feedback_service.create_feedback(feedback)


# @router.get("/{feedback_id}", response_model=FeedbackInDB)
# async def get_feedback_by_id(feedback_id: str) -> FeedbackInDB:
#     """
#     Get feedback details by its ID.
#     """
#     feedback = feedback_service.get_feedback_by_id(feedback_id)
#     if not feedback:
#         raise HTTPException(status_code=404, detail="Feedback not found")
#     return feedback


@router.get("/user/{user_id}", response_model=List[FeedbackInDB])
async def get_feedback_by_user_id(user_id: str) -> List[FeedbackInDB]:
    """
    Get feedback details by its user ID.
    """
    feedbacks = feedback_service.get_feedback_by_user_id(user_id)
    if not feedbacks:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return feedbacks


@router.get("/", response_model=List[FeedbackInDB])
async def get_all_feedbacks() -> List[FeedbackInDB]:
    """
    Get all feedback entries.
    """
    return feedback_service.get_all_feedbacks()


@router.put("/{feedback_id}", response_model=bool)
async def update_feedback(feedback_id: str, feedback_update: FeedbackUpdate) -> bool:
    """
    Update a feedback by its ID.
    """
    if not feedback_service.update_feedback(feedback_id, feedback_update):
        raise HTTPException(
            status_code=404, detail="Feedback not found or update failed"
        )
    return True


@router.delete("/{feedback_id}", response_model=bool)
async def delete_feedback(feedback_id: str) -> bool:
    """
    Delete a feedback by its ID.
    """
    if not feedback_service.delete_feedback(feedback_id):
        raise HTTPException(
            status_code=404, detail="Feedback not found or delete failed"
        )
    return True
