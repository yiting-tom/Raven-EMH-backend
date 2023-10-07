# feedback_routes.py

from typing import List

from fastapi import APIRouter, HTTPException

from database.mongodb import MongoDB
from models import FeedbackInDB, FeedbackUpdateRequest, FeedbackInDBResponse
from repositories import FeedbackRepo, RobotProfileRepo
from services import FeedbackService, RobotProfileService

router = APIRouter()

db = MongoDB()
feedback_repo = FeedbackRepo(
    db.get_database,
    db.get_collection("feedbacks"),
)
feedback_service = FeedbackService(feedback_repo)

robot_profile_repo = RobotProfileRepo(
    db.get_database,
    db.get_collection("robot_profiles"),
)
robot_profile_service = RobotProfileService(robot_profile_repo)


@router.get(
    "/user_id/{user_id}/robot_id/{robot_id}", response_model=List[FeedbackInDBResponse]
)
async def get_feedback_by_user_id_and_robot_id(
    user_id: str, robot_id: str
) -> List[FeedbackInDB]:
    """
    Get feedback details by its user ID.
    """
    feedbacks: List[
        FeedbackInDB
    ] = feedback_service.get_feedback_by_user_id_and_robot_id(user_id, robot_id)
    return [
        FeedbackInDBResponse(
            **feedback.model_dump(),
            robot_profile=robot_profile_service.get_robot_profile_by_robot_profile_id(
                feedback.robot_profile_id
            )
        )
        for feedback in feedbacks
    ]


@router.get("/user_id/{user_id}", response_model=List[FeedbackInDBResponse])
async def get_feedback_by_user_id(user_id: str) -> List[FeedbackInDB]:
    """
    Get feedback details by its user ID.
    """
    feedbacks = feedback_service.get_feedback_by_user_id(user_id)

    return [
        FeedbackInDBResponse(
            **feedback.model_dump(),
            robot_profile=robot_profile_service.get_robot_profile_by_robot_profile_id(
                feedback.robot_profile_id
            )
        )
        for feedback in feedbacks
    ]


@router.put("/{feedback_id}", response_model=bool)
async def update_feedback(
    feedback_id: str, feedback_update: FeedbackUpdateRequest
) -> bool:
    """
    Update a feedback by its ID.
    """
    if not feedback_service.update_feedback(feedback_id, feedback_update):
        raise HTTPException(
            status_code=404, detail="Feedback not found or update failed"
        )
    return True
