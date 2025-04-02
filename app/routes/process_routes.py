from flask import Blueprint
from app.controllers.process_controller import get_process_status, get_all_processes


process_bp = Blueprint('process', __name__)

@process_bp.route('/process/<task_id>', methods=['GET'])
def api_get_process_status(task_id):
    return get_process_status(task_id)
    

@process_bp.route('/processes', methods=['GET'])
def api_get_all_processes():
   return get_all_processes()