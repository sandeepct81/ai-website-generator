from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json

from database import engine, get_db
from models import Base, Project
from schemas import ProjectCreate, ProjectResponse
from gemini_service import generate_website, combine_code

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="AI Website Generator API")

# Configure CORS - VERY IMPORTANT for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "file://"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Website Generator API is running"}

@app.post("/generate", response_model=ProjectResponse)
async def generate_website_endpoint(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Generate a website based on user prompt and save to database
    """
    try:
        # Step 1: Call Gemini to generate website
        generated_parts = generate_website(project.prompt)
        
        # Step 2: Combine into complete HTML
        complete_html = combine_code(
            generated_parts["html"],
            generated_parts["css"],
            generated_parts["javascript"]
        )
        
        # Step 3: Save to database
        db_project = Project(
            prompt=project.prompt,
            generated_code=complete_html
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Step 4: Return response with all data
        return db_project
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.get("/projects", response_model=List[ProjectResponse])
def get_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get list of all generated projects
    """
    projects = db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    return projects

@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Get a specific project by ID
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """
    Delete a project
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)