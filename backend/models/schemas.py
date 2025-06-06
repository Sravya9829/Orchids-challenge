from pydantic import BaseModel, HttpUrl
from typing import Optional
from enum import Enum

class CloneStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class CloneRequest(BaseModel):
    url: HttpUrl
    
class CloneResponse(BaseModel):
    job_id: str
    status: CloneStatus
    message: str
    
class CloneResult(BaseModel):
    job_id: str
    status: CloneStatus
    original_url: str
    cloned_html: Optional[str] = None
    error_message: Optional[str] = None