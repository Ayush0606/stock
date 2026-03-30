"""
Caching utility for API responses
Implements simple in-memory caching with TTL
"""
import time
from functools import wraps
from typing import Any, Callable, Optional
import logging

logger = logging.getLogger(__name__)


class Cache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.cache = {}
        self.ttl_map = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in cache with optional TTL"""
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        ttl = ttl or self.default_ttl
        self.cache[key] = value
        self.ttl_map[key] = time.time() + ttl
        logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache, returns None if expired or not found"""
        if key not in self.cache:
            return None
        
        # Check if expired
        if time.time() > self.ttl_map.get(key, 0):
            self._delete(key)
            logger.debug(f"Cache MISS (expired): {key}")
            return None
        
        logger.debug(f"Cache HIT: {key}")
        return self.cache[key]
    
    def delete(self, key: str) -> None:
        """Delete a value from cache"""
        self._delete(key)
    
    def _delete(self, key: str) -> None:
        """Internal delete"""
        self.cache.pop(key, None)
        self.ttl_map.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
        self.ttl_map.clear()
        logger.info("Cache cleared")
    
    def _evict_oldest(self) -> None:
        """Remove oldest item when cache is full"""
        if self.cache:
            oldest_key = min(self.ttl_map.keys(), key=lambda k: self.ttl_map[k])
            self._delete(oldest_key)
            logger.debug(f"Cache evicted: {oldest_key}")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl_entries": len(self.ttl_map),
            "utilization": f"{(len(self.cache)/self.max_size)*100:.2f}%"
        }


# Global cache instance
_cache = Cache()


def cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate cache key from prefix and arguments"""
    args_str = "_".join(str(arg) for arg in args)
    kwargs_str = "_".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
    if args_str and kwargs_str:
        return f"{prefix}:{args_str}:{kwargs_str}"
    elif args_str:
        return f"{prefix}:{args_str}"
    elif kwargs_str:
        return f"{prefix}:{kwargs_str}"
    else:
        return prefix


def cached(prefix: str, ttl: Optional[int] = None):
    """
    Decorator to cache function results
    
    Usage:
        @cached("stock_data", ttl=3600)
        def get_stock_data(symbol):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            result = _cache.get(key)
            if result is not None:
                return result
            
            # Cache miss, call function
            result = func(*args, **kwargs)
            
            # Store in cache
            if result is not None:
                _cache.set(key, result, ttl)
            
            return result
        
        return wrapper
    
    return decorator


def invalidate_cache(pattern: Optional[str] = None) -> None:
    """
    Invalidate cache entries matching pattern
    
    Examples:
        invalidate_cache("stock_data:INFY")  # Clear INFY cache
        invalidate_cache("stock_")           # Clear all stock_ prefixed
        invalidate_cache()                    # Clear all cache
    """
    if pattern is None:
        _cache.clear()
        return
    
    keys_to_delete = [k for k in _cache.cache.keys() if pattern in k]
    for key in keys_to_delete:
        _cache.delete(key)
    
    logger.info(f"Invalidated {len(keys_to_delete)} cache entries matching '{pattern}'")


def get_cache_stats() -> dict:
    """Get cache statistics"""
    return _cache.get_stats()


# Example usage:
"""
from app.utils.cache import cached, invalidate_cache

@cached("stock_summary", ttl=1800)
def get_stock_summary(symbol: str):
    # This result will be cached for 30 minutes
    return expensive_operation(symbol)

# Invalidate when data is refreshed
invalidate_cache("stock_")
"""
