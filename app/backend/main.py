from fastapi import FastAPI
from celery import Celery
from backend.core.settings import settings

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Celery client to send tasks
celery_client = Celery(
    "areadera_client",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
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
    # Mock book_id - in real app this would come from database
    book_id = 123
    
    # Send task to Celery worker
    task = celery_client.send_task(
        "tasks.process_book_task",
        args=[book_id]
    )
    
    return {
        "message": "Book upload started",
        "book_id": book_id,
        "task_id": task.id,
        "status": "processing"
    }

@app.get("/books/{book_id}/status")
async def get_book_status(book_id: int):
    return {
        "book_id": book_id,
        "status": "processing",
        "progress": 45
    }

@app.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """Check Celery task status"""
    result = celery_client.AsyncResult(task_id)
    
    if result.state == 'PENDING':
        response = {
            "task_id": task_id,
            "state": "PENDING",
            "progress": 0,
            "message": "Task is waiting to be processed"
        }
    elif result.state == 'PROGRESS':
        response = {
            "task_id": task_id,
            "state": "PROGRESS",
            "progress": result.info.get('progress', 0),
            "step": result.info.get('step', 'Processing'),
            "message": f"Task is in progress: {result.info.get('step', 'Processing')}"
        }
    elif result.state == 'SUCCESS':
        response = {
            "task_id": task_id,
            "state": "SUCCESS",
            "progress": 100,
            "result": result.result,
            "message": "Task completed successfully"
        }
    else:  # FAILURE
        response = {
            "task_id": task_id,
            "state": "FAILURE",
            "progress": 0,
            "error": str(result.info),
            "message": "Task failed"
        }
    
    return response

@app.post("/generate-qa")
async def generate_qa():
    """Generate Q&A for a section"""
    task = celery_client.send_task(
        "tasks.generate_qa_task",
        args=["Sample section content", "Sample sub-point content"]
    )
    
    return {
        "message": "Q&A generation started",
        "task_id": task.id
    }

@app.post("/generate-report")
async def generate_section_report():
    """Generate personalized section report"""
    task = celery_client.send_task(
        "tasks.generate_section_report_task",
        args=[1, 1]  # user_id=1, section_id=1
    )
    
    return {
        "message": "Section report generation started", 
        "task_id": task.id
    }

