from fastapi import FastAPI
from app.modules.booking.router import router as booking_router

app = FastAPI(
    title="GrainFlow Smart Procurement Platform",
    description="AI-powered smart procurement and queue management system",
    version="1.0.0"
)

app.include_router(booking_router)

@app.get("/")
def root():
    return {"message": "GrainFlow API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}