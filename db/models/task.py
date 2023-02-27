from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskDB(BaseModel):
    id_hash: Optional[str]
    timestamp: Optional[datetime]
    data: str
    last_hash: Optional[str]
    completed: Optional[bool]


class TaskData(BaseModel):
    data: str

