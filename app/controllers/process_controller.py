from flask import jsonify
from app.models.process import Process
from app.utils.error_handler import APIError, error_response

def get_process_status(task_id):
    """Retrieve the status of a specific process by task ID"""
    try:
        if not task_id:
            raise APIError("Task ID is required", 400)

        process = Process.get_process_by_task_id(task_id)
        
        if process:
            return jsonify(process), 200
        else:
            raise APIError("Process not found", 404)

    except APIError as e:
        return error_response(e.message, e.status_code)
    except Exception as e:
        return error_response(f"Failed to retrieve process: {str(e)}", 500)

def get_all_processes():
    """Retrieve the status of all processes"""
    try:
        processes = Process.get_all_processes()

        if not processes:
            return jsonify({"message": "No processes found"}), 200
        
        return jsonify(processes), 200

    except Exception as e:
        return error_response(f"Failed to retrieve processes: {str(e)}", 500)
