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
**Response:** JSON with task ID for tracking.

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

### 📌 **Get Process Status**
```http
GET /api/v1/process/<task_id>
```
Returns the **status** of a specific process.

### 📌 **Get All Processes**
```http
GET /api/v1/processes
```
Returns **all processes** with their statuses.

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