from pydantic import BaseModel


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    student_number: str
    faculty: str
    major: str
    class_year: int = 1


class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True