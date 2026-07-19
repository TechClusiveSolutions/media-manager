import os
from pathlib import Path

from ui.shell.single_instance_guard import SingleInstanceGuard


def test_acquire_succeeds_when_no_lock_present(tmp_path: Path) -> None:
    guard = SingleInstanceGuard(tmp_path / "mediman.lock")

    assert guard.acquire() is True
    assert (tmp_path / "mediman.lock").read_text(encoding="utf-8") == str(os.getpid())


def test_acquire_fails_when_owner_still_alive(tmp_path: Path) -> None:
    lock_path = tmp_path / "mediman.lock"
    lock_path.write_text(str(os.getpid()), encoding="utf-8")

    guard = SingleInstanceGuard(lock_path)

    assert guard.acquire() is False


def test_acquire_succeeds_when_lock_file_content_is_invalid(tmp_path: Path) -> None:
    lock_path = tmp_path / "mediman.lock"
    lock_path.write_text("not-a-pid", encoding="utf-8")

    guard = SingleInstanceGuard(lock_path)

    assert guard.acquire() is True


def test_acquire_succeeds_when_owner_pid_is_dead(tmp_path: Path) -> None:
    lock_path = tmp_path / "mediman.lock"
    # A PID vanishingly unlikely to correspond to a live process.
    lock_path.write_text("999999", encoding="utf-8")

    guard = SingleInstanceGuard(lock_path)

    assert guard.acquire() is True


def test_release_removes_lock_file(tmp_path: Path) -> None:
    lock_path = tmp_path / "mediman.lock"
    guard = SingleInstanceGuard(lock_path)
    guard.acquire()

    guard.release()

    assert not lock_path.exists()


def test_request_focus_is_observed_by_primary(tmp_path: Path) -> None:
    lock_path = tmp_path / "mediman.lock"
    primary = SingleInstanceGuard(lock_path)
    primary.acquire()
    secondary = SingleInstanceGuard(lock_path)

    assert primary.poll_focus_requested() is False

    secondary.request_focus_on_existing()

    assert primary.poll_focus_requested() is True
    # The request is cleared once observed.
    assert primary.poll_focus_requested() is False
