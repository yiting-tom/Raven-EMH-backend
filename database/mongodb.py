"""
MongoDB Connection Module for FastAPI
Author: Yi-Ting Li
Email: yitingli.public@gmail.com
Date Created: 2023-08-17
Last Modified: 2023-08-17

This module contains classes for connecting to MongoDB, testing the
connection, and closing the connection using FastAPI event handlers.
"""

import os

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from utils.logger import logger


class MongoDB:
    """
    Class representing a MongoDB client, allowing for connection management and
    connectivity testing.
    """

    def __init__(self):
        """
        Initializes an instance of the MongoDB client.
        Uses environment variables for the host, port, username, password, and database name.
        """
        self.client = AsyncIOMotorClient(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        self.database = self.client[os.getenv("DB_NAME")]

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


class MongoDBConnector:
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
        self.mongodb = MongoDB()
        self.app = app

    def connect_to_mongo(self):
        """
        Registers the test_connection method of the MongoDB instance to the startup event of the FastAPI application.
        """
        self.app.add_event_handler("startup", self.mongodb.test_connection)

    def close_mongo_connection(self):
        """
        Registers the close_connection method of the MongoDB instance to the shutdown event of the FastAPI application.
        """
        self.app.add_event_handler("shutdown", self.mongodb.close_connection)
