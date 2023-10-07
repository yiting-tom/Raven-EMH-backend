"""
external/tts/openai_api.py

This module defines the MedicalChatBot class which is used to interact with the OpenAI API.
It is designed to facilitate chat interactions in a medical context.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - MedicalChatBot: A class to handle interaction with the OpenAI API, specifically for medical chatbot purposes.
"""

import os
import re
from typing import Dict, List, Optional

import openai
from loguru import logger


class ChatBot:
    """
    A class to handle interaction with the OpenAI API for chatbot purposes.

    Attributes:
        api_key (Optional[str]): The OpenAI API key.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
    ):
        """
        Initialize the MedicalChatBot.

        Args:
            api_key (Optional[str]): The OpenAI API key. Defaults to None.

        Raises:
            Exception: If the API key is not set.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._validate_api_key()

    def __repr__(self):
        """The string representation of the MedicalChatBot."""
        return f"{self.__class__.__name__}(model={self.model})"

    def _validate_api_key(self):
        """
        Validate the API key. Raise an exception if it's not set.
        """
        if self.api_key is None:
            logger.exception("The OpenAI API key must be set.")
        openai.api_key = self.api_key
        logger.info("Loaded OpenAI API key")

    def chat(
        self,
        system_msg: str,
        user_assistants: List[str],
        model: str = "gpt-3.5-turbo",
        **kwargs,
    ) -> str:
        """
        Chat with the OpenAI API.

        Args:
            system_msg: str
            user_assistants (List[str]): A list of strings that alternate between user and assistant messages.

        Returns:
            str: The response from the assistant.
        """
        assert isinstance(system_msg, str), "`system_msg` should be a string"
        assert isinstance(user_assistants, list), "`user_assistants` should be a list"

        system_msg = [{"role": "system", "content": system_msg}]
        user_assistant_msgs = [
            {"role": "assistant" if i % 2 else "user", "content": message}
            for i, message in enumerate(user_assistants)
        ]

        msgs = system_msg + user_assistant_msgs

        logger.info(f"Sending {len(msgs)} messages to OpenAI model '{model}")

        try:
            response = openai.ChatCompletion.create(
                messages=msgs,
                model=model,
                **kwargs,
            )
        except Exception as e:
            logger.error(f"Failed to call OpenAI API: {e}")
            raise

        if not response.get("choices"):
            logger.error("No choices in the response from OpenAI API")
            raise Exception("No choices in the response from OpenAI API")

        logger.info("Received response from OpenAI API")

        return response["choices"][0]["message"]["content"]
