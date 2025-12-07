from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from datetime import datetime


class NewsModel(BaseModel):
    title: str
    news_text: str
    category: str
    priority: Annotated[int, Field(ge=1, le=5)]

class NewsResponse(NewsModel):
    id: Annotated[int, Field(ge=1)]
    created_at: datetime

    class Config:
        from_attributes = True