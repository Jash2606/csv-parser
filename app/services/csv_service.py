import os
import uuid
import re
import pyarrow as pa
import pyarrow.csv as csv
from datetime import datetime
from app.models.movie import Movie
from flask import current_app

def process_csv_file(file_path):
    """
    Process a CSV file using PyArrow and insert data into MongoDB
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        dict: Processing statistics
    """
    try:
        with current_app.app_context():
            print(f"Starting to process CSV file: {file_path}")
            
            # Define column types for efficient parsing
            column_types = {
                'homepage': pa.string(),
                'original_language': pa.string(),
                'original_title': pa.string(),
                'overview': pa.string(),
                'release_date': pa.string(),
                'revenue': pa.float64(),
                'runtime': pa.float32(),
                'status': pa.string(),
                'title': pa.string(),
                'vote_average': pa.float32(),
                'vote_count': pa.float32(),
                'production_company_id': pa.string(),
                'genre_id': pa.string(),
                'languages': pa.string()
            }

            # Read CSV with PyArrow for efficient processing
            read_options = csv.ReadOptions(block_size=1024 * 1024)  # 1MB chunks
            parse_options = csv.ParseOptions(delimiter=',')
            convert_options = csv.ConvertOptions(column_types=column_types)
            
            print("Reading CSV file with PyArrow...")
            table = csv.read_csv(file_path, read_options=read_options, parse_options=parse_options, convert_options=convert_options)
            
            print(f"CSV file read successfully. Total rows: {table.num_rows}")
            
            # Convert Arrow Table to list of dictionaries (batch processing)
            batch_size = 1000
            total_rows = table.num_rows
            processed_rows = 0
            inserted_count = 0
            
            for batch_start in range(0, total_rows, batch_size):
                batch_end = min(batch_start + batch_size, total_rows)
                batch = table.slice(batch_start, batch_end - batch_start)
                
                print(f"Processing batch {batch_start}-{batch_end} of {total_rows}")
                
                # Convert batch to Python dictionaries
                records = batch.to_pylist()
                
                # Process and transform each record
                movies = []
                for record in records:
                    # Clean and transform the record
                    movie = clean_movie_record(record)
                    if movie:  # Only add valid records
                        movies.append(movie)
                
                print(f"Cleaned {len(movies)} valid records in this batch")
                
                # Bulk insert the batch
                if movies:
                    inserted = Movie.bulk_insert(movies)
                    inserted_count += inserted
                    print(f"Inserted {inserted} records into MongoDB")
                
                processed_rows += (batch_end - batch_start)
                print(f"Progress: {processed_rows}/{total_rows} rows processed")
            
            # Ensure indexes are created for efficient querying
            print("Creating indexes...")
            Movie.create_indexes()
            
            result = {
                "success": True,
                "total_rows": total_rows,
                "processed_rows": processed_rows,
                "inserted_count": inserted_count
            }
            print(f"CSV processing completed: {result}")
            return result
    
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Temporary file removed: {file_path}")

def clean_movie_record(record):
    """
    Clean and transform a movie record from CSV
    
    Args:
        record: Dictionary representing a row from the CSV
        
    Returns:
        dict: Cleaned and transformed movie record
    """
    try:
        # Extract release date and convert to proper format
        release_date = None
        year = None
        
        if record.get('release_date'):
            try:
                release_date_obj = datetime.strptime(str(record['release_date']), '%Y-%m-%d')
                release_date = release_date_obj.isoformat()
                year = release_date_obj.year
            except ValueError:
                # If date parsing fails, try to extract just the year
                year_match = re.match(r'(\d{4})', str(record['release_date']))
                if year_match:
                    year = int(year_match.group(1))
                    release_date = f"{year}-01-01T00:00:00"

        # Build the cleaned record
        movie = {
            "homepage": record.get('homepage', ''),
            "original_language": record.get('original_language', ''),
            "original_title": record.get('original_title', ''),
            "overview": record.get('overview', ''),
            "release_date": release_date,
            "year": year,
            "revenue": record.get('revenue', 0),
            "runtime": record.get('runtime', 0),
            "status": record.get('status', ''),
            "title": record.get('title', ''),
            "vote_average": record.get('vote_average', 0.0),
            "vote_count": record.get('vote_count', 0),
            "production_company_id": record.get('production_company_id', ''),
            "genre_id": record.get('genre_id', ''),
            "languages": record.get('languages', '').split(',') if record.get('languages') else []
        }
        
        # Only return records with at least a title
        if movie['title']:
            return movie
        return None
    
    except Exception as e:
        print(f"Error cleaning record: {str(e)}")
        return None

def save_uploaded_file(file):
    """
    Save an uploaded file to a temporary location
    
    Args:
        file: Flask file object from request.files
        
    Returns:
        str: Path to the saved file
    """
    # Generate a unique filename
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(os.environ.get('UPLOAD_FOLDER', 'temp_uploads'), filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save the file
    file.save(file_path)
    print(f"File saved to temporary location: {file_path}")
    
    return file_path
