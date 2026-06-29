from fastapi import FastAPI

from app.api.chat_router import router as chat_router

app = FastAPI(
    title="AI Core",
    version="0.1.0",
    description="Core platform for AI-powered applications."
)

app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Core",
        "status": "running"
    }