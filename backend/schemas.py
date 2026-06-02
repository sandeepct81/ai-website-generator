from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema for creating a new project (request)
class ProjectCreate(BaseModel):
    prompt: str

# Schema for reading project data (response)
class ProjectResponse(BaseModel):
    id: int
    prompt: str
    generated_code: str
    created_at: datetime

    class Config:
        from_attributes = True  # Enables ORM mode for SQLAlchemy

# Schema for Gemini response
class GeneratedWebsite(BaseModel):
    html: str
    css: str
    javascript: str