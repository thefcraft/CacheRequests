from requests import Session, PreparedRequest
from requests.cookies import RequestsCookieJar
from requests.auth import AuthBase
from .response import CacheResponse
from .path import Path
from .urlmap import UrlMap

from contextlib import contextmanager
from datetime import timedelta
from typing import Any, TypeAlias
from requests.sessions import (
    _Params, 
    _Data, 
    _HeadersUpdateMapping, 
    _TextMapping, 
    _Files,
    _Auth, 
    _Timeout,
    _HooksInput,
    _Verify,
    _Cert
)
_JSON: TypeAlias = Any  # any object that can be serialized to JSON

class _Default: ...
_DEFAULT = _Default()


class CacheSession(Session):
    def get(
        self,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: _JSON | None = None,
    ) -> CacheResponse: ...
    def options(
        self,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: _JSON | None = None,
    ) -> CacheResponse: ...
    def head(
        self,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: _JSON | None = None,
    ) -> CacheResponse: ...
    def post(
        self,
        url: str | bytes,
        data: _Data | None = None,
        json: _JSON | None = None,
        *,
        params: _Params | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
    ) -> CacheResponse: ...
    def put(
        self,
        url: str | bytes,
        data: _Data | None = None,
        *,
        params: _Params | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: _JSON | None = None,
    ) -> CacheResponse: ...
    def patch(
        self,
        url: str | bytes,
        data: _Data | None = None,
        *,
        params: _Params | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: _JSON | None = None,
    ) -> CacheResponse: ...
    def delete(
        self,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: _JSON | None = None,
    ) -> CacheResponse: ...
    def send(
        self,
        request: PreparedRequest,
        *,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        proxies: _TextMapping | None = ...,
        cert: _Cert | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        **kwargs: Any,
    ) -> CacheResponse: ...
    
    def __init__(self, 
                 cache_dir: Path | str | None = None, 
                 force_refresh: bool = False, 
                 refresh_on_error: bool = False, 
                 dump_to_cache: bool = True,
                 overwrite_allow_redirects: bool | None = False,
                 refresh_after: timedelta | None = None) -> None: ...
    def dump_url_map(self): ...
    def load_url_map(self) -> UrlMap: ...
    @property
    def dump_to_cache(self) -> bool: ...
    @property
    def cache_dir(self) -> Path: ...
    @property
    def refresh_after(self) -> timedelta | None: ...
    @property
    def force_refresh(self) -> bool: ...
    @property
    def refresh_on_error(self) -> bool: ...
    @property
    def overwrite_allow_redirects(self) -> bool | None: ...
    @property
    def url_map(self) -> UrlMap: ...
    @property
    def url_map_inv(self) -> UrlMap: ...
    
    @contextmanager
    def configure(self, 
        cache_dir: Path | str | None | _Default = _DEFAULT,
        force_refresh: bool | _Default = _DEFAULT,
        refresh_after: timedelta | None | _Default = _DEFAULT,
        refresh_on_error: bool | _Default = _DEFAULT,
        dump_to_cache: bool | _Default = _DEFAULT,
        overwrite_allow_redirects: bool | None | _Default = _DEFAULT,
    ): ...
    
    def request(
        self,
        method: str | bytes,
        url: str | bytes,
        params: _Params | None = None,
        data: _Data | None = None,
        headers: _HeadersUpdateMapping | None = None,
        cookies: None | RequestsCookieJar | _TextMapping = None,
        files: _Files | None = None,
        auth: _Auth | None = None,
        timeout: _Timeout | None = None,
        allow_redirects: bool = True,
        proxies: _TextMapping | None = None,
        hooks: _HooksInput | None = None,
        stream: bool | None = None,
        verify: _Verify | None = None,
        cert: _Cert | None = None,
        json: _JSON | None = None,
    ) -> CacheResponse: ...
    
    def url2filename(self, url: str) -> str: ...
    def filename2url(self, filename: str) -> str: ...