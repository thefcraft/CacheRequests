from requests import Response, HTTPError

from uuid import uuid4
from datetime import timedelta, datetime, timezone

from typing import Callable, Protocol
from pickle import UnpicklingError
from .urlmap import UrlMap
from .path import Path
from .response import CacheResponse
class CacheSessionProtocol(Protocol):  
    @property
    def url_map(self) -> UrlMap: ...
    @property
    def cache_dir(self) -> Path: ...
    def dump_url_map(self): ...

def uuid() -> str:
    return uuid4().hex

def raise_for_redirect(response: Response):
    """Raises HTTPError if the response is a redirect."""
    if response.status_code in (301, 302, 303, 307, 308):
        location = response.headers.get("Location", "<no location>")
        error_msg = (
            f"{response.status_code} Redirect Error: {response.reason} "
            f"to {location} for url: {response.url}"
        )
        raise HTTPError(error_msg, response=response)

def delete_cache_by_expiration(session: CacheSessionProtocol, ex: timedelta) -> None:
        """
        Deletes all cache entries older than the specified timeout.

        Args:
            ex (timedelta): The maximum age of a cache entry before it is deleted.
        """
        now = datetime.now(timezone.utc)
        urls_to_delete: list[str] = []
        for url, filename in session.url_map.items():
            filepath = session.cache_dir @ filename
            if filepath.exists():
                try:
                    cached_response = CacheResponse.load(filepath)
                    if now - cached_response.timestamp > ex:
                        urls_to_delete.append(url)
                except (UnpicklingError, EOFError):
                    # Handle cases where the cache file is corrupted or empty
                    urls_to_delete.append(url)
            else:
                urls_to_delete.append(url)
        for url in urls_to_delete:
            session.url_map.delitem(url, session.cache_dir)
        
        session.dump_url_map()
def delete_cache_by_function(session: CacheSessionProtocol, isDeleteUrl: Callable[[str], bool]) -> None:
    urls_to_delete: list[str] = []
    for url, filename in session.url_map.items():  
        filepath = session.cache_dir @ filename
        if filepath.exists() and isDeleteUrl(url): 
            urls_to_delete.append(url)
        else:
            urls_to_delete.append(url)
    for url in urls_to_delete:
        session.url_map.delitem(url, session.cache_dir)
    session.dump_url_map()