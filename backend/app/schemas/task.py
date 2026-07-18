from pydantic import BaseModel, Field,ConfigDict
import uuid

class TaskCreateRequest(BaseModel):
    task_title : str = Field(..., min_length=1,max_length=100)
    descryption: str = Field(default="")
    status: str = Field(default="active")

class TaskResponse(BaseModel):
    task_id : uuid.UUID
    task_title : str = Field(..., min_length=1,max_length=100)
    descryption : str = Field(default="")
    status : str
    user_id : uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class TaskStatusUpdateRequest(BaseModel):
    status : str
