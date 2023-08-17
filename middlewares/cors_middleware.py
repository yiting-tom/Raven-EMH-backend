"""
CORS Middleware for FastAPI
Author: Yi-Ting Li
Email: yitingli.public@gmail.com
Date Created: 2023-08-17
Last Modified: 2023-08-17

Middleware configuration for handling Cross-Origin Resource Sharing (CORS) in a FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# A list of origins that are allowed to make cross-origin requests
# to this FastAPI application. For example, if your frontend is
# running on http://localhost:3000, you would add that URL to this list.
origins = [
    "http://localhost:3000",  # React server
]


def add_middleware(app: FastAPI):
    """
    Add CORS middleware to the FastAPI app instance.

    This function configures how the FastAPI application handles
    cross-origin requests by adding CORS (Cross-Origin Resource Sharing)
    middleware to the FastAPI app instance. It defines which origins are
    allowed to access resources, what methods can be used when accessing
    the resources, and which headers can be used during the request.

    Parameters:
    app (FastAPI): The FastAPI application instance to which the middleware will be added.

    Returns:
    FastAPI: The FastAPI application instance after adding the middleware.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # List of origins that are allowed to make cross-origin requests
        allow_credentials=True,  # Allow cookies to be sent and credentials to be included in the response
        allow_methods=["*"],  # Allow all HTTP methods (e.g., GET, POST, PUT, DELETE)
        allow_headers=["*"],  # Allow all headers to be sent in the request
    )

    return app
