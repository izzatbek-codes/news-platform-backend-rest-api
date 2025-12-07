from sqlalchemy import Column, String, Integer, Boolean, DateTime
from src.database.database import Base
from datetime import datetime
from datetime import timezone

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=datetime.now(timezone.utc))






