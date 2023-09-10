from abc import ABC, abstractmethod

from fastapi import FastAPI


class BaseDatabase(ABC):
    """
    Abstract Base Class representing a generic database client.
    This provides a blueprint for any database client implementation.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Tests the connection to the database server.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def close_connection(self):
        """
        Closes the connection to the database server.
        """
        raise NotImplementedError


class BaseDatabaseConnector(ABC):
    """
    Abstract Base Class to manage the integration of a generic database
    with a FastAPI application.
    Manages the connection and disconnection events using FastAPI event handlers.
    """

    database: BaseDatabase  # This type hint ensures that any child class will use a BaseDatabase derivative for its database.

    def __init__(self, app: FastAPI):
        """
        Initializes the BaseDatabaseConnector with a FastAPI application instance.

        Args:
            app (FastAPI): FastAPI application instance.
        """
        raise NotImplementedError

    @abstractmethod
    def connect_to_db(self):
        """
        Registers the database connection method to the startup event of the FastAPI application.
        """
        raise NotImplementedError

    @abstractmethod
    def close_db_connection(self):
        """
        Registers the database close connection method to the shutdown event of the FastAPI application.
        """
        raise NotImplementedError
