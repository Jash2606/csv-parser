from app.database import get_db

class Movie:
    @classmethod
    def get_collection(cls):
        """Get the MongoDB collection for movies"""
        db = get_db()
        return db.movies
    
    @classmethod
    def create_indexes(cls):
        """Create necessary indexes for efficient querying"""
        collection = cls.get_collection()
        collection.create_index([("release_date", 1)])
        collection.create_index([("vote_average", -1)])
        collection.create_index([("revenue", -1)])
        collection.create_index([("original_language", 1)])
        collection.create_index([("year", 1)])
    
    @classmethod
    def bulk_insert(cls, movies):
        """Insert multiple movie documents"""
        if not movies:
            return 0
        
        collection = cls.get_collection()
        result = collection.insert_many(movies)
        return len(result.inserted_ids)
    
    @classmethod
    def get_movies(cls, page=1, limit=10, year=None, language=None, sort_by="release_date", order=1):
        """Get movies with pagination, filtering and sorting"""
        collection = cls.get_collection()
        
        query = {}
        if year:
            query["year"] = int(year)
        if language:
            query["original_language"] = language
        
        sort_field = sort_by
        sort_direction = int(order)  
        
        skip = (page - 1) * limit
        
        cursor = collection.find(query).sort(sort_field, sort_direction).skip(skip).limit(limit)
        
        total_docs = collection.count_documents(query)
        total_pages = (total_docs + limit - 1) // limit  

        movies = []
        for movie in cursor:
            movie['_id'] = str(movie['_id']) 
            movies.append(movie)
        
        return {
            "movies": movies,
            "page": page,
            "limit": limit,
            "total_docs": total_docs,
            "total_pages": total_pages
        }
    
    @classmethod
    def get_languages(cls):
        """Get unique languages in the collection"""
        collection = cls.get_collection()
        return collection.distinct("original_language")
    
    @classmethod
    def get_years(cls):
        """Get unique years in the collection"""
        collection = cls.get_collection()
        return sorted(collection.distinct("year"))
