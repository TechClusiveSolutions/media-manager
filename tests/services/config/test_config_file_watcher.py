import time
from pathlib import Path

from services.config.config_file_watcher import ConfigFileWatcher


def test_poll_detects_change_and_invokes_callback(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text("{}", encoding="utf-8")
    calls: list[None] = []
    watcher = ConfigFileWatcher(config_path, on_change=lambda: calls.append(None))

    assert watcher.poll() is False
    assert calls == []

    time.sleep(0.01)
    config_path.write_text('{"changed": true}', encoding="utf-8")

    assert watcher.poll() is True
    assert calls == [None]
    # A second poll with no further change should not re-fire.
    assert watcher.poll() is False
    assert calls == [None]
