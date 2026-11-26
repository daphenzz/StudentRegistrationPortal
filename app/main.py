from fastapi import FastAPI
from app.database import Base, engine, ensure_class_year_column
from app.registration import router as registration_router

# Veritabanında students tablosu yoksa otomatik oluşturur
Base.metadata.create_all(bind=engine)
ensure_class_year_column()

app = FastAPI(
    title="Öğrenci Kayıt Sistemi API",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.include_router(registration_router)


@app.get("/")
def root():
    return {"message": "Öğrenci Kayıt Sistemi çalışıyor."}