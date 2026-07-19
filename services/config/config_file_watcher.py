"""Detects externally-made edits to the config file (docs/ARCHITECTURE.md §5)."""

from collections.abc import Callable
from pathlib import Path


class ConfigFileWatcher:
    """Polls a config file's mtime and invokes a callback when it changes.

    Used so an edit made directly to the config file while the app is
    running is picked up the same way a ``SettingsFrame`` edit would be,
    per docs/PRD.md §7.7.
    """

    def __init__(self, path: Path, on_change: Callable[[], None]) -> None:
        self._path = path
        self._on_change = on_change
        self._last_mtime = self._current_mtime()

    def _current_mtime(self) -> float | None:
        try:
            return self._path.stat().st_mtime
        except FileNotFoundError:
            return None

    def poll(self) -> bool:
        """Check for a change since the last poll; invoke the callback if so.

        Returns whether a change was detected.
        """
        mtime = self._current_mtime()
        if mtime != self._last_mtime:
            self._last_mtime = mtime
            self._on_change()
            return True
        return False
