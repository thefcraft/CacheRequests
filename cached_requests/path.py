import os
from typing import Iterator


class Path(str):
    def __matmul__(self, other: str) -> "Path":
        """Overload the @ operator to join paths."""
        return Path(os.path.join(self, other))
    def exists(self) -> bool:
        """Check if the path exists."""
        return os.path.exists(self)
    def ensure_exists(self) -> "Path":
        """Create the directory if it doesn't exist, and do nothing if it does."""
        os.makedirs(self, exist_ok=True)
        return self
    def iter_dir(self) -> Iterator[str]:
        """
        The function `iter_dir` yields the full path of each item in a directory if it exists, otherwise
        raises a `FileNotFoundError`.
        """
        if not self.exists():
            raise FileNotFoundError(f"Directory not found: {self}")
        assert os.path.isdir(self), "Path is not a Directory"
        for item in os.listdir(self):
            yield os.path.join(self, item)
    @classmethod
    def from_basedir(cls, file_path: str = __file__) -> "Path":
        """Return a Path instance based on the directory of the given file."""
        return cls(os.path.dirname(os.path.abspath(file_path)))
    def __repr__(self) -> str:
        """Override string representation for debugging."""
        return f"Path({super().__repr__()})"
    def join_path(self, *paths: str) -> "Path":
        return Path(os.path.join(self, *paths))
    def abs_path(self) -> "Path":
        return Path(os.path.abspath(self))
    
if __name__ == "__main__":
    basedir = Path.from_basedir(__file__)
    print(basedir)