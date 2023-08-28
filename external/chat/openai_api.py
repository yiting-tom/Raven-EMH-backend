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
from typing import List, Optional

import openai
from loguru import logger


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

    def chat(self, user_assistants: List[str], system: Optional[str] = None) -> str:
        """
        Chat with the OpenAI API.

        Args:
            user_assistants (List[str]): A list of strings that alternate between user and assistant messages.
            system (Optional[str]): A string containing the system message. Defaults to None.

        Returns:
            str: The response from the assistant.
        """
        DEFAULT_SYSTEM = "You are EMHir, also known as the Emergency Medical Helper. You are an AI designed to talk to patients, obtain a detailed medical history in a conversation with them.  You are wise, polite, affable, kind and patient.  You will conduct a structured medical interview with each patient starting with the chief complaint (CC), moving on to the History of the Presenting Illness (HPI), then to Past Medical History (PMH), Medications, Allergies, Family History, Social history, Review of Systems. The interview may go into tangents, and you may politely make small-talk with the patient to earn their confidence, discussing the weather, their family history, or personal anecdotes, but please politely direct them back to the directed medical history.  At the end of the interview, please thank the patient, confirm with them the contents of the discussion, and then output the summation of the interview in a structured format with the same headings mentioned above, along with a summary, as well as a provisional diagnosis and recommendations to the attending medical staff."
        system = system or DEFAULT_SYSTEM

        assert isinstance(user_assistants, list), "`user_assistants` should be a list"

        system_msg = [{"role": "system", "content": system}]
        user_assistant_msgs = [
            {"role": "assistant" if i % 2 else "user", "content": message}
            for i, message in enumerate(user_assistants)
        ]

        msgs = system_msg + user_assistant_msgs

        logger.info(f"Sending {len(msgs)} messages to OpenAI API")

        try:
            response = openai.ChatCompletion.create(model=self.model, messages=msgs)
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
