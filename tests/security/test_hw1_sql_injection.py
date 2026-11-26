import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Student
from app.registration import get_students_by_faculty


class FacultySearchSecurityTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        self.session.add_all(
            [
                Student(
                    first_name="Fake",
                    last_name="Engineering",
                    student_number="TEST-ENG",
                    faculty="Faculty of Engineering",
                    major="Test Major",
                    class_year=1,
                ),
                Student(
                    first_name="Fake",
                    last_name="Science",
                    student_number="TEST-SCI",
                    faculty="Faculty of Science",
                    major="Test Major",
                    class_year=1,
                ),
            ]
        )
        self.session.commit()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_normal_faculty_search_returns_only_matching_rows(self):
        results = get_students_by_faculty("Faculty of Engineering", self.session)

        self.assertEqual([row["student_number"] for row in results], ["TEST-ENG"])

    def test_sql_syntax_in_faculty_is_treated_as_literal_data(self):
        results = get_students_by_faculty(
            "Faculty of Engineering' OR 'x'='y", self.session
        )

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()