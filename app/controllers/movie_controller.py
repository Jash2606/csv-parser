from flask import jsonify, request
from app.models.movie import Movie
from app.services.csv_service import save_uploaded_file
from app.services.cache_service import get_cached_movies, cache_movies_response
from app.zmq_instance import get_push_socket
from app.tasks import serialize_task
from app.utils.error_handler import APIError, error_response

def upload_csv():
    """Handle CSV file upload and processing"""
    try:
        if 'file' not in request.files:
            raise APIError("No file part", 400)
        
        file = request.files['file']
        if file.filename == '':
            raise APIError("No selected file", 400)
        
        if not file.filename.endswith('.csv'):
            raise APIError("File must be a CSV", 400)
        
        file_path = save_uploaded_file(file)
        task_data, task_id = serialize_task('process_csv_task', file_path=file_path)
        
        socket = get_push_socket()
        socket.send_json(task_data)
        
        return jsonify({
            "message": "File uploaded successfully and queued for processing",
            "task_id": task_id
        }), 202
    except APIError as e:
        return error_response(e.message, e.status_code)
    except Exception as e:
        return error_response("Internal Server Error: " + str(e), 500)

def get_movies():
    """Get movies with pagination, filtering, and sorting"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        year = request.args.get('year')
        language = request.args.get('language')
        sort_by = request.args.get('sort_by', 'release_date')
        order = request.args.get('order', 1, type=int)
        
        if page < 1:
            raise APIError("Page number must be 1 or greater", 400)
        if limit < 1 or limit > 100:
            raise APIError("Limit must be between 1 and 100", 400)
        if sort_by not in ['release_date', 'rating', 'title']:
            raise APIError("Invalid sort_by value", 400)
        if order not in [1, -1]:
            raise APIError("Order must be 1 (ascending) or -1 (descending)", 400)
        
        cached_response = get_cached_movies(page, limit, year, language, sort_by, order)
        if cached_response:
            return jsonify(cached_response), 200
        
        result = Movie.get_movies(page, limit, year, language, sort_by, order)
        cache_movies_response(result, page, limit, year, language, sort_by, order)
        
        return jsonify(result), 200
    except APIError as e:
        return error_response(e.message, e.status_code)
    except Exception as e:
        return error_response("Internal Server Error: " + str(e), 500)
