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
from io import BytesIO

import requests
from bson import Binary


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


def url2base64(image_url: str) -> str:
    """url2base64

    Args:
        image_url (str): The URL of the image.

    Returns:
        str: The base64 encoded
    """
    # Send a HTTP request to the URL of the image
    response = requests.get(image_url)

    # Check if the request was successful (HTTP Status Code 200)
    if response.status_code == 200:
        # Get the content of the response
        image_data = response.content

        # Convert the image data to a base64 string
        base64_str = base64.b64encode(image_data).decode("utf-8")
        return base64_str
    else:
        raise ValueError("Image could not be loaded. Check the URL or the network.")
