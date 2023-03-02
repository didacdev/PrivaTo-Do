from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskData(BaseModel):
    """
    It is used to create a new task in the database from de data field.
    """
    data: str


class TaskDB(TaskData):
    """
    It represents a block of the blockchain in the database. It is a full task.
    """
    id_hash: Optional[str]
    timestamp: Optional[datetime]
    last_hash: Optional[str]
    completed: Optional[bool]
