import os
from flask import Flask
from flask_caching import Cache
from dotenv import load_dotenv
from app.config import Config
import redis


load_dotenv()

cache = Cache()

os.makedirs(os.getenv('UPLOAD_FOLDER' , 'uploads'), exist_ok=True)

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    
    try:
        redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'])
        redis_ping = redis_client.ping()
        print(f"Redis connection successful: {redis_ping}")
    except Exception as e:
        print(f"Redis connection failed: {str(e)}")

    cache.init_app(app)
    app.cache = cache 
    
    from app.database import init_db
    init_db(app)
    
    from app.routes.movie_routes import movie_bp
    from app.routes.process_routes import process_bp
    app.register_blueprint(movie_bp, url_prefix='/api/v1')
    app.register_blueprint(process_bp, url_prefix='/api/v1')
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting app...")
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
    
