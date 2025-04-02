from flask import Blueprint
from app.controllers.movie_controller import upload_csv, get_movies

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/upload', methods=['POST'])
def api_upload_csv():
    return upload_csv()

@movie_bp.route('/movies', methods=['GET'])
def api_get_movies():
    return get_movies()

