"""
routes/chat.py

This module provides routes for chat-related operations in the FastAPI application.
It provides endpoints for creating, retrieving, and deleting chat objects from the database.
Furthermore, it integrates with external services like a medical chatbot and text-to-speech APIs.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Routes:
    - POST "/": Create a new chat object.
    - GET "/{chat_id}": Retrieve a chat object by its unique ID.
    - GET "/": Retrieve all chat objects.
    - DELETE "/{chat_id}": Delete a chat object by its unique ID.
"""


from fastapi import APIRouter
from loguru import logger

from database.mongodb import MongoDB
from external.chat.openai_api import ChatBot
from external.tts.aws_polly_api import PollyTTS
from models import (
    ChatCreateRequest,
    ChatCreateResponse,
    ChatData,
    FeedbackCreate,
    RobotProfileCreateRequest,
    RobotProfileInCache,
)
from repositories import ChatRepo, FeedbackRepo, RobotProfileRepo
from services import ChatService, FeedbackService, RobotProfileService
from Wav2Lip.wav2lip import Wav2LipAAG

router = APIRouter()

# Initialize necessary components
mongo_db = MongoDB()
chatbot = ChatBot()
tts = PollyTTS()
aag = Wav2LipAAG()

# Set up the chat repository
chat_repo = ChatRepo(
    mongo_db.get_database,
    mongo_db.get_collection("chats"),
)

robot_profile_repo = RobotProfileRepo(
    mongo_db.get_database, mongo_db.get_collection("robot_profiles")
)

feedback_repo = FeedbackRepo(
    mongo_db.get_database, mongo_db.get_collection("feedbacks")
)

# Initialize the chat service with all its dependencies
chat_service = ChatService(
    repository=chat_repo,
    chatbot=chatbot,
    tts=tts,
    aag=aag,
)

robot_profile_service = RobotProfileService(
    repository=robot_profile_repo,
)

feedback_service = FeedbackService(
    feedback_repo,
)


@router.post("/", response_model=ChatCreateResponse, status_code=201)
async def create_chat(chat: ChatCreateRequest):
    """
    Create a new chat object and save it to the database.

    Args:
        chat (ChatCreate): The chat object to be created.

    Returns:
        The created chat object, with additional information like its unique ID.
    """
    logger.info(
        f"Creating chat for user {chat.chat_data.user_id} with robot {chat.robot_profile.robot_id}"
    )
    chat_data_request: ChatData = chat.chat_data
    robot_profile_request: RobotProfileCreateRequest = chat.robot_profile

    # TODO: Implement the caching when refactoring.
    # robot_profile_cached = robot_profile_service.get_cached_robot_profile_by_robot_id(
    #     robot_profile_request.robot_id,
    # )
    # if robot_profile_cached is None:
    #     robot_profile_id = robot_profile_service.create_robot_profile(
    #         robot_profile_request
    #     )
    #     robot_profile_cached = robot_profile_service.cache_robot_profile_request(
    #         robot_profile_request,
    #         robot_profile_id,
    #     )

    robot_profile_id = robot_profile_service.create_robot_profile(robot_profile_request)
    robot_profile_cached: RobotProfileInCache = (
        robot_profile_service.cache_robot_profile_request(
            robot_profile_request,
        )
    )

    chat_response: ChatCreateResponse = await chat_service.create_chat(
        chat_data_request,
        robot_profile_cached,
        robot_profile_id,
    )

    feedback = FeedbackCreate(
        user_id=chat_data_request.user_id,
        parent_id=chat_data_request.parent_id,
        username=chat_data_request.username,
        robot_id=robot_profile_request.robot_id,
        request=chat_response.request,
        response=chat_response.response,
        robot_profile_id=robot_profile_id,
    )
    _ = feedback_service.create_feedback(feedback)
    return chat_response


@router.get("/", status_code=200)
async def get_chats_by_user_id_and_robot_id(user_id, robot_id):
    """
    Retrieve all chat objects.

    Returns:
        A list of all chat objects.
    """
    logger.info(f"Getting all chats for user {user_id} and robot {robot_id}")
    return await chat_service.get_chats_by_user_id_and_robot_id(
        user_id,
        robot_id,
    )
