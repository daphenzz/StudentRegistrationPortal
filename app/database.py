import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def ensure_class_year_column():
    inspector = inspect(engine)
    if "students" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("students")}
    with engine.begin() as connection:
        if "class_year" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE students "
                    "ADD COLUMN class_year INTEGER NOT NULL DEFAULT 1"
                )
            )
        if "released" in columns:
            connection.execute(text("ALTER TABLE students DROP COLUMN released"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()