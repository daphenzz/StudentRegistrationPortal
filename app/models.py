from sqlalchemy import Column, Integer, String
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    student_number = Column(String(20), unique=True, index=True, nullable=False)
    faculty = Column(String(150), nullable=False)
    major = Column(String(150), nullable=False)
    class_year = Column(Integer, nullable=False, default=1, server_default="1")