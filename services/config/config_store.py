"""Single source of truth for application settings (docs/ARCHITECTURE.md §5)."""

import json
import os
import time
from pathlib import Path
from typing import Any

from services.config import defaults

_LOCK_STALE_SECONDS = 5.0
_LOCK_POLL_SECONDS = 0.05


class ConfigStore:
    """Reads/writes the application's single config file.

    On first run (no file present at ``path``), constructs a fresh, valid
    config file from ``services.config.defaults``' constants and writes it
    out immediately, per docs/SESSION_MANAGEMENT.md §1.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock_path = path.with_suffix(path.suffix + ".lock")
        if not self._path.exists():
            self._data: dict[str, Any] = {
                "allow_multiple_instances": defaults.ALLOW_MULTIPLE_INSTANCES,
                "minimize_to_tray": defaults.MINIMIZE_TO_TRAY,
            }
            self._write()
        else:
            self._data = json.loads(self._path.read_text(encoding="utf-8"))

    @property
    def allow_multiple_instances(self) -> bool:
        return bool(self._data["allow_multiple_instances"])

    @property
    def minimize_to_tray(self) -> bool:
        return bool(self._data["minimize_to_tray"])

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._write()

    def reload(self) -> None:
        """Reload from disk, picking up an externally-made edit."""
        self._data = json.loads(self._path.read_text(encoding="utf-8"))

    def _write(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._advisory_write_lock():
            self._path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    def _advisory_write_lock(self) -> "_AdvisoryWriteLock":
        return _AdvisoryWriteLock(self._lock_path)


class _AdvisoryWriteLock:
    """Cross-process advisory lock serializing ConfigStore writes.

    Only held around a write, never around reads, per
    docs/SESSION_MANAGEMENT.md §1's "Multi-instance data-safety" note.
    """

    def __init__(self, lock_path: Path) -> None:
        self._lock_path = lock_path

    def __enter__(self) -> "_AdvisoryWriteLock":
        deadline = time.monotonic() + _LOCK_STALE_SECONDS
        while True:
            try:
                fd = os.open(self._lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                return self
            except FileExistsError:
                if time.monotonic() >= deadline:
                    # Stale lock from a crashed process; reclaim it.
                    self._lock_path.unlink(missing_ok=True)
                    continue
                time.sleep(_LOCK_POLL_SECONDS)

    def __exit__(self, *exc_info: object) -> None:
        self._lock_path.unlink(missing_ok=True)
