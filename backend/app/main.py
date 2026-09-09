from fastapi import FastAPI

from backend.app.modules.farmer.router import router as farmer_router
from backend.app.db.database import Base, engine
from backend.app.modules.booking.router import router as booking_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GrainFlow Smart Procurement Platform",
    description="AI-powered smart procurement and queue management system",
    version="1.0.0"
)

app.include_router(farmer_router)
app.include_router(booking_router)


@app.get("/")
def root():
    return {"message": "GrainFlow API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}