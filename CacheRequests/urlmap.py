import os
from .path import Path

class UrlMap(dict[str, str]):
    def __init__(self, *args, mutable: bool = True, **kwargs):
        self.__mutable = mutable
        super().__init__(*args, **kwargs)
        
    @property
    def mutable(self) -> bool: return self.__mutable

    def _check_mutable(self):
        if not self.mutable:
            raise TypeError("This dictionary is constant and cannot be modified.")

    def inverse(self) -> "UrlMap":
        if len(self) != len(set(self.values())):
            raise ValueError(
                f"Values Can't be Duplicate, maybe Duplicate uuid exists, url_map: {self}"
            )
        return UrlMap(((v, k) for k, v in self.items()), mutable=False)

    def clear(self) -> None:
        raise RuntimeError("Unsupported method")

    def pop(self, key, default=None):
        raise RuntimeError("Unsupported method")

    def popitem(self):
        raise RuntimeError("Unsupported method")

    def setdefault(self, key, default=None):
        raise RuntimeError("Unsupported method")

    def update(self, *args, **kwargs):
        raise RuntimeError("Unsupported method")

    def __ior__(self, other):
        raise RuntimeError("Unsupported method")

    def __or__(self, other):
        raise RuntimeError("Unsupported method")

    def __ror__(self, other):
        raise RuntimeError("Unsupported method")

    def __getitem__(self, key: str) -> str:
        raise RuntimeError("Please use `getitem` Insted.")

    def __setitem__(self, key: str, value: str) -> None:
        raise RuntimeError("Please use `setitem` Insted.")

    def __delitem__(self, key: str) -> None:
        raise RuntimeError("Please use `delitem` Insted.")

    def getitem(self, key: str) -> str:
        return super().__getitem__(key)

    def setitem(self, key: str, value: str, check_mutable: bool = True) -> None:
        if check_mutable:
            self._check_mutable()
        return super().__setitem__(key, value)

    def delitem(self, key: str, cachedir: Path) -> None:
        self._check_mutable()
        filepath = cachedir @ self.getitem(key)
        if filepath.exists():
            os.remove(filepath)
        return super().__delitem__(key)

    def empty(self, cachedir: Path) -> None:
        self._check_mutable()
        for key, value in self.items():
            filepath = cachedir @ value
            if filepath.exists():
                os.remove(filepath)
        super().clear()

