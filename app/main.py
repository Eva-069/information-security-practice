from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.auth.router import router as auth_router
from app.routes.students import router as students_router
from app.routes.teachers import router as teachers_router
from app.routes.admin import router as admin_router

app = FastAPI(title="Electronic Dean's Office", version="0.5.0")

app.include_router(auth_router)
app.include_router(students_router)
app.include_router(teachers_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Electronic Dean's Office API v0.5.0"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "SQLite",
        "tables": len(Base.metadata.tables)
    }