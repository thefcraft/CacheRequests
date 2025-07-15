from .session import CacheSession
from .path import Path
from .utils import delete_cache_by_function, delete_cache_by_expiration
            
requests: CacheSession = CacheSession()

__all__ = [
    'Path',
    'requests', 
    'CacheSession',
    'delete_cache_by_function',
    'delete_cache_by_expiration'
]