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
from typing import List, Optional

import openai
from loguru import logger

from configs import paths


class MedicalChatBot:
    """
    A class to handle interaction with the OpenAI API for medical chatbot purposes.

    Attributes:
        api_key (Optional[str]): The OpenAI API key.
        model (str): The name of the model to use.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the MedicalChatBot.

        Args:
            api_key (Optional[str]): The OpenAI API key. Defaults to None.
            model (str): The name of the model to use. Defaults to "gpt-3.5-turbo".
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._validate_api_key()
        self.system_template: str = open(
            paths.PROMPT_DIR / f"{self.__class__.__name__}.txt"
        ).read()
        self.template_slot = re.findall(r"\{([^}]+)\}", self.system_template)
        self.chatsummary = ""

    def __repr__(self):
        """The string representation of the MedicalChatBot."""
        return f"MedicalChatBot(model={self.model})"

    def _validate_api_key(self):
        """
        Validate the API key. Raise an exception if it's not set.
        """
        if self.api_key is None:
            logger.error("The OpenAI API key must be set.")
            raise EnvironmentError("OpenAI API key not set.")
        openai.api_key = self.api_key
        logger.info("Loaded OpenAI API key")

    def summary_chatgpt(self, user_assistant_msgs, max_tokens: int = 64):
        
        previous_summary = self.chatsummary
        conversation_content = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in user_assistant_msgs])

        msgs = [
            {"role": "system", "content": "You will summarize the conversation between user and you, and outcomes only one sentence in 50 words or less."},
            {"role": "user", "content": f"This is the previous summary: {previous_summary}\nPlease combine the conversation below with the previous summary:\n{conversation_content}"}
        ]

        logger.info(f"Sending {len(msgs)} messages to OpenAI API")

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=msgs,
                max_tokens=max_tokens,
            )
        except Exception as e:
            logger.error(f"Failed to call OpenAI API: {e}")
            raise

        if not response.get("choices"):
            logger.error("No choices in the response from OpenAI API")
            raise Exception("No choices in the response from OpenAI API")

        status_code = response["choices"][0]["finish_reason"]
        assert status_code == "stop", f"The status code was {status_code}."

        logger.info("Received response from OpenAI API")

        return response["choices"][0]["message"]["content"]

    def chat(
        self,
        user_assistants: List[str],
        format_dict: Optional[dict] = None,
        max_tokens: int = 64,
    ) -> str:
        """
        Chat with the OpenAI API.

        Args:
            user_assistants (List[str]): A list of strings that alternate between user and assistant messages.

        Returns:
            str: The response from the assistant.
        """

        assert isinstance(user_assistants, list), "`user_assistants` should be a list"
        assert set(self.template_slot) == set(
            format_dict.keys()
        ), f"formating_dict ({format_dict.keys()}) should have the same keys as template_slot ({self.template_slot})"

        system = self.system_template.format(**format_dict)

        if self.chatsummary != "":
            system = system + "Your previous chat history with user is summarized as below:" + self.chatsummary

        system_msg = [{"role": "system", "content": system}]
        logger.info(f"system_msg: {system_msg}")

        user_assistant_msgs = [
            {"role": "assistant" if i % 2 else "user", "content": message}
            for i, message in enumerate(user_assistants)
        ]

        msgs = system_msg + user_assistant_msgs

        logger.info(f"Sending {len(msgs)} messages to OpenAI API")

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=msgs,
                max_tokens=max_tokens,
            )
        except Exception as e:
            logger.error(f"Failed to call OpenAI API: {e}")
            raise

        if not response.get("choices"):
            logger.error("No choices in the response from OpenAI API")
            raise Exception("No choices in the response from OpenAI API")

        status_code = response["choices"][0]["finish_reason"]
        assert status_code == "stop", f"The status code was {status_code}."

        logger.info("Received response from OpenAI API")

        # Update the new self.chatsummary at the end of every chat.
        self.chatsummary = self.summary_chatgpt(user_assistant_msgs)
        # logger.info(f"self.chatsummary: {self.chatsummary}")

        return response["choices"][0]["message"]["content"]
