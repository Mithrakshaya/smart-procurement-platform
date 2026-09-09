from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.dashboard.routes import router as dashboard_router

app = FastAPI(
    title="GrainFlow Smart Procurement Platform",
    description="AI-powered smart procurement and queue management system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"message": "GrainFlow API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}