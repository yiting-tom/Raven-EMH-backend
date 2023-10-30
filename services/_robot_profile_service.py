"""
services/_robot_profile_service.py

This module defines the service layer for robot_profile interactions in the FastAPI application. 
It primarily handles the creation, retrieval, and deletion of robot_profile records, as well 
as their associated multimedia files.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - RobotProfileService: Service class that encapsulates robot_profile interactions and its related operations.
"""


import re
import tempfile
from typing import Dict, List, Optional

import numpy as np
from loguru import logger

from models import (
    Filter,
    RobotProfileCreateRequest,
    RobotProfileInCache,
    RobotProfileInDB,
    RobotProfileInDBCreate,
)
from repositories import RobotProfileRepo
from utils import converter


class RobotProfileService:
    """
    Service class that encapsulates robot_profile interactions and its related operations.

    Attributes:
        repo (RobotProfileRepo): Repository for robot_profile records.
    """

    def __init__(self, repository: RobotProfileRepo):
        self.repo = repository
        self.robot_profiles_cache = {}
        # TODO: Implement caching of robot_profiles

    def create_robot_profile(
        self, robot_profile_request: RobotProfileCreateRequest
    ) -> str:
        """create_robot_profile

        Args:
            robot_profile_request (RobotProfileCreateRequest): The request object for creating a robot_profile.

        Returns:
            str: The id for the created robot_profile.
        """
        request_dict: dict = robot_profile_request.model_dump()
        # Transform the request dict into a RobotProfileInDBCreate object
        for dropped_field in ["voice", "description", "imageURL"]:
            del request_dict[dropped_field]
        robot_profile_create = RobotProfileInDBCreate(**request_dict)

        return self.repo.create_robot_profile(robot_profile_create)

    def get_cached_robot_profile_by_robot_id(
        self, robot_id: str
    ) -> Optional[RobotProfileInCache]:
        return self.robot_profiles_cache.get(robot_id, None)

    def get_robot_profile_by_robot_profile_id(
        self, robot_profile_id: str
    ) -> Optional[RobotProfileInDB]:
        return self.repo.get_robot_profile(robot_profile_id)

    def cache_robot_profile_request(
        self,
        robot_profile_request: RobotProfileCreateRequest,
    ) -> RobotProfileInCache:
        robot_profile_dict = robot_profile_request.model_dump()

        # Transform the request dict into a RobotProfileInCache object
        # Drop unused fileds
        for dropped_field in ["name", "description"]:
            del robot_profile_dict[dropped_field]

        cached_robot_profile = RobotProfileInCache(
            **robot_profile_dict,
        )
        self.robot_profiles_cache[robot_profile_request.robot_id] = cached_robot_profile
        return cached_robot_profile
