# robot_profile_routes.py

from typing import Optional

from fastapi import APIRouter, HTTPException

from database.mongodb import MongoDB
from models import RobotProfileInDB
from repositories import RobotProfileRepo
from services import RobotProfileService

router = APIRouter()

db = MongoDB()
robot_profile_repo = RobotProfileRepo(
    db.get_database,
    db.get_collection("robot_profiles"),
)
robot_profile_service = RobotProfileService(robot_profile_repo)


@router.get("/{robot_profile_id}", response_model=RobotProfileInDB)
async def get_robot_profile(
    robot_profile_id: str,
) -> Optional[RobotProfileInDB]:
    """
    Update a robot_profile by its ID.
    """
    return robot_profile_service.get_robot_profile_by_robot_profile_id(robot_profile_id)
