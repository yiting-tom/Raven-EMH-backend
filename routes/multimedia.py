"""
routes/multimedia.py

This module defines the HTTP routes related to the multimedia functionalities of the FastAPI application.
It defines endpoints for creating, retrieving, and deleting multimedia objects.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Routes:
    POST /            : Create a new multimedia object
    GET /{multimedia_id} : Retrieve a specific multimedia object by its ID
    GET /             : Retrieve all multimedia objects
    DELETE /{multimedia_id} : Delete a specific multimedia object by its ID
"""

from typing import List
from fastapi import APIRouter, HTTPException

from database.mongodb import MongoDB
from models._multimedia import MultimediaCreate, MultimediaInDBOutput
from repositories._multimedia_repo import MultimediaRepo
from services._multimedia_service import MultimediaService

router = APIRouter()

# Database initialization
mongo_db = MongoDB()
multimedia_repo = MultimediaRepo(
    mongo_db.get_database,
    mongo_db.get_collection(MultimediaRepo.COLLECTION_NAME),
    mongo_db.get_gridfs,
)

# Service initialization
multimedia_service = MultimediaService(
    repository=multimedia_repo,
)


@router.post("/", response_model=MultimediaInDBOutput)
async def create_multimedia(multimedia: MultimediaCreate):
    """
    Create a new multimedia object and save it to the database.

    Args:
        multimedia (MultimediaCreate): The multimedia object to be created.

    Returns:
        The created multimedia object, with additional information like its unique ID.
    """
    return multimedia_service.create_multimedia(multimedia)


@router.get("/{multimedia_id}")
async def get_multimedia_by_id(multimedia_id: str):
    """
    Retrieve a specific multimedia object by its unique ID.

    Args:
        multimedia_id (str): The unique ID of the multimedia object to retrieve.

    Returns:
        The multimedia object with the specified ID.
    """
    tmp = multimedia_service.get_multimedia_by_id(multimedia_id)
    return tmp


@router.get("/", response_model=List[MultimediaInDBOutput])
async def get_all_multimedias():
    """
    Retrieve all multimedia objects stored in the database.

    Returns:
        A list of all multimedia objects.
    """
    return multimedia_service.get_all_multimedias()


@router.delete("/{multimedia_id}")
async def delete_multimedia(multimedia_id: str):
    """
    Delete a specific multimedia object by its unique ID.

    Args:
        multimedia_id (str): The unique ID of the multimedia object to delete.

    Returns:
        A message confirming the deletion of the multimedia object.
    """
    multimedia_service.delete_multimedia(multimedia_id)
    return {"message": f"Multimedia {multimedia_id} deleted"}
