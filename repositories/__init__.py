"""
repositories.__init__.py

This module initializes the `repositories` package and provides direct access 
to its core classes and exceptions. These repositories handle interactions 
between the FastAPI application and the underlying database.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Imports:
    - IdNotFoundError: Exception raised when an ID is not found in the database.
    - ChatRepo: Repository for handling database interactions related to chat objects.
    - MultimediaRepo: Repository for handling database interactions related to multimedia objects.
"""

from repositories._base_repo import IdNotFoundError
from repositories._chat_repo import ChatRepo
from repositories._feedback_repo import FeedbackRepo
from repositories._multimedia_repo import MultimediaRepo
from repositories._robot_profile_repo import RobotProfileRepo
from repositories._user_repo import UserRepo
