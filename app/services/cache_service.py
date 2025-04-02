from flask import current_app

def get_movies_cache_key(page, limit, year, language, sort_by, order):
    """
    Generate a cache key for movies query
    
    Args:
        page: Page number
        limit: Items per page
        year: Filter by year
        language: Filter by language
        sort_by: Field to sort by
        order: Sort order (1 for ascending, -1 for descending)
        
    Returns:
        str: Cache key
    """
    return f"movies:page={page}:limit={limit}:year={year}:language={language}:sort_by={sort_by}:order={order}"

def cache_movies_response(response, page, limit, year, language, sort_by, order):
    """
    Cache a movies response
    
    Args:
        response: Response data to cache
        page, limit, year, language, sort_by, order: Query parameters
        
    Returns:
        The cached response
    """
    key = get_movies_cache_key(page, limit, year, language, sort_by, order)
    current_app.cache.set(key, response, timeout=5)
    return response

def get_cached_movies(page, limit, year, language, sort_by, order):
    """
    Get cached movies response if available
    
    Args:
        page, limit, year, language, sort_by, order: Query parameters
        
    Returns:
        Cached response or None if not in cache
    """
    key = get_movies_cache_key(page, limit, year, language, sort_by, order)
    return current_app.cache.get(key)
