from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from src.database.database import Base
from datetime import datetime
from datetime import timezone

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    news_text = Column(Text)
    category = Column(String)
    priority = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey('users.id'))

