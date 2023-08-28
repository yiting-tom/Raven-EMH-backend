"""
external/tts/aws_polly_tts.py

This module provides an interface to AWS Polly, a service that turns text into lifelike speech. It allows the 
conversion of text to speech using the Polly API and is integrated as a Text-To-Speech (TTS) engine for the FastAPI 
application.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - PollyTTS: A TTS converter leveraging AWS Polly for text-to-speech synthesis.
"""

import os
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from loguru import logger

from external.tts._base_tts import AudioGenerationFailed, BaseTTS


class PollyTTS(BaseTTS):
    """
    A Text-To-Speech converter leveraging AWS Polly.

    Attributes:
        aws_access_key_id (str): The AWS Access Key ID used to authenticate with Polly.
        aws_secret_access_key (str): The AWS Secret Access Key used to authenticate with Polly.
        aws_region (str): The AWS Region where Polly is available.
        polly_client (boto3.client): The boto3 client instance to interact with AWS Polly.
    """

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_region: Optional[str] = None,
    ):
        """
        Initialize a PollyTTS instance.

        Parameters:
            aws_access_key_id (Optional[str]): The AWS Access Key ID used to authenticate with Polly.
            aws_secret_access_key (Optional[str]): The AWS Secret Access Key used to authenticate with Polly.
            aws_region (Optional[str]): The AWS Region where Polly is available.
        """
        self.aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.getenv(
            "AWS_SECRET_ACCESS_KEY"
        )
        self.aws_region = aws_region or os.getenv("AWS_REGION")

        self.polly_client = boto3.client(
            "polly",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region,
        )

    def text_to_speech(
        self, text: str, output_format: str = "mp3", voice_id: str = "Matthew"
    ) -> bytes:
        """
        Convert text to speech by sending a request to AWS Polly.

        Parameters:
            text (str): The text that needs to be converted to speech.
            output_format (str): The format of the speech file. Defaults to 'mp3'.
            voice_id (str): The voice used for the speech generation. Defaults to 'Joanna'.

        Returns:
            bytes: The generated audio in bytes.

        Raises:
            AudioGenerationFailed: If the audio generation fails.
        """
        try:
            # Perform text-to-speech synthesis
            response = self.polly_client.synthesize_speech(
                Text=text, OutputFormat=output_format, VoiceId=voice_id
            )
            return response["AudioStream"].read()
        except (BotoCoreError, ClientError) as error:
            logger.error(f"Audio generation failed with error: {error}")
            raise AudioGenerationFailed("Audio generation failed") from error
