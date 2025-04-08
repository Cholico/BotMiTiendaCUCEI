from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseReviewDomain(BaseModel):
    id: str
    rating: float
    comment: str
    sentiment: Optional[str] = None
    created_at: datetime
    updated_at: datetime