from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.database import engine, Base
from app.routers import rooms, bookings, rentals, statistics

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hotel Management System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(rentals.router)
app.include_router(statistics.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
