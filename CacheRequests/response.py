from requests.sessions import CaseInsensitiveDict, PreparedRequest, RequestsCookieJar
from requests import Response, HTTPError
import pickle
from typing import BinaryIO, overload, Iterator
from datetime import timedelta, datetime, timezone
from .path import Path

class CacheResponse(Response):
    def __init__(self, *, timestamp: datetime):
        self._stream_dump_path: Path | None = None
        self._timestamp: datetime = timestamp
        Response.__init__(self)
        
    @classmethod
    def from_current_timestamp(cls) -> "CacheResponse":
        return cls(
            timestamp=datetime.now(tz=timezone.utc)
        )

    @overload
    @classmethod
    def from_response(cls, resp: Response) -> "CacheResponse": ...
    @overload
    @classmethod
    def from_response(cls, resp: Response, *, dump_path: Path | None) -> "CacheResponse": ...
    
    @classmethod
    def from_response(cls, resp: Response, *, dump_path: Path | None = None) -> "CacheResponse":
        self = cls.from_current_timestamp()
        self._content = resp.content
        self._content_consumed = True  # type: ignore
        self._next = None  # type: ignore
        self.status_code = resp.status_code
        self.headers = resp.headers.copy()
        self.raw = None
        self.url = resp.url
        self.encoding = resp.encoding
        self.history = []  # redirect
        self.reason = resp.reason
        self.cookies = resp.cookies.copy()
        self.elapsed = resp.elapsed
        self._stream_dump_path = dump_path
        if resp.request is None:
            self.request = PreparedRequest()
        else:
            self.request = resp.request.copy()
        return self

    def iter_content(
        self, chunk_size: int | None = 1, decode_unicode: bool = False
    ) -> Iterator[bytes]:
        return Response.iter_content(self, chunk_size, decode_unicode)

    def close(self) -> None:
        Response.close(self)
        # TODO: we don't want to dump redirects that's why we handle other cases manually.
        if self._stream_dump_path:
            self.dump(file=self._stream_dump_path)

    def dump(self, file: BinaryIO | Path) -> None:
        _content: bytes | None = self._content
        status_code: int = self.status_code
        headers: CaseInsensitiveDict[str] = self.headers
        url: str = self.url
        encoding: str | None = self.encoding
        reason: str = self.reason
        cookies: RequestsCookieJar = self.cookies
        elapsed: timedelta = self.elapsed
        request: PreparedRequest = self.request
        data = {
            "_content": _content,
            "status_code": status_code,
            "headers": headers,
            "url": url,
            "encoding": encoding,
            "reason": reason,
            "cookies": cookies,
            "elapsed": elapsed,
            "request": request,
            "_timestamp": self._timestamp
        }
        if isinstance(file, str):
            with open(file, "wb") as f:
                pickle.dump(data, f, fix_imports=False)
        else:
            pickle.dump(data, file, fix_imports=False)
        
    @classmethod
    def load(cls, file: BinaryIO | Path) -> "CacheResponse":
        if isinstance(file, str):
            with open(file, "rb") as f:
                data = pickle.load(f, fix_imports=False)
        else:
            data = pickle.load(file, fix_imports=False)
            
        _content: bytes | None = data["_content"]
        status_code: int = data["status_code"]
        headers: CaseInsensitiveDict[str] = data["headers"]
        url: str = data["url"]
        encoding: str | None = data["encoding"]
        reason: str = data["reason"]
        cookies: RequestsCookieJar = data["cookies"]
        elapsed: timedelta = data["elapsed"]
        request: PreparedRequest = data["request"]
        _timestamp: datetime = data["_timestamp"]
        
        self = cls(timestamp=_timestamp)
        self._content = _content
        self._content_consumed = True  # type: ignore
        self._next = None  # type: ignore
        self.status_code = status_code
        self.headers = headers.copy()
        self.raw = None
        self.url = url
        self.encoding = encoding
        self.history = []  # redirect
        self.reason = reason
        self.cookies = cookies.copy()
        self.elapsed = elapsed
        self.request = request.copy()
        return self

    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    