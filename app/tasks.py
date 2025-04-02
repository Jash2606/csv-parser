import os
import uuid
from app.services.csv_service import process_csv_file
from app.models.process import Process

def serialize_task(task_name, **kwargs):
    """
    Serialize a task to JSON for ZeroMQ transport
    """
    task_id = str(uuid.uuid4())

    Process.create_process(task_id, status='pending')
    return {
        'task_id': task_id,
        'task': task_name,
        'kwargs': kwargs
    }, task_id

def process_csv_task(file_path,task_id):
    """
    Process a CSV file and return the results
    """
    try:
        Process.update_status( 'processing' , task_id)
        result = process_csv_file(file_path)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        return result
    except Exception as e:

        Process.update_status( 'failed' , task_id)

        if os.path.exists(file_path):
            os.remove(file_path)
        return {'success': False, 'error': str(e)}
