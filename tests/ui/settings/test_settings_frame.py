from pathlib import Path

import pytest
import wx

from services.config.config_store import ConfigStore
from ui.settings.settings_frame import SettingsFrame

pytestmark = pytest.mark.widget


def _store(tmp_path: Path) -> ConfigStore:
    return ConfigStore(tmp_path / "config.json")


def test_general_category_reflects_current_config(tmp_path: Path, wx_app: wx.App) -> None:
    store = _store(tmp_path)
    store.set("allow_multiple_instances", True)
    store.set("minimize_to_tray", False)
    parent = wx.Frame(None)
    try:
        dialog = SettingsFrame(parent, store)
        try:
            assert dialog.allow_multiple_instances_checkbox.GetValue() is True
            assert dialog.minimize_to_tray_checkbox.GetValue() is False
            assert dialog.category_list.GetString(0) == "General"
        finally:
            dialog.Destroy()
    finally:
        parent.Destroy()


def test_autosave_notice_is_shown(tmp_path: Path, wx_app: wx.App) -> None:
    store = _store(tmp_path)
    parent = wx.Frame(None)
    try:
        dialog = SettingsFrame(parent, store)
        try:
            assert "automatically" in dialog.autosave_notice.GetLabel()
        finally:
            dialog.Destroy()
    finally:
        parent.Destroy()


def test_toggling_checkbox_persists_to_config_store(tmp_path: Path, wx_app: wx.App) -> None:
    store = _store(tmp_path)
    parent = wx.Frame(None)
    try:
        dialog = SettingsFrame(parent, store)
        try:
            checkbox = dialog.minimize_to_tray_checkbox
            checkbox.SetValue(True)
            event = wx.CommandEvent(wx.EVT_CHECKBOX.typeId, checkbox.GetId())
            event.SetInt(1)
            checkbox.GetEventHandler().ProcessEvent(event)

            assert store.minimize_to_tray is True
        finally:
            dialog.Destroy()
    finally:
        parent.Destroy()
