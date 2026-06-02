from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String(500), nullable=False)  # User's input prompt
    generated_code = Column(Text, nullable=False)  # Complete website code
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Project(id={self.id}, prompt={self.prompt[:30]}...)>"