from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import auth

app = FastAPI(title="Electronic Dean's Office", version="0.4.0")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Electronic Dean's Office API v0.4.0"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "SQLite",
        "tables": len(Base.metadata.tables)
    }