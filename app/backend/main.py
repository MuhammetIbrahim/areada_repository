from fastapi import FastAPI
from core.settings import settings

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

@app.get("/")
async def root():
    return {"message": "AREADERA API is running!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database_connected": True,
        "redis_connected": True
    }

@app.post("/upload")
async def upload_book():
    return {"message": "Book upload endpoint - will be implemented"}

@app.get("/books/{book_id}/status")
async def get_book_status(book_id: int):
    return {
        "book_id": book_id,
        "status": "processing",
        "progress": 45
    }

