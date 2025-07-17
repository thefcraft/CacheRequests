# cached_requests

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/thefcraft/cached_requests)
[![PyPI version](https://badge.fury.io/py/cached_requests.svg)](https://badge.fury.io/py/cached_requests)

cached_requests is a Python library that provides a simple and effective caching layer for your web requests. It's built on top of the popular `requests` library and is designed to be a drop-in replacement for `requests.Session`.

## Features

*   **Persistent Caching:** Save responses to disk to speed up repeated requests.
*   **Automatic Cache Invalidation:** Set a time-to-live (TTL) for your cached responses.
*   **Customizable:** Configure cache directories, refresh policies, and more.
*   **Easy to Use:** A simple, intuitive API that gets out of your way.

## Installation

Install CacheFlow using pip:

```bash
pip install cached_requests
```

## Quick Start

Here's a simple example of how to use cached_requests:

```python
from cached_requests import CacheSession
from datetime import timedelta

# Create a new session with a cache directory
requests = CacheSession(cache_dir='.cache', refresh_after=timedelta(hours=1)) # or use `from cached_requests import requests`

# Make a request
response = requests.get('https://api.github.com')

# The response is now cached. Subsequent requests to the same URL will be served from the cache.
cached_response = requests.get('https://api.github.com')

print(response.json())
```

## Advanced Usage

### Configuration

You can configure the behavior of cached_requests by passing arguments to the `CacheSession` constructor:

*   `cache_dir`: The directory where cached responses will be stored.
*   `force_refresh`: If `True`, the cache will be ignored and all requests will be made to the network.
*   `refresh_after`: A `timedelta` object that specifies how long a cached response is valid.
*   `refresh_on_error`: If `True`, the cache will be refreshed if a cached response resulted in an error.

### Context Manager

You can also use a context manager to temporarily change the configuration:

```python
with requests.configure(force_refresh=True):
    # This request will bypass the cache
    response = requests.get('https://api.github.com')
```

## Deleting Cache Entries

CacheFlow provides multiple ways to manage your cache.

### Deleting by URL

You can delete cache entries based on a URL pattern:

```python
from cached_requests import delete_cache_by_function
def should_delete(url: str):
    return 'github.com' in url

delete_cache_by_function(requests, should_delete)
```
### Deleting by Expiration

You can delete cache entries that are older than a specified timedelta:

```python
from cached_requests import delete_cache_by_expiration
from datetime import timedelta
# Delete all cache entries older than 7 days
delete_cache_by_expiration(requests, timedelta(days=7))
```


## Contributing

Contributions are welcome! If you have a feature request, bug report, or pull request, please open an issue on GitHub.

## License

cached_requests is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.