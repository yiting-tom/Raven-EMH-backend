"""
utils/converter.py

This module contains utility functions for handling various conversions related to binary data.
These functions are primarily used to facilitate the storage and transmission of multimedia files.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Functions:
    - bytes2base64: Converts binary data to a base64 encoded string.
    - base642bytes: Converts a base64 encoded string back to binary data.
    - bytes2bson: Converts binary data to a BSON binary data format.
    - bytes2file: Writes binary data to a file.
    - file2bytes: Reads binary data from a file.
"""

import base64
import tempfile
from io import BytesIO
from typing import Optional, Union

import cv2
import numpy as np
import requests
from bson import Binary
from moviepy.editor import AudioClip, VideoClip


def bytes2base64(source: bytes) -> str:
    """
    Converts binary data to a base64 encoded string.

    Parameters:
        source (bytes): The binary data to be encoded.

    Returns:
        str: The base64 encoded string representation of the input binary data.
    """
    return base64.b64encode(source).decode()


def base642bytes(source: str) -> bytes:
    """
    Converts a base64 encoded string back to binary data.

    Parameters:
        source (str): The base64 encoded string.

    Returns:
        bytes: The decoded binary data.
    """
    return base64.b64decode(source.encode())


def bytes2bson(source: bytes) -> Binary:
    """
    Converts binary data to a BSON binary data format.

    Parameters:
        source (bytes): The binary data to be converted.

    Returns:
        Binary: The BSON binary data format of the input binary data.
    """
    return Binary(source)


def bytes2file(source: bytes, filename: str) -> str:
    """
    Writes binary data to a file.

    Parameters:
        source (bytes): The binary data to be written to a file.
        filename (str): The name of the file to which the data should be written.

    Returns:
        str: The name of the file where the data was written.
    """
    with open(filename, "wb") as f:
        f.write(source)
    return filename


def file2bytes(filename: str, mode: str = "rb") -> bytes:
    """
    Reads binary data from a file.

    Parameters:
        filename (str): The name of the file from which to read the data.
        mode (str): The mode in which the file should be opened. Defaults to 'rb' (read binary).

    Returns:
        bytes: The binary data read from the file.
    """
    with open(filename, mode) as f:
        return f.read()


def bytes2bytesio(source: bytes) -> BytesIO:
    """
    Converts binary data to a BytesIO object.

    Parameters:
        source (bytes): The binary data to be converted.

    Returns:
        BytesIO: The BytesIO object of the input binary data.
    """
    return BytesIO(source)


def file2bytesio(filename: str) -> BytesIO:
    """
    Reads binary data from a file.

    Parameters:
        filename (str): The name of the file from which to read the data.

    Returns:
        BytesIO: The binary data read from the file.
    """
    return BytesIO(file2bytes(filename))


def url2numpy(
    image_url: str,
    flags: Optional[int] = cv2.IMREAD_COLOR,
    to_rgb: Optional[bool] = True,
) -> np.array:
    """
    Reads binary data from a file.

    Parameters:
        image_url (str): The name of the file from which to read the data.

    Returns:
        np.array: The image data read from the URL.
    """
    # Get the image as a stream of bytes from the URL
    response = requests.get(image_url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Convert the stream of bytes into a numpy array
    image_bytes = np.asarray(
        bytearray(response.content),
        dtype=np.uint8,
    )
    image_bgr = cv2.imdecode(image_bytes, flags=flags)

    if image_bgr is None:
        raise ValueError("Image could not be loaded. Check the URL or the network.")

    if not to_rgb:
        return image_bgr

    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)


def clip_to_base64(clip: Union[VideoClip, AudioClip], codec="libx264", **kwargs) -> str:
    """
    Converts a moviepy clip to a base64 encoded string.

    Parameters:
        clip (Union[VideoClip, AudioClip]): The moviepy clip to be converted.
        codec (str): The codec to be used for the output video. Defaults to 'libx264'.
        **kwargs: Additional keyword arguments to be passed to the write_videofile() method.

    Returns:
        str: The base64 encoded string representation of the input moviepy clip.
    """
    suffix = ".mp4" if isinstance(clip, VideoClip) else ".mp3"
    # Use a temporary file to write the video
    with tempfile.NamedTemporaryFile(delete=True, suffix=suffix) as temp_file:
        clip.write_videofile(temp_file.name, codec=codec, **kwargs)

        # Convert the temporary file's content to base64
        with open(temp_file.name, "rb") as f:
            video_base64 = base64.b64encode(f.read()).decode("utf-8")

    return video_base64
