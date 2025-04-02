# IMDb Content Upload and Review System

A Flask-based web application for uploading, processing, and exploring IMDb movie data with asynchronous task processing using ZeroMQ.

## Features

- CSV file upload and processing with PyArrow for efficient parsing
- Asynchronous task processing with ZeroMQ
- MongoDB data storage with efficient indexing
- Redis caching with 5-second TTL
- RESTful API with proper error handling
- Process tracking and monitoring
- Handles CSV files up to 1GB with ease thanks to batch processing and efficient PyArrow implementation

## Prerequisites

- Python 3.9+
- MongoDB
- Redis
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Jash2606/csv-parser.git
   cd csv-parser
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   FLASK_APP=run.py
   DEBUG=True
   MONGO_URI=your_mongo_uri
   MONGO_DB=imdb_content
   REDIS_URL=redis://localhost:6379
   HOST=127.0.0.1
   PORT=5000
   UPLOAD_FOLDER=uploads
   ZMQ_HOST=127.0.0.1
   ZMQ_PORT=5557
   ```

## Running the Application

1. Start Redis server:
   ```
   # If using Redis locally
   redis-server
   
   # If using Docker
   docker run -p 6379:6379 --name redis-server -d redis
   ```

2. Start the Flask application:
   ```
   python run.py
   ```

3. Start the ZeroMQ worker in a separate terminal:
   ```
   python worker.py
   ```

## API Endpoints

### Upload CSV File
```
POST /api/v1/upload
```
- Request: Form data with 'file' field containing a CSV file
- Response: JSON with task ID for tracking

### Get Movies
```
GET /api/v1/movies
```
Query parameters:
- `page` (default: 1): Page number
- `limit` (default: 10, max: 100): Items per page
- `year`: Filter by release year
- `language`: Filter by original language
- `sort_by` (default: 'release_date'): Field to sort by (options: 'release_date', 'rating', 'title')
- `order` (default: 1): Sort order (1 for ascending, -1 for descending)

### Get Process Status
```
GET /api/v1/process/
```
Returns the status of a specific process.

### Get All Processes
```
GET /api/v1/processes
```
Returns all processes with their statuses.

## Technologies Used

- **Flask**: Web framework for building the API
- **PyMongo**: MongoDB driver for Python
- **PyArrow**: High-performance CSV parsing and data manipulation
- **ZeroMQ**: Asynchronous messaging library for task processing
- **Redis**: In-memory data store for caching
- **Python-dotenv**: Environment variable management

## Error Handling

The application uses a centralized error handling system with custom APIError class for consistent error responses across all endpoints.

## Performance Optimizations

- Batch processing of CSV data using PyArrow
- MongoDB indexing for efficient queries
- Redis caching with 5-second TTL to reduce database load
- Asynchronous task processing for handling large CSV files

