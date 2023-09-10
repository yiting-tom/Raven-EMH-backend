from typing import Dict, List

import firebase_admin
from firebase_admin import auth, firestore
from loguru import logger

from models import UserDataInFirebaseAuth, UserDataInFirestore, UserOutput


class UserRepo:
    def __init__(self):
        # Ensure you've initialized Firebase Admin SDK prior to using it here.
        # Typically, you'd do this once at the start of your application.
        self.db = firestore.client()
        self.users_collection = self.db.collection("users")

    def get_all_users(self) -> List[UserOutput]:
        """Retrieve all users from Firestore."""
        user_in_auth: List[UserDataInFirebaseAuth] = [
            UserDataInFirebaseAuth(**user.__dict__["_data"])
            for user in auth.list_users().iterate_all()
        ]
        user_in_firestore: Dict[str, UserDataInFirestore] = {
            user.id: UserDataInFirestore(**user.to_dict())
            for user in self.users_collection.stream()
        }
        logger.debug(f"Found {len(user_in_auth)} users in Firebase Auth")
        return [
            UserOutput(
                **user.model_dump(), **user_in_firestore[user.localId].model_dump()
            )
            for user in user_in_auth
        ]

    def get_user_by_id(self, user_id: str) -> UserOutput:
        """Retrieve a user from Firestore by its ID."""
        user_in_auth: UserDataInFirebaseAuth = UserDataInFirebaseAuth(
            **auth.get_user(user_id).__dict__["_data"]
        )
        user_in_firestore: UserDataInFirestore = UserDataInFirestore(
            **self.users_collection.document(user_id).get().to_dict()
        )
        return UserOutput(**user_in_auth.model_dump(), **user_in_firestore.model_dump())
