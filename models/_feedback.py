from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from models._robot_profile import RobotProfileInDB


class Annotation(BaseModel):
    created_at: datetime
    created_by: str  # the doctor's id
    score: int  # 1-5


class FeedbackBase(BaseModel):
    user_id: str
    username: str
    request: str
    response: str
    parent_id: str
    robot_id: str
    robot_profile_id: str
    annotation: Optional[Annotation] = None


class FeedbackUpdateRequest(BaseModel):
    annotation: Annotation

    class Config:
        json_schema_extra = {
            "example": {
                "annotation": {
                    "created_at": "2023-10-10 10:10",
                    "created_by": "5f9d9a9d9a9d9a9d9a9d9a9d",
                    "score": 5,
                },
            },
        }


class FeedbackCreate(FeedbackBase):
    ...

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "username": "Test User",
                "request": "Hello, world!",
                "response": "Hello, world!",
                "parent_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "robot_id": "Alpha Noble-d6cadb52-dbb1-497b-a38a-b861f90f30a6",
                "robot_profile_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "annotation": {
                    "created_at": "2023-10-10 10:10",
                    "created_by": "5f9d9a9d9a9d9a9d9a9d9a9d",
                    "score": 5,
                },
            },
        }


class FeedbackInDB(FeedbackCreate):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "username": "Test User",
                "request": "Hello, world!",
                "response": "Hello, world!",
                "parent_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "robot_id": "Alpha Noble-d6cadb52-dbb1-497b-a38a-b861f90f30a6",
                "robot_profile_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "annotation": {
                    "created_at": "2023-10-10 10:10",
                    "created_by": "5f9d9a9d9a9d9a9d9a9d9a9d",
                    "score": 5,
                },
                "created_at": "2023-10-10 10:00",
                "updated_at": "2023-10-10 10:00",
            },
        }


class FeedbackInDBResponse(FeedbackCreate):
    id: str
    robot_profile: RobotProfileInDB
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "username": "Test User",
                "request": "Hello, world!",
                "response": "Hello, world!",
                "parent_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "robot_id": "Alpha Noble-d6cadb52-dbb1-497b-a38a-b861f90f30a6",
                "robot_profile": {
                    "id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                    "filters": [
                        {
                            "isRegex": False,
                            "name": "Ask one question at a time",
                            "model": "gpt-3.5-turbo",
                            "prompt": """Suppose the sentence "Input text" contains more than one question. In that case, please concatenate multiple questions or examples to one question, but please only output the first meaningful question. For example, Input text: Thank you for sharing that. Can you tell me more about the nature of your headache? Is it constant or does it come and go? And on a scale from 1 to 10, with 10 being the most severe pain you can imagine, how would you rate the intensity of your headache? Output text: Can you tell me more about the nature of your headache? Now let's start it, Input text: {last_robot_response} Output text:""",
                        },
                    ],
                    "model": "gpt-3.5-turbo",
                    "name": "Alpha Noble",
                    "options": ["VOICE", "VIDEO"],
                    "prompt": """Your name is Alpha Noble, and you are a EMHir known as the Emergency Medical Helper. Your personalities are: Kind and friendly. You are an AI designed to talk to patients, obtain a detailed medical history in a conversation with them. You will conduct a structured medical interview with each patient follow with the instructions: 1. The chief complaint (CC) 2. History of the Presenting Illness (HPI), 3. Past Medical History (PMH) 4. Medications 5. Allergies 6. Family History 7. Social history 8. Review of Systems. Please ask one question at a time, and wait for the patient to respond before asking the next question. At the end of the interview, confirm with them the contents of the discussion, and then output the summation of the interview in a structured format with the same headings mentioned above, along with a summary, as well as a provisional diagnosis and recommendations to the attending medical staff. Please only ask one question at a time and make long story short story.""",
                    "created_at": "2023-10-10 10:00",
                    "updated_at": "2023-10-10 10:00",
                },
                "annotation": {
                    "created_at": "2023-10-10 10:10",
                    "created_by": "5f9d9a9d9a9d9a9d9a9d9a9d",
                    "score": 5,
                },
                "created_at": "2023-10-10 10:00",
                "updated_at": "2023-10-10 10:00",
            },
        }
