from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskData(BaseModel):
    data: str


class TaskDB(TaskData):
    id_hash: Optional[str]
    timestamp: Optional[datetime]
    last_hash: Optional[str]
    completed: Optional[bool]
