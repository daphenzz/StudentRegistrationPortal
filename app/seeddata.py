from app.database import Base, SessionLocal, engine, ensure_class_year_column
from app.models import Student


def seed():
    Base.metadata.create_all(bind=engine)
    ensure_class_year_column()
    db = SessionLocal()

    sample_students = [
        Student(
            first_name="Ahmet",
            last_name="Yilmaz",
            student_number="20231001",
            faculty="Faculty of Engineering",
            major="Computer Engineering",
            class_year=1,
        ),
        Student(
            first_name="Zeynep",
            last_name="Kaya",
            student_number="20231002",
            faculty="Faculty of Engineering",
            major="Electrical and Electronics Engineering",
            class_year=2
        ),
        Student(

            first_name="Mehmet",
            last_name="Demir",
            student_number="20231003",
            faculty="Faculty of Science",
            major="Mathematics",
            class_year=3,
        ),
    ]

    try:
        for student in sample_students:
            exists = (
                db.query(Student)
                .filter(Student.student_number == student.student_number)
                .first()
            )
            if exists:
                exists.first_name = student.first_name
                exists.last_name = student.last_name
                exists.faculty = student.faculty
                exists.major = student.major
                exists.class_year = student.class_year
            else:
                db.add(student)
        db.commit()
        print("Seed data inserted successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()