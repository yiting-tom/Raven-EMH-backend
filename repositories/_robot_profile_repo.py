from typing import List, Optional

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database

from models import RobotProfileInDB, RobotProfileInDBCreate


class RobotProfileRepo:
    def __init__(self, db: Database, collection: Collection):
        # Create a MongoClient and specify the database and collection
        self.db: Database = db
        self.collection: Collection = collection

    def create_robot_profile(self, robot_profile: RobotProfileInDBCreate) -> str:
        # Insert a new robot_profile document into the database and return its id
        result = self.collection.insert_one(robot_profile.model_dump())
        return str(result.inserted_id)

    def get_robot_profile(self, robot_profile_id: str) -> Optional[RobotProfileInDB]:
        # Find a robot_profile document by its id
        robot_profile_data = self.collection.find_one(
            {"_id": ObjectId(robot_profile_id)}
        )

        def object_id_to_str(robot_profile_data):
            robot_profile_data["id"] = str(robot_profile_data["_id"])
            del robot_profile_data["_id"]
            return robot_profile_data

        if robot_profile_data:
            return RobotProfileInDB(**object_id_to_str(robot_profile_data))
        return None

    @staticmethod
    def object_id_to_str(obj):
        obj["id"] = str(obj["_id"])
        del obj["_id"]
        return obj

    def get_robot_profiles(
        self, order_by: Optional[str] = "created_at"
    ) -> List[RobotProfileInDB]:
        # Find all robot_profile documents
        robot_profiles_data = self.collection.find(
            {}, {"_id": 0}, sort=[(order_by, -1)]
        )

        if robot_profiles_data:
            return [
                RobotProfileInDB(**self.object_id_to_str(robot_profile_data))
                for robot_profile_data in robot_profiles_data
            ]
        return []

    def delete_robot_profile(self, robot_profile_id: str) -> bool:
        # Delete a robot_profile document by its id and return whether the operation was successful
        result = self.collection.delete_one({"_id": ObjectId(robot_profile_id)})
        return result.deleted_count > 0
