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

from pathlib import Path
from typing import Any, Dict, List, Optional

from bson import ObjectId
from gridfs import GridFS
from loguru import logger

from external.chat.openai_api import MedicalChatBot
from external.tts._base_tts import BaseTTS
from models import (
    ChatCreate,
    ChatCreateInput,
    ChatUpdate,
    ChatInDB,
    ChatInDBOutput,
    Status,
    FeedbackCreate,
)
from services._feedback_service import FeedbackService
from repositories import ChatRepo, IdNotFoundError
from configs import paths as paths
from utils import converter
from Wav2Lip.wav2lip import Wav2LipAAG


class ChatService:
    """
    Service class that encapsulates chat interactions and its related operations.

    Attributes:
        repo (ChatRepo): Repository for chat records.
        chatbot (MedicalChatBot): Chatbot service for generating responses.
        tts (BaseTTS): Text-to-speech service.
        aag (Wav2LipAAG): Avatar generation service.
        grid_fs (GridFS): File storage service for storing multimedia files.
    """

    def __init__(
        self,
        repository: ChatRepo,
        tts: BaseTTS,
        chatbot: MedicalChatBot,
        aag: Wav2LipAAG,
        grid_fs: GridFS,
        feedback_service: FeedbackService,
    ):
        self.repo = repository
        self.chatbot = chatbot
        self.tts = tts
        self.aag = aag
        self.grid_fs = grid_fs
        self.feedback_service = feedback_service

    def create_chat(
        self, data: ChatCreateInput, username: str = "Mr. TestUser"
    ) -> ChatInDBOutput:
        """
        Creates a new chat record based on the input data.

        Args:
            data (ChatCreateInput): The input data for creating a chat.

        Returns:
            ChatInDBOutput: The created chat record.
        """
        context: List[str] = []

        def rec_get_context(parent_id: str) -> None:
            """
            Helper function to recursively get context from parent chats.

            Args:
                parent_id (str): The ID of the parent chat.
            """
            if parent_id is None or parent_id == "":
                return
            parent_in_db: ChatInDB = self.repo.find_by_id(parent_id)
            context.insert(0, parent_in_db.response)
            context.insert(0, parent_in_db.request)
            rec_get_context(parent_in_db.parent_id)

        rec_get_context(data.parent_id)
        context.append(data.request)
        logger.info(f"Context length: {len(context)//2}")
        # Generate response by chatbot
        response: str = self.chatbot.chat(
            user_assistants=context,
        )
        logger.debug(f"Response from {self.chatbot}: {response}")

        # Generate audio by text-to-speech(TTS)
        audio_data: bytes = self.tts.text_to_speech(response)
        audio_fname: Path = paths.DATA / "temp.mp3"
        audio_fname.write_bytes(audio_data)

        # Generate video by animated-avatar-generation(AAG)
        video_fname: str = self.aag.generate_avatar(audio_fname)
        video_data: bytes = converter.file2bytes(video_fname)

        # Store audio and video in GridFS
        audio_id: ObjectId = self.grid_fs.put(audio_data, content_type="audio/mp3")
        video_id: ObjectId = self.grid_fs.put(video_data, content_type="video/mp4")

        # Create new feedback
        new_feedback = FeedbackCreate(
            user_id=data.user_id,
            username=username,
            chat_id=data.parent_id,
            request=data.request,
            response=response,
            parent_id=data.parent_id,
            annotations=[],
        )
        self.feedback_service.create_feedback(new_feedback)

        chat_in_db: ChatInDB = self.repo.create(
            ChatCreate(
                user_id=data.user_id,
                request=data.request,
                parent_id=data.parent_id,
                response=response,
                audio_id=str(audio_id),
                video_id=str(video_id),
                status=Status.ACTIVATING,
                children_ids=[],
            )
        )
        # Update parent's children_ids if parent_id is not None
        if data.parent_id is not None and data.parent_id != "":
            # Get parent chat record
            parent_in_db: ChatInDB = self.repo.find_by_id(data.parent_id)
            # Create new children_ids list with the new chat record's ID appended
            new_children_ids: List[str] = parent_in_db.children_ids + [chat_in_db.id]
            # Update parent chat record
            self.update_chat(data.parent_id, ChatUpdate(children_ids=new_children_ids))

        return self.__convert_indb_to_indboutput(chat_in_db)

    def get_chat_by_id(self, id: str) -> Optional[ChatInDBOutput]:
        """
        Retrieves a chat record by its ID.

        Args:
            id (str): The ID of the chat record to retrieve.

        Returns:
            Optional[ChatInDBOutput]: The retrieved chat record or None if not found.
        """
        chat_in_db: ChatInDB = self.repo.find_by_id(id)
        return self.__convert_indb_to_indboutput(chat_in_db)

    def get_all_chats(self) -> List[ChatInDB]:
        """
        Retrieves all chat records.

        Returns:
            List[ChatInDB]: A list of all chat records.
        """
        return [
            self.__convert_indb_to_indboutput(chat_in_db)
            for chat_in_db in self.repo.find_all()
        ]

    def update_chat(self, id: str, data: ChatUpdate) -> ChatInDBOutput:
        """
        Updates a chat record by its ID.

        Args:
            id (str): The ID of the chat record to update.
            data (ChatUpdate): The data to update the chat record with.

        Returns:
            ChatInDBOutput: The updated chat record.
        """
        chat_in_db: ChatInDB = self.repo.update(id, data)
        return self.__convert_indb_to_indboutput(chat_in_db)

    def archive_chat(self, id: str) -> None:
        """
        Archives a chat record by its ID.

        Args:
            id (str): The ID of the chat record to archive.
        """
        chat_in_db: ChatInDB = self.repo.find_by_id(id)
        chat_in_db.status = Status.ARCHIVED
        self.repo.update(id, ChatUpdate(status=Status.ARCHIVED))
        # Recursively archive all children chats
        for child_id in chat_in_db.children_ids:
            self.archive_chat(child_id)

    def delete_chat(self, id: str) -> None:
        """
        Deletes a chat record by its ID.

        Args:
            id (str): The ID of the chat record to delete.
        """
        return self.repo.delete(id)

    def __convert_indb_to_indboutput(
        self,
        chat_in_db: ChatInDB,
    ) -> ChatInDBOutput:
        """
        Helper function to convert ChatInDB object to ChatInDBOutput.

        Args:
            chat_in_db (ChatInDB): The chat record in database format.

        Returns:
            ChatInDBOutput: The chat record in output format.
        """
        chat_dict: Dict[str, Any] = chat_in_db.model_dump()
        chat_dict["audio"] = converter.bytes2base64(
            self.grid_fs.get(ObjectId(chat_dict.pop("audio_id"))).read()
        )
        chat_dict["video"] = converter.bytes2base64(
            self.grid_fs.get(ObjectId(chat_dict.pop("video_id"))).read()
        )
        return ChatInDBOutput(**chat_dict)

    def get_chat_by_user_id(self, user_id: str) -> List[ChatInDBOutput]:
        """
        Retrieves all chat records by user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            List[ChatInDBOutput]: A list of all chat records by user ID.
        """
        return [
            self.__convert_indb_to_indboutput(chat_in_db)
            for chat_in_db in self.repo.find_by_user_id(user_id)
        ]
