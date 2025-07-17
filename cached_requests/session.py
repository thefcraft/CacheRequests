import json
from requests import Session
from contextlib import contextmanager

from datetime import datetime, timedelta, timezone

from requests import Response
from .response import CacheResponse
from .urlmap import UrlMap
from .utils import uuid
from .path import Path

class _Default: ...
_DEFAULT = _Default()

class CacheSession(Session):
    def __init__(self, 
                 cache_dir: Path | str | None = None, 
                 force_refresh: bool = False, 
                 refresh_on_error: bool = False, 
                 dump_to_cache: bool = True,
                 overwrite_allow_redirects: bool | None = False,
                 refresh_after: timedelta | None = None) -> None:
        self.__force_refresh: bool = force_refresh
        self.__cache_dir: None | Path = Path(cache_dir).ensure_exists() if cache_dir is not None else None
        self.__dump_to_cache: bool = dump_to_cache
        self.__refresh_after: timedelta | None = refresh_after
        self.__refresh_on_error: bool = refresh_on_error
        self.__url_map: UrlMap | None = None
        self.__url_map_inv: UrlMap | None = None 
        self.__overwrite_allow_redirects: bool | None = overwrite_allow_redirects
        Session.__init__(self)
    def dump_url_map(self):
        urlmap = self.url_map
        with open(self.cache_dir @ 'url_map.json', 'w') as f:
            json.dump(urlmap, f) # BUG: i don't know why but here directly using self.url_map will may put empty file in disk on initial dump_url_map as self.url_map is None but why i don't know
    def load_url_map(self) -> UrlMap:
        if not (self.cache_dir @ 'url_map.json').exists():
            with open(self.cache_dir @ 'url_map.json', 'w') as f:
                json.dump(UrlMap(), f)
            return UrlMap()
        with open(self.cache_dir @ 'url_map.json', 'rb') as f:
            url_map: UrlMap = UrlMap(json.load(f))
        if len(url_map) > 10000:
            with open(self.cache_dir @ 'url_map.backup_10000.json', 'w') as f: json.dump(url_map, f)
        elif len(url_map) > 1000:
            with open(self.cache_dir @ 'url_map.backup_1000.json', 'w') as f: json.dump(url_map, f)
        elif len(url_map) > 100:
            with open(self.cache_dir @ 'url_map.backup_100.json', 'w') as f: json.dump(url_map, f)
        else:
            with open(self.cache_dir @ 'url_map.backup.json', 'w') as f: json.dump(url_map, f)
        return url_map
    @property
    def dump_to_cache(self) -> bool:
        return self.__dump_to_cache
    @property
    def cache_dir(self) -> Path:
        if self.__cache_dir is None:
            raise RuntimeError('please run inside with .configure(cachedir=...) block')
        return self.__cache_dir
    @property
    def force_refresh(self) -> bool:
        return self.__force_refresh
    @property
    def refresh_after(self) -> timedelta | None:
        return self.__refresh_after
    @property
    def refresh_on_error(self) -> bool:
        return self.__refresh_on_error
    @property
    def overwrite_allow_redirects(self) -> bool | None:
        return self.__overwrite_allow_redirects
    @property
    def url_map(self) -> UrlMap: 
        if self.__url_map is None:
            self.__url_map = self.load_url_map()
            self.__url_map_inv = self.__url_map.inverse()
        return self.__url_map
    @property
    def url_map_inv(self) -> UrlMap: 
        if self.__url_map_inv is None:
            self.__url_map = self.load_url_map()
            self.__url_map_inv = self.__url_map.inverse()
        return self.__url_map_inv
    
    
    @contextmanager
    def configure(self, 
        cache_dir: Path | str | None | _Default = _DEFAULT,
        force_refresh: bool | _Default = _DEFAULT,
        refresh_after: timedelta | None | _Default = _DEFAULT,
        refresh_on_error: bool | _Default = _DEFAULT,
        dump_to_cache: bool | _Default = _DEFAULT,
        overwrite_allow_redirects: bool | None | _Default = _DEFAULT,
    ):
        prev_cache_dir = self.__cache_dir
        prev_force_refresh = self.__force_refresh
        prev_refresh_after = self.__refresh_after
        prev_refresh_on_error = self.__refresh_on_error
        prev_dump_to_cache = self.__dump_to_cache
        prev_overwrite_allow_redirects = self.__overwrite_allow_redirects
        try:
            if not isinstance(cache_dir, _Default): self.__cache_dir = Path(cache_dir).ensure_exists() if cache_dir is not None else None
            if not isinstance(force_refresh, _Default): self.__force_refresh = force_refresh
            if not isinstance(refresh_after, _Default): self.__refresh_after = refresh_after
            if not isinstance(refresh_on_error, _Default): self.__refresh_on_error = refresh_on_error
            if not isinstance(dump_to_cache, _Default): self.__dump_to_cache = dump_to_cache
            if not isinstance(overwrite_allow_redirects, _Default): self.__overwrite_allow_redirects = overwrite_allow_redirects
            yield self
        finally:
            self.__cache_dir = prev_cache_dir
            self.__force_refresh = prev_force_refresh
            self.__refresh_after = prev_refresh_after
            self.__refresh_on_error = prev_refresh_on_error
            self.__dump_to_cache = prev_dump_to_cache
            self.__overwrite_allow_redirects = prev_overwrite_allow_redirects
    
    def request(
        self,
        method,
        url: str | bytes,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None
    ) -> CacheResponse:
        assert isinstance(url, str), f"Why providing bytes to request: {url=}"
        
        filepath: Path | None = None
        if not self.force_refresh or self.dump_to_cache:
            filepath = self.cache_dir @ self.url2filename(url=url)
        if not self.force_refresh and filepath and filepath.exists():
            cach_resp = CacheResponse.load(filepath)
            refresh_after = self.refresh_after
            if refresh_after:
                since = datetime.now(tz=timezone.utc) - cach_resp.timestamp
                if since < refresh_after and (
                    not self.refresh_on_error or cach_resp.ok
                ):
                    return cach_resp
            elif not self.refresh_on_error or cach_resp.ok:
                return cach_resp
    
        resp = Session.request(
            self=self,
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=(
                allow_redirects if self.overwrite_allow_redirects is None else 
                self.overwrite_allow_redirects
            ),
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json
        )
        if stream:
            _filepath: Path | None = None
            if self.dump_to_cache and filepath:
                _filepath = filepath
            cach_resp = CacheResponse.from_response(resp, dump_path=_filepath)
        else:
            cach_resp = CacheResponse.from_response(resp)
            if self.dump_to_cache and filepath:
                cach_resp.dump(file=filepath)
                
        return cach_resp
    
    def url2filename(self, url: str) -> str:
        if url not in self.url_map: 
            filename = uuid() + ".bin"
            self.url_map.setitem(url, filename)
            self.url_map_inv.setitem(filename, url, check_mutable=False)
            self.dump_url_map()
        return self.url_map.getitem(url)
    def filename2url(self, filename: str) -> str:
        return self.url_map_inv.getitem(filename)
        