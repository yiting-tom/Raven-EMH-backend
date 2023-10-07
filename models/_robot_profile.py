from datetime import datetime
from typing import List, Optional

import numpy as np
from pydantic import BaseModel, Field

# 1. request from frontend: ChatCreateRequest, ChatDeleteRequest, ChatGetRequest, (ChatUpdateRequest - not implemented)
# - route: ChatRouter

# 2. data in backend: ChatCreate, ChatDelete, ChatGet, (ChatUpdate - not implemented)
# - service: ChatService

# 3. data in database: ChatInDB
# - repository: ChatRepo

# 4. response to frontend: ChatInDBResponse
# - route: ChatRouter


class Filter(BaseModel):
    isRegex: bool
    name: str
    prompt: str
    model: Optional[str] = "gpt-3.5-turbo"


# Data storage in memory `RobotProfileService.robot_profiles_cache`
class RobotProfileInCache(BaseModel):
    robot_id: str
    model: str  # openai model id
    voice: str  # polly voice id
    filters: List[Filter]
    options: List[str]
    prompt: str
    image_np_array: np.array

    class Config:
        arbitrary_types_allowed = True


# Data storage in firestore
class RobotProfileCreateRequest(BaseModel):
    robot_id: str
    model: str  # openai model id
    filters: List[Filter]
    options: List[str]
    prompt: str
    name: str
    voice: str  # polly voice id
    description: str
    imageURL: str  # firebase storage image url

    class Config:
        json_schema_extra = {
            "example": {
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
            }
        }


# Data storage in mongodb
class RobotProfileInDBCreate(BaseModel):
    name: str
    model: str  # openai model id
    filters: List[Filter]
    options: List[str]
    prompt: str
    # =========== will not be used ===========
    # voice: str             # polly voice id
    # description: str      # will not be used
    # imageURL: str         # change to base64


# Data representation in frontend
class RobotProfileInDB(RobotProfileInDBCreate):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
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
            }
        }
