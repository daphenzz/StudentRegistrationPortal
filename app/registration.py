from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Student
from app.schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing_student = (
        db.query(Student)
        .filter(Student.student_number == student.student_number)
        .first()
    )
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu öğrenci numarası zaten kayıtlı.",
        )

    new_student = Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get("/by-faculty", response_model=List[StudentResponse])
def get_students_by_faculty(
    faculty: str = "Faculty of Engineering",
    db: Session = Depends(get_db),
):
    statement = text("SELECT * FROM students WHERE faculty = :faculty")
    return db.execute(statement, {"faculty": faculty}).mappings().all()


@router.get("/{student_number}", response_model=StudentResponse)
def get_student_by_number(student_number: str, db: Session = Depends(get_db)):
    statement = text(
        "SELECT * FROM students WHERE student_number = :student_number"
    )
    student = db.execute(
        statement, {"student_number": student_number}
    ).mappings().first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Öğrenci bulunamadı.",
        )
    return student