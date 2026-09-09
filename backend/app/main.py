from fastapi import FastAPI
from backend.app.modules.farmer.router import router as farmer_router
from backend.app.db.database import Base, engine
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GrainFlow Smart Procurement Platform",
    description="AI-powered smart procurement and queue management system",
    version="1.0.0"
)
app.include_router(farmer_router)

@app.get("/")
def root():
    return {"message": "GrainFlow API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}