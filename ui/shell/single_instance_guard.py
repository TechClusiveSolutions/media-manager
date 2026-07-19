"""Single-instance enforcement, configurable via ``allow_multiple_instances``.

Per docs/SESSION_MANAGEMENT.md §1: when a second launch is detected and
multiple instances aren't allowed, the existing instance is asked to focus
its window rather than letting a second process start. File-based (a lock
file holding the owning PID, plus a sibling "focus request" file) so it is
testable without a live GUI/IPC channel.
"""

import os
from pathlib import Path


class SingleInstanceGuard:
    def __init__(self, lock_path: Path) -> None:
        self._lock_path = lock_path
        self._focus_request_path = lock_path.with_suffix(lock_path.suffix + ".focus")
        self._is_primary = False

    def acquire(self) -> bool:
        """Attempt to become the primary instance.

        Returns True if this process is now the primary instance, False if
        another live instance already holds the lock (in which case the
        caller should request focus on it instead of starting normally).
        """
        if self._lock_path.exists() and self._owner_is_alive():
            return False
        self._lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock_path.write_text(str(os.getpid()), encoding="utf-8")
        self._is_primary = True
        return True

    def release(self) -> None:
        if self._is_primary:
            self._lock_path.unlink(missing_ok=True)
            self._is_primary = False

    def request_focus_on_existing(self) -> None:
        """Signal the primary instance to raise/focus its window."""
        self._focus_request_path.write_text("1", encoding="utf-8")

    def poll_focus_requested(self) -> bool:
        """Check (and clear) whether another launch requested focus.

        Called periodically by the primary instance's ``MainFrame``.
        """
        if self._focus_request_path.exists():
            self._focus_request_path.unlink(missing_ok=True)
            return True
        return False

    def _owner_is_alive(self) -> bool:
        try:
            pid = int(self._lock_path.read_text(encoding="utf-8").strip())
        except (ValueError, FileNotFoundError):
            return False
        return _pid_is_running(pid)


def _pid_is_running(pid: int) -> bool:
    if os.name == "nt":
        import ctypes

        process = ctypes.windll.kernel32.OpenProcess(1, 0, pid)  # PROCESS_TERMINATE
        if process:
            ctypes.windll.kernel32.CloseHandle(process)
            return True
        return False
    try:  # pragma: no cover (posix-only path; this project's CI runs a Windows leg too)
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True
