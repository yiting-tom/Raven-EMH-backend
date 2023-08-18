"""
repositories/__init__.py

This module initializes the `repositories` package and exposes the relevant
classes and exceptions that are defined in the underlying modules. The
`repositories` package contains classes that handle interactions between
the FastAPI application and the database, effectively acting as the data
access layer of the application.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Exports:
    - IdNotFoundError: Exception raised when a requested ID is not found in the database.
    - MultimediaRepo: Repository class for handling CRUD operations related to
                      multimedia objects in the database.
"""

from repositories._base_repo import IdNotFoundError
from repositories._multimedia_repo import MultimediaRepo

# The IdNotFoundError exception and the MultimediaRepo class are now exposed
# at the package level, allowing them to be imported directly from `repositories`
# instead of from the underlying modules.
