import json
from pathlib import Path

from services.config import defaults
from services.config.config_store import ConfigStore


def test_first_run_constructs_config_from_defaults(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"

    store = ConfigStore(config_path)

    assert config_path.exists()
    assert store.allow_multiple_instances is defaults.ALLOW_MULTIPLE_INSTANCES
    assert store.minimize_to_tray is defaults.MINIMIZE_TO_TRAY
    on_disk = json.loads(config_path.read_text(encoding="utf-8"))
    assert on_disk["allow_multiple_instances"] is defaults.ALLOW_MULTIPLE_INSTANCES
    assert on_disk["minimize_to_tray"] is defaults.MINIMIZE_TO_TRAY


def test_existing_config_is_loaded_not_overwritten(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"allow_multiple_instances": True, "minimize_to_tray": True}),
        encoding="utf-8",
    )

    store = ConfigStore(config_path)

    assert store.allow_multiple_instances is True
    assert store.minimize_to_tray is True


def test_set_persists_and_is_reflected_immediately(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    store = ConfigStore(config_path)

    store.set("minimize_to_tray", True)

    assert store.minimize_to_tray is True
    on_disk = json.loads(config_path.read_text(encoding="utf-8"))
    assert on_disk["minimize_to_tray"] is True


def test_reload_picks_up_external_edit(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    store = ConfigStore(config_path)

    config_path.write_text(
        json.dumps({"allow_multiple_instances": True, "minimize_to_tray": False}),
        encoding="utf-8",
    )
    store.reload()

    assert store.allow_multiple_instances is True
