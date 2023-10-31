"""
services/_chat_service.py

This module defines the service layer for chat interactions in the FastAPI application. 
It primarily handles the creation, retrieval, and deletion of chat records, as well 
as their associated multimedia files.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - ChatService: Service class that encapsulates chat interactions and its related operations.
"""


import re
import os
import requests
from typing import List, Optional
from time import time

from loguru import logger

from configs import paths as paths
from external.chat.openai_api import ChatBot
from external.tts._base_tts import BaseTTS
from models import (
    ChatCreateResponse,
    ChatData,
    ChatInDB,
    ChatInDBCreate,
    Filter,
    RobotProfileInCache,
)
from repositories import ChatRepo
from utils import converter


class ChatService:
    """
    Service class that encapsulates chat interactions and its related operations.

    Attributes:
        repo (ChatRepo): Repository for chat records.
        chatbot (MedicalChatBot): Chatbot service for generating responses.
        tts (BaseTTS): Text-to-speech service.
        grid_fs (GridFS): File storage service for storing multimedia files.
    """

    def __init__(
        self,
        repository: ChatRepo,
        tts: BaseTTS,
        chatbot: ChatBot,
    ):
        self.repo = repository
        self.chatbot = chatbot
        self.tts = tts

    async def create_chat(
        self,
        chat_data: ChatData,
        robot_profile: RobotProfileInCache,
        robot_profile_id: str,
    ) -> ChatCreateResponse:
        """
        Create a new chat object and save it to the database.

        Args:
            chat (ChatCreate): The chat object to be created.

        Returns:
            The created chat object, with additional information like its unique ID.
        """
        logger.info(f"Creating chat: {chat_data}")
        raw_response: str = ""
        audio_base64: Optional[str] = None
        video_base64: Optional[str] = None
        workflow: List[str] = []

        workflow.append("Dialog: " + "\n".join(chat_data.history))
        workflow.append("User Request: " + chat_data.message)
        if "HISTORY" in robot_profile.options:
            workflow.append(f"Applied History: ")
            ...

        if "MEDICAL KNOWLEDGE" in robot_profile.options:
            workflow.append(f"Applied Medical Knowledge: ")
            ...

        # Generate raw response
        time_start = time()
        raw_response = self.chatbot.chat(
            system_msg=robot_profile.prompt,
            user_assistants=chat_data.history + [chat_data.message],
            model=robot_profile.model,
        )
        workflow.append(f"Raw Response({time() - time_start:0.2f}): {raw_response}")

        # Filters
        if len(robot_profile.filters) > 0:
            logger.info("Applying filters", robot_profile.filters)

            def filter_func(message: str, filter: Filter):
                if filter.isRegex:
                    result = re.search(filter.prompt, message)
                    if result:
                        return result.group(0)
                    return message
                filtered_message = self.chatbot.chat(
                    system_msg=filter.prompt,
                    user_assistants=[message],
                    model=filter.model or "gpt-3.5-turbo",
                )
                return filtered_message

            for i, filter in enumerate(robot_profile.filters, 1):
                logger.info("Applying filter", filter.name)
                time_start = time()
                raw_response = filter_func(raw_response, filter)
                workflow.append(
                    f"Applied Filter-{i} '{filter.name}'({time() - time_start:0.2f}): {raw_response}"
                )

        # Audio
        if "VOICE" in robot_profile.options:
            logger.info("Generating audio")
            time_start = time()
            audio_bytes: bytes = await self.tts.text_to_speech(
                text=raw_response,
                voice_id=robot_profile.voice,
            )
            audio_base64: str = converter.bytes2base64(audio_bytes)
            workflow.append(f"Applied Voice Generation({time()-time_start:0.2f})")

            # Video
            if "VIDEO" in robot_profile.options:
                logger.info("Generating video")

                time_start = time()
                resp = requests.post(
                    os.getenv("APP_AAG_SERVICE_URL"),
                    json={
                        "audio_base64": audio_base64,
                        "image_url": robot_profile.imageURL,
                    },
                )
                resp = resp.json()
                video_base64 = resp["video_base64"]
                workflow.append(f"Applied Video Generation({time()-time_start:0.2f})")

        # Save to database
        chat_in_db_create = ChatInDBCreate(
            user_id=chat_data.user_id,
            robot_id=robot_profile.robot_id,
            robot_profile_id=robot_profile_id,
            parent_id=chat_data.parent_id,
            children_ids=[],
            request=chat_data.message,
            response=raw_response,
        )

        chat_id: str = self.repo.create_chat(chat_in_db_create)

        chat_in_db_resopnse = ChatCreateResponse(
            id=chat_id,
            request=chat_data.message,
            response=raw_response,
            audio_base64=audio_base64,
            video_base64=video_base64,
        )

        return chat_in_db_resopnse, workflow

    async def get_chats_by_user_id_and_robot_id(
        self, user_id: str, robot_id: str, order_by: Optional[str] = "created_at"
    ) -> List[ChatInDB]:
        """
        Retrieve all chat objects.

        Returns:
            A list of all chat objects.
        """
        return self.repo.get_chats_by_user_id_and_robot_id(
            user_id, robot_id, order_by=order_by
        )
