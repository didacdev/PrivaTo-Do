from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Task(BaseModel):
    id_hash: Optional[str]
    timestamp: Optional[datetime]
    data: str
    last_hash: Optional[str]
    completed: Optional[bool]
