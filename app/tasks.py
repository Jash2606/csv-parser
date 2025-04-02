import os
import uuid
from app.services.csv_service import process_csv_file
from app.models.process import Process
# from flask import current_app

def serialize_task(task_name, **kwargs):
    """
    Serialize a task to JSON for ZeroMQ transport
    """
    task_id = str(uuid.uuid4())
    # Create a new process entry in the database
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
        Process.update_status(file_path, 'processing')
        result = process_csv_file(file_path)
        # Clean up the file after processing
        if os.path.exists(file_path):
            os.remove(file_path)
        return result
    except Exception as e:
        # Update the process status to failed
        Process.update_status(file_path, 'failed')
        # Make sure to clean up even if processing fails\
        if os.path.exists(file_path):
            os.remove(file_path)
        return {'success': False, 'error': str(e)}
