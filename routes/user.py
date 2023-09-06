"""
routes/user.py

This module provides routes for user-related operations in the FastAPI application.
It provides endpoints for creating, retrieving, and deleting user objects from the database.
Furthermore, it integrates with external services like a medical userbot and text-to-speech APIs.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Routes:
    - POST "/": Create a new user object.
    - GET "/{user_id}": Retrieve a user object by its unique ID.
    - GET "/": Retrieve all user objects.
    - DELETE "/{user_id}": Delete a user object by its unique ID.
"""

from fastapi import APIRouter, HTTPException
from database.mongodb import MongoDB

router = APIRouter()

# Initialize necessary components
mongo_db = MongoDB()

from typing import List


@router.get("/")
async def get_all_users():
    """
    Retrieve all user objects stored in the database.

    Returns:
        A list of all user objects.
    """
    mock_usernames = [
        "Jack Pineda",
        "Tasha Olson",
        "Ulysses Yates",
        "Jean Casey",
        "Janette Kirby",
    ]

    mock_sex = [
        "Male",
        "Female",
        "Male",
        "Female",
        "Female",
    ]

    return [
        {
            "id": "test_user_id",
            "username": "Mr. Test User",
            "sex": "Male",
        }
    ] + [
        {
            "id": f"test_user_{i}",
            "username": mock_usernames[i - 1],
            "sex": mock_sex[i - 1],
        }
        for i in range(1, 6)
    ]
