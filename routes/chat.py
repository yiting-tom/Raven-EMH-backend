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

from typing import Dict, List

from fastapi import APIRouter, HTTPException

from database.mongodb import MongoDB
from external.chat.openai_api import MedicalChatBot
from external.tts.aws_polly_api import PollyTTS
from models import ChatCreateInput, ChatInDBOutput, ChatUpdate
from repositories import ChatRepo, FeedbackRepo
from services import ChatService, FeedbackService
from Wav2Lip.wav2lip import Wav2LipAAG

router = APIRouter()

# Initialize necessary components
mongo_db = MongoDB()
chatbot = MedicalChatBot()
tts = PollyTTS()
aag = Wav2LipAAG()

# Set up the chat repository
chat_repo = ChatRepo(
    mongo_db.get_database,
    mongo_db.get_collection(ChatRepo.COLLECTION_NAME),
)

feedback_repo = FeedbackRepo(
    mongo_db.get_database,
    mongo_db.get_collection(FeedbackRepo.COLLECTION_NAME),
)
feedback_service = FeedbackService(feedback_repo)

# Initialize the chat service with all its dependencies
chat_service = ChatService(
    chatbot=chatbot,
    tts=tts,
    repository=chat_repo,
    aag=aag,
    grid_fs=mongo_db.get_gridfs,
    feedback_service=feedback_service,
)


@router.post("/", response_model=ChatInDBOutput)
async def create_chat(user_id: str, chat: ChatCreateInput, format_dict: Dict[str, str]):
    """
    Create a new chat object and save it to the database.

    Args:
        user_id (str): The unique ID of the user initiating the chat.
        chat (ChatCreate): The chat object to be created.

    Returns:
        The created chat object, with additional information like its unique ID.
    """
    return chat_service.create_chat(user_id, chat, format_dict)


# @router.post("/", response_model=ChatInDBOutput)
# async def create_chat(chat: ChatCreateInput):
#     import time

#     time.sleep(1)
#     return chat_service.get_chat_by_id("64ef3987ee8fd5026096311d")


@router.get("/{chat_id}")
async def get_chat_by_id(chat_id: str):
    """
    Retrieve a specific chat object by its unique ID.

    Args:
        chat_id (str): The unique ID of the chat object to retrieve.

    Returns:
        The chat object with the specified ID.
    """
    return chat_service.get_chat_by_id(chat_id)


@router.get("/", response_model=List[ChatInDBOutput])
async def get_all_chats():
    """
    Retrieve all chat objects stored in the database.

    Returns:
        A list of all chat objects.
    """
    return chat_service.get_all_chats()


@router.put("/{chat_id}", response_model=ChatInDBOutput)
async def update_chat(chat_id: str, chat: ChatUpdate):
    """
    Update a specific chat object by its unique ID.

    Args:
        chat_id (str): The unique ID of the chat object to update.
        chat (ChatUpdate): The data to update the chat object with.

    Returns:
        The updated chat object.
    """
    return chat_service.update_chat(chat_id, chat)


@router.delete("/{chat_id}")
async def delete_chat(chat_id: str):
    """
    Delete a specific chat object by its unique ID.

    Args:
        chat_id (str): The unique ID of the chat object to delete.

    Returns:
        A message confirming the deletion of the chat object.
    """
    chat_service.delete_chat(chat_id)
    return {"message": f"Chat {chat_id} deleted"}


@router.get("/user/{user_id}")
async def get_chat_by_user_id(user_id: str):
    """
    Retrieve a specific chat object by its unique ID.

    Args:
        chat_id (str): The unique ID of the chat object to retrieve.

    Returns:
        The chat object with the specified ID.
    """
    return chat_service.get_chat_by_user_id(user_id)


@router.put("/{chat_id}")
async def archive_chat(chat_id: str):
    """
    Archive a specific chat object by its unique ID.

    Args:
        chat_id (str): The unique ID of the chat object to archive.

    Returns:
        The archived chat object.
    """
    return chat_service.archive_chat(chat_id)
