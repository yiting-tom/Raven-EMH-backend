"""
database/mongodb_connection.py

This module contains classes for connecting to MongoDB, testing the connection,
and closing the connection using FastAPI event handlers.

Classes:
    - MongoDB: Represents a MongoDB client for connection management and connectivity testing.
    - MongoDBConnector: Manages the integration of MongoDB with a FastAPI application.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)
"""

import os

from fastapi import FastAPI
from gridfs import GridFS
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from database._base_database import BaseDatabase, BaseDatabaseConnector
from utils.logger import logger


class MongoDB(BaseDatabase):
    """
    Class representing a MongoDB client, allowing for connection management and
    connectivity testing.
    """

    def __init__(self):
        """
        Initializes an instance of the MongoDB client.
        Uses environment variables for the host, port, username, password, and database name.
        """
        self.client = MongoClient(
            host=os.getenv("MONGODB_HOST"),
            port=int(os.getenv("MONGODB_PORT")),
            username=os.getenv("MONGODB_USER"),
            password=os.getenv("MONGODB_PASSWORD"),
        )
        self.database = self.client[os.getenv("MONGODB_NAME")]
        self.grid_fs = GridFS(self.database)

    def test_connection(self) -> bool:
        """
        Tests the connection to the MongoDB server.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        logger.info("Testing connection to MongoDB")
        try:
            self.client.server_info()
        except Exception as e:
            logger.error(e)
            return False
        return True

    def close_connection(self):
        """
        Closes the connection to the MongoDB server.
        """
        self.client.close()

    @property
    def get_database(self) -> Database:
        """
        Exposes the MongoDB database instance.

        Returns:
            Database: The MongoDB database instance.
        """
        return self.database

    @property
    def get_gridfs(self) -> GridFS:
        """
        Exposes the MongoDB GridFS instance.

        Returns:
            GridFS: The MongoDB GridFS instance.
        """
        return self.grid_fs

    def get_collection(self, name: str) -> Collection:
        """
        Exposes a MongoDB collection instance for a given collection name.

        Args:
            name (str): Name of the collection.

        Returns:
            Collection: The MongoDB collection instance.
        """
        return self.database[name]


class MongoDBConnector(BaseDatabaseConnector):
    """
    Class to manage the integration of MongoDB with a FastAPI application.
    Manages the connection and disconnection events using FastAPI event handlers.
    """

    def __init__(self, app: FastAPI):
        """
        Initializes the MongoDBConnector with a FastAPI application instance.

        Args:
            app (FastAPI): FastAPI application instance.
        """
        self.database = MongoDB()  # Initialize MongoDB instance
        self.app = app

    def connect_to_db(self):
        """
        Registers the test_connection method of the MongoDB instance to the startup event of the FastAPI application.
        """
        self.app.add_event_handler("startup", self.database.test_connection)

    def close_db_connection(self):
        """
        Registers the close_connection method of the MongoDB instance to the shutdown event of the FastAPI application.
        """
        self.app.add_event_handler("shutdown", self.database.close_connection)
