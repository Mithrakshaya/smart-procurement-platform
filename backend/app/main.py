from fastapi import FastAPI

app = FastAPI(
    title="GrainFlow Smart Procurement Platform",
    description="AI-powered smart procurement and queue management system",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "GrainFlow API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}