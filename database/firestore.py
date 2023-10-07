from typing import Any, Dict, Optional

import firebase_admin
from fastapi import FastAPI
from firebase_admin import firestore

from database._adapter import (
    DatabaseAdapter,
)  # Assume DatabaseAdapter is in a module named database_adapter
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


class FirestoreAdapter(DatabaseAdapter):
    def __init__(self):
        self.db = firestore.Client()

    def create(self, collection: str, document: Dict[str, Any]) -> Dict[str, Any]:
        doc_ref = self.db.collection(collection).add(document)
        return {"id": doc_ref.id}

    def read(self, collection: str, filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        docs = (
            self.db.collection(collection)
            .where(list(filter.keys())[0], "==", list(filter.values())[0])
            .stream()
        )
        for doc in docs:
            return {"id": doc.id, **doc.to_dict()}
        return None

    def update(self, collection: str, doc_id: str, update: Dict[str, Any]) -> None:
        doc_ref = self.db.collection(collection).document(doc_id)
        doc_ref.update(update)

    def delete(self, collection: str, doc_id: str) -> None:
        self.db.collection(collection).document(doc_id).delete()
