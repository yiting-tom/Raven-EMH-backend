"""
models/__init__.py

This module is responsible for making the necessary data models available at the package level.
By importing the models here, they can be easily accessed from the 'models' package in other parts
of the application without needing to know the specific module in which each model is defined.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Imports:
    - MultimediaCreate: Model for validating the data when creating a new multimedia object.
    - MultimediaInDBOutput: Model for representing the response data for a multimedia object.
    - MultimediaInDB: Model for representing a multimedia object stored in the database.
"""

from models._chat import (
    ChatCreateRequest,
    ChatCreateResponse,
    ChatData,
    ChatDeleteRequest,
    ChatGetRequest,
    ChatInDB,
    ChatInDBCreate,
    ChatsGetRequest,
)
from models._feedback import (
    FeedbackCreate,
    FeedbackInDB,
    FeedbackUpdateRequest,
    FeedbackInDBResponse,
)
from models._multimedia import MultimediaCreate, MultimediaInDB, MultimediaInDBOutput
from models._robot_profile import (
    Filter,
    RobotProfileCreateRequest,
    RobotProfileInCache,
    RobotProfileInDB,
    RobotProfileInDBCreate,
)
from models._user import (
    UserDataInFirebaseAuth,
    UserDataInFirestore,
    UserOutput,
    UserRole,
    UserStatus,
)
