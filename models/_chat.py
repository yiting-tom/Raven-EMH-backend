from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from models._robot_profile import RobotProfileCreateRequest

# 1. request from frontend: ChatCreateRequest, ChatDeleteRequest, ChatGetRequest, (ChatUpdateRequest - not implemented)
# - route: ChatRouter

# 2. data in backend: ChatCreate, ChatDelete, ChatGet, (ChatUpdate - not implemented)
# - service: ChatService

# 3. data in database: ChatInDB
# - repository: ChatRepo

# 4. response to frontend: ChatInDBResponse
# - route: ChatRouter


class ChatsGetRequest(BaseModel):
    user_id: str
    robot_id: str
    order_by: Optional[str] = "created_at"
    filter: Optional[Dict[str, str]] = None


class ChatData(BaseModel):
    user_id: str
    parent_id: str
    username: str
    message: str
    history: List[str]


class ChatCreateRequest(BaseModel):
    chat_data: ChatData
    robot_profile: RobotProfileCreateRequest

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "chat_data": {
                    "user_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                    "parent_id": "",
                    "username": "John Doe",
                    "message": "I have a headache.",
                    "history": [
                        "What is your name?",
                        "Hello, my name is Alpha Noble",
                    ],
                },
                "robot_profile": {
                    "robot_id": "Alpha Noble-d6cadb52-dbb1-497b-a38a-b861f90f30a6",
                    "voice": "Arthur (Neural)",
                    "description": "A robot that can chat with you.",
                    "filters": [
                        {
                            "isRegex": False,
                            "name": "Ask one question at a time",
                            "model": "gpt-3.5-turbo",
                            "prompt": """Suppose the sentence "Input text" contains more than one question. In that case, please concatenate multiple questions or examples to one question, but please only output the first meaningful question. For example, Input text: Thank you for sharing that. Can you tell me more about the nature of your headache? Is it constant or does it come and go? And on a scale from 1 to 10, with 10 being the most severe pain you can imagine, how would you rate the intensity of your headache? Output text: Can you tell me more about the nature of your headache? Now let's start it, Input text: {last_robot_response} Output text:""",
                        },
                    ],
                    "imageURL": "https://firebasestorage.googleapis.com/v0/b/raven-emh-robot.appspot.com/o/images%2Femh%2FAlpha%20Noble-d6cadb52-dbb1-497b-a38a-b861f90f30a6?alt=media&token=594fb450-5697-4fb8-a8c7-8d7a5a5f5763&_gl=1*1yj98ei*_ga*MTY3NTkzMzMxNS4xNjkzMzIxOTky*_ga_CW55HF8NVT*MTY5NjY2MjI0OS43MC4xLjE2OTY2NjIyNTYuNTMuMC4w",
                    "model": "gpt-3.5-turbo",
                    "name": "Alpha Noble",
                    "options": ["VOICE", "VIDEO"],
                    "prompt": """Your name is Alpha Noble, and you are a EMHir known as the Emergency Medical Helper. Your personalities are: Kind and friendly. You are an AI designed to talk to patients, obtain a detailed medical history in a conversation with them. You will conduct a structured medical interview with each patient follow with the instructions: 1. The chief complaint (CC) 2. History of the Presenting Illness (HPI), 3. Past Medical History (PMH) 4. Medications 5. Allergies 6. Family History 7. Social history 8. Review of Systems. Please ask one question at a time, and wait for the patient to respond before asking the next question. At the end of the interview, confirm with them the contents of the discussion, and then output the summation of the interview in a structured format with the same headings mentioned above, along with a summary, as well as a provisional diagnosis and recommendations to the attending medical staff. Please only ask one question at a time and make long story short story.""",
                },
            },
        }


class ChatCreateResponse(BaseModel):
    id: str
    request: str
    response: str
    audio_base64: Optional[str]
    video_base64: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "request": "What is your name?",
                "response": "Hello, my name is Alpha Noble",
                "audio_base64": "UklGRkZ6BwBXQVZFZm10IBAAAAABAAEAwF0AAIC7AAAC...",
                "video_base64": "UklGRkZ6BwBXQVZFZm10IBAAAAABAAEAwF0AAIC7AAAC...",
            },
        },
    }


class ChatDeleteRequest(BaseModel):
    id: str

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "5f9d9a9d9a9d9a9d9a9d9a9d",
            },
        }


class ChatGetRequest(BaseModel):
    id: str

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "5f9d9a9d9a9d9a9d9a9d9a9d",
            },
        }


class ChatInDBCreate(BaseModel):
    user_id: str
    robot_id: str
    robot_profile_id: str
    parent_id: str
    children_ids: List[str]
    request: str
    response: str


class ChatInDB(ChatInDBCreate):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "user_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "robot_id": "Alpha Noble-d6cadb52-dbb1-497b-a38a-b861f90f30a6",
                "robot_profile_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "parent_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "children_ids": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "request": "What is your name?",
                "response": "Hello, my name is Alpha Noble",
                "created_at": "2023-10-10 10:10",
                "updated_at": "2023-10-10 10:10",
            },
        },
    }
