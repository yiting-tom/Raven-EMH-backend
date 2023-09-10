import firebase_admin
from fastapi import FastAPI
from firebase_admin import firestore

from database._base_database import BaseDatabase, BaseDatabaseConnector


class Firebase(BaseDatabase):
    """
    Class representing a Firebase Firestore client.
    """

    def __init__(self):
        """
        Initializes an instance of the Firebase Firestore client.
        Uses a service account JSON for authentication.
        """
        # Get Firestore client
        self.database = firestore.client()

    def test_connection(self) -> bool:
        """
        Tests the connection to the Firestore.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        try:
            # Try retrieving the collections to test the connection.
            # This may vary based on how you'd like to test your connection.
            _ = list(self.database.collections())
            return True
        except Exception as e:
            print(e)  # or log it
            return False

    def close_connection(self):
        """
        Firebase Admin SDK handles connection pooling, so there isn't a direct
        "close" operation. However, you can delete the app instance if needed.
        """
        firebase_admin.delete_app(self.app)

    @property
    def get_database(self) -> firestore.client:
        """
        Exposes the Firebase Firestore client instance.
        """
        return self.database


class FirebaseConnector(BaseDatabaseConnector):
    """
    Class to manage the integration of Firebase with a FastAPI application.
    Manages the connection and disconnection events using FastAPI event handlers.
    """

    def __init__(self, app: FastAPI):
        """
        Initializes the FirebaseConnector with a FastAPI application instance.
        Args:
            app (FastAPI): FastAPI application instance.
        """
        self.database = Firebase()  # Initialize Firebase instance
        self.app = app

    def connect_to_db(self):
        """
        Registers the test_connection method of the Firebase instance
        to the startup event of the FastAPI application.
        """
        self.app.add_event_handler("startup", self.database.test_connection)

    def close_db_connection(self):
        """
        Registers the close_connection method of the Firebase instance
        to the shutdown event of the FastAPI application.
        """
        self.app.add_event_handler("shutdown", self.database.close_connection)
