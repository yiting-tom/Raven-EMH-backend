"""
external/tts/_base_tts.py

This module defines the base class and exceptions for Text-To-Speech (TTS) operations.
The `BaseTTS` abstract base class is intended to be subclassed by concrete TTS service implementations.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - AudioGenerationFailed: Exception raised when audio generation fails.
    - AudioUrlListLengthError: Exception raised when the audio URL list length is more than 1.
    - BaseTTS: Abstract base class for Text-To-Speech services.
"""

from abc import ABC, abstractmethod


class AudioGenerationFailed(Exception):
    """
    Exception that is raised when the audio generation fails.

    Usage:
        raise AudioGenerationFailed("Specific reason for failure")
    """

    pass


class AudioUrlListLengthError(Exception):
    """
    Raised when the audio URL list length is more than 1.

    Usage:
        raise AudioUrlListLengthError("Specific reason for exceeding the list length")
    """

    pass


class BaseTTS(ABC):
    """
    Abstract base class for Text-To-Speech services. This class must be subclassed by specific
    TTS service implementations. It ensures that any TTS service provides the `text_to_speech`
    method for generating audio data from text.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the TTS service. Any configuration or setup for the specific TTS service
        should be done here.
        """
        super().__init__()

    @abstractmethod
    def text_to_speech(self, text: str, *args, **kwargs) -> bytes:
        """
        Convert the provided text to audio data. This method must be implemented by the subclasses.

        Args:
            text (str): The text to be converted to speech.

        Returns:
            bytes: The audio data in bytes.

        Raises:
            NotImplementedError: If this method is not implemented by a subclass.
        """
        raise NotImplementedError
