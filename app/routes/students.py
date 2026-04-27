from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Grade
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/me/grades")
def get_my_grades(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    grades = db.query(Grade).filter(Grade.student_id == current_user.id).all()
    return {
        "student": current_user.username,
        "grades": [
            {"subject_id": g.subject_id, "grade": g.grade, "date": str(g.date_assigned)}
            for g in grades
        ],
    }