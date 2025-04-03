# IMDb Content Upload and Review System

A Flask-based web application for uploading, processing, and exploring IMDb movie data with asynchronous task processing using ZeroMQ.

## 🚀 Features

✅ **CSV file upload & processing** using **PyArrow** for efficient parsing  
✅ **Asynchronous task processing** with **ZeroMQ**  
✅ **MongoDB storage** with optimized indexing  
✅ **Redis caching** with a **5-second TTL** to speed up responses  
✅ **RESTful API** with structured **error handling**  
✅ **Process tracking & monitoring** for better visibility  
✅ **Handles large CSV files (up to 1GB)** efficiently with batch processing  

---

## 🛠️ Prerequisites

Before running the application, make sure you have:

- **Python** 3.9+
- **MongoDB** (local or cloud)
- **Redis** (for caching)
- **Virtual environment** (recommended)

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Jash2606/csv-parser.git
cd csv-parser
```

### 2️⃣ Create and Activate a Virtual Environment
```sh
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a **`.env` file** in the project root and add the following:
```ini
FLASK_APP=run.py
DEBUG=False
MONGO_URI=your_mongo_uri
MONGO_DB=imdb_content
REDIS_URL=redis://localhost:6379
HOST=0.0.0.0  # Use 0.0.0.0 for external access
PORT=5000
UPLOAD_FOLDER=uploads
ZMQ_HOST=127.0.0.1  # Change if using a remote worker
ZMQ_PORT=5557
```

---

## ▶️ Running the Application

### 1️⃣ Start the Redis Server
```sh
# If using Redis locally
redis-server

# If using Docker
docker run -p 6379:6379 --name redis-server -d redis
```

### 2️⃣ Start the Flask API
```sh
python run.py
```

### 3️⃣ Start the ZeroMQ Worker (in a separate terminal)
```sh
python worker.py
```

---

## 🔥 API Endpoints

### 📌 **Upload CSV File**
```http
POST /api/v1/upload
```
**Request:** Form data with a 'file' field containing a CSV file.  
**Response:**
```json
{
  "message": "File uploaded successfully and queued for processing",
  "task_id": "2fcc9e10-5c30-4746-bfc4-591ef0108f95"
}
```

### 📌 **Check Process Status**
```http
GET /api/v1/process/
```
**Example:** `GET /api/v1/process/2fcc9e10-5c30-4746-bfc4-591ef0108f95`  
**Response:**
```json
{
  "_id": "67ed6f9b0b51ce746e0e3cbb",
  "created_at": "Wed, 02 Apr 2025 22:40:51 GMT",
  "status": "pending",
  "task_id": "2fcc9e10-5c30-4746-bfc4-591ef0108f95",
  "updated_at": "Wed, 02 Apr 2025 22:40:51 GMT"
}
```

### 📌 **Get Movies**
```http
GET /api/v1/movies
```
| Parameter  | Description |
|------------|-------------|
| `page` (default: 1) | Page number |
| `limit` (default: 10, max: 100) | Items per page |
| `year` | Filter by release year |
| `language` | Filter by language |
| `sort_by` (default: `release_date`) | Options: `release_date`, `rating`, `title` |
| `order` (default: 1) | Sort order (1 = ascending, -1 = descending) |

**Example with filters:** `GET /api/v1/movies?page=10&limit=20&year=1990&language=en&sort_by=rating&order=-1`

**Response:**
```json
{
  "limit": 20,
  "movies": [
    {
      "_id": "67ed536ee12df977c71ca84a",
      "genre_id": "35",
      "homepage": "",
      "languages": ["English"],
      "original_language": "en",
      "original_title": "Life Is Sweet",
      "overview": "Just north of London live Wendy, Andy, and their twenty-something twins, Natalie and Nicola. Wendy clerks in a shop, leads aerobics at a primary school, jokes like a vaudevillian, agrees to waitress at a friend's new restaurant and dotes on Andy, a cook who forever puts off home remodeling projects, and with a drunken friend, buys a broken down lunch wagon. Natalie, with short neat hair and a snappy, droll manner, is a plumber; she has a holiday planned in America, but little else. Last is Nicola, odd man out: a snarl, big glasses, cigarette, mussed hair, jittery fingers, bulimic, jobless, and unhappy. How they interact and play out family conflict and love is the film's subject.",
      "production_company_id": "9210",
      "release_date": "1990-11-15T00:00:00",
      "revenue": 0,
      "runtime": 103,
      "status": "Released",
      "title": "Life Is Sweet",
      "vote_average": 6.9,
      "vote_count": 46,
      "year": 1990
    }
  ],
  "page": 10,
  "total_docs": 969,
  "total_pages": 49
}
```

### 📌 **Get All Processes**
```http
GET /api/v1/processes
```
**Response:** 
```json
[
  {
    "_id": "67ed6f9c643efa0d13005f7a",
    "created_at": "Wed, 02 Apr 2025 22:40:52 GMT",
    "status": "processing",
    "task_id": "2fcc9e10-5c30-4746-bfc4-591ef0108f95",
    "updated_at": "Wed, 02 Apr 2025 22:40:52 GMT"
  },
  {
    "_id": "67ed6f9b0b51ce746e0e3cbb",
    "created_at": "Wed, 02 Apr 2025 22:40:51 GMT",
    "status": "completed",
    "task_id": "2fcc9e10-5c30-4746-bfc4-591ef0108f95",
    "updated_at": "Wed, 02 Apr 2025 22:44:32 GMT"
  },
  {
    "_id": "67ed6681643efa0d13ffae04",
    "created_at": "Wed, 02 Apr 2025 22:02:01 GMT",
    "status": "processing",
    "task_id": "d477fc29-2057-43bc-8dab-302abf2fd4b5",
    "updated_at": "Wed, 02 Apr 2025 22:02:01 GMT"
  }
]
```

---

## 📊 Handling Large CSV Files

Our system efficiently processes large CSV files up to 1GB through several optimizations:

1. **Streaming Processing**: Instead of loading the entire file into memory, we read the CSV in small chunks (1MB blocks). This keeps memory usage low even for very large files.

2. **Batch Processing**: We process records in batches of 1000 rows. This balances memory usage and processing speed, allowing efficient handling of large datasets.

3. **PyArrow Integration**: We use PyArrow's high-performance CSV parsing capabilities, which are significantly faster than traditional CSV parsers.

4. **Asynchronous Processing**: Large file processing happens in a separate worker process using ZeroMQ. This keeps the web server responsive to other requests while processing occurs in the background.

5. **MongoDB Bulk Operations**: We insert processed records into MongoDB using bulk operations, reducing database overhead and speeding up the insertion process.

6. **Progress Tracking**: The system maintains processing status in the database, allowing clients to monitor progress of large file uploads through the API.

This architecture allows the system to handle CSV files up to 1GB and potentially beyond without overwhelming system resources, providing an efficient solution for processing large datasets.

---

## 🛠️ Technologies Used

- **Flask** - Web framework for building APIs
- **PyMongo** - MongoDB driver for Python
- **PyArrow** - High-performance CSV parsing and data handling
- **ZeroMQ** - Asynchronous messaging for background task processing
- **Redis** - In-memory caching to reduce database queries
- **Python-dotenv** - Environment variable management

---

## ❗ Error Handling

The application uses a **centralized error handling system** with a custom `APIError` class for consistent error responses.

---

## ⚡ Performance Optimizations

✔️ **Batch processing** of CSV data using **PyArrow**  
✔️ **MongoDB indexing** for faster queries  
✔️ **Redis caching** to minimize database load  
✔️ **Asynchronous task processing** for handling large CSV files efficiently  

---

## 📌 Future Improvements
- ✅ Implement **Redis Queue (RQ) / Celery** instead of ZeroMQ for better task handling.
- ✅ Add **JWT Authentication** for secure API access.
- ✅ Improve **batch processing** to handle even larger files efficiently.

---
