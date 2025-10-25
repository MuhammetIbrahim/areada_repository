from celery import Celery
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pydantic_settings import BaseSettings

class WorkerSettings(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    class Config:
        env_file = "../.env"

settings = WorkerSettings()

celery_app = Celery(
    "areadera_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["tasks"]
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True)
def process_book_task(self, book_id: int):
    """
    Main task for processing uploaded books
    """
    try:
        print(f"Processing book {book_id}")
        
        # Step 1: PDF Analysis
        print("Step 1: Analyzing PDF structure...")
        self.update_state(state='PROGRESS', meta={'progress': 10, 'step': 'PDF Analysis'})
        
        # Step 2: Text Extraction/OCR
        print("Step 2: Extracting text...")
        self.update_state(state='PROGRESS', meta={'progress': 30, 'step': 'Text Extraction'})
        
        # Step 3: Chunking with LlamaIndex
        print("Step 3: Creating chunks with context windows...")
        self.update_state(state='PROGRESS', meta={'progress': 60, 'step': 'Text Chunking'})
        
        # Step 4: Vectorization and Storage
        print("Step 4: Creating embeddings and storing in Qdrant...")
        self.update_state(state='PROGRESS', meta={'progress': 80, 'step': 'Vectorization'})
        
        # Step 5: Mark as Ready
        print("Step 5: Marking book as ready...")
        self.update_state(state='PROGRESS', meta={'progress': 100, 'step': 'Completed'})
        
        return {
            'status': 'SUCCESS',
            'message': f'Book {book_id} processed successfully',
            'book_id': book_id
        }
        
    except Exception as exc:
        print(f"Error processing book {book_id}: {str(exc)}")
        self.update_state(
            state='FAILURE',
            meta={'error': str(exc), 'book_id': book_id}
        )
        raise exc

@celery_app.task
def generate_qa_task(section_content: str, sub_point_content: str):
    """
    Task for generating Q&A for sub-points
    """
    try:
        print(f"Generating Q&A for sub-point...")
        
        # Mock Q&A generation - will be replaced with actual LLM calls
        qa_data = {
            "question": "Sample question based on content?",
            "correct_answer": "Sample correct answer",
            "wrong_answers": [
                "Wrong answer 1",
                "Wrong answer 2", 
                "Wrong answer 3"
            ],
            "lookup_text": sub_point_content[:100]
        }
        
        return qa_data
        
    except Exception as exc:
        print(f"Error generating Q&A: {str(exc)}")
        raise exc

@celery_app.task
def generate_section_report_task(user_id: int, section_id: int):
    """
    Task for generating personalized section reports
    """
    try:
        print(f"Generating section report for user {user_id}, section {section_id}")
        
        # Mock report generation - will be replaced with actual LLM calls
        report = {
            "user_id": user_id,
            "section_id": section_id,
            "strengths": ["Good understanding of basic concepts"],
            "weaknesses": ["Struggled with advanced topics"],
            "recommendations": ["Review chapter 3 examples", "Practice more problems"],
            "next_steps": "Ready to proceed to next section"
        }
        
        return report
        
    except Exception as exc:
        print(f"Error generating section report: {str(exc)}")
        raise exc

if __name__ == "__main__":
    celery_app.start()