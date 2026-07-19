import pytest
import wx

from ui.shell.tray_icon import TrayIcon

pytestmark = pytest.mark.widget


def test_restore_shows_raises_and_removes_icon(wx_app: wx.App) -> None:
    frame = wx.Frame(None)
    frame.Hide()
    tray_icon = TrayIcon(frame, on_exit=lambda: None)
    try:
        tray_icon._on_restore(wx.CommandEvent())  # pyright: ignore[reportPrivateUsage]

        assert frame.IsShown() is True
    finally:
        frame.Destroy()


def test_popup_menu_exit_item_invokes_callback(wx_app: wx.App) -> None:
    frame = wx.Frame(None)
    calls: list[None] = []
    tray_icon = TrayIcon(frame, on_exit=lambda: calls.append(None))
    try:
        tray_icon._on_exit(wx.CommandEvent())  # pyright: ignore[reportPrivateUsage]

        assert calls == [None]
    finally:
        frame.Destroy()


def test_create_popup_menu_has_restore_and_exit(wx_app: wx.App) -> None:
    frame = wx.Frame(None)
    tray_icon = TrayIcon(frame, on_exit=lambda: None)
    try:
        menu = tray_icon.CreatePopupMenu()
        labels: list[str] = [
            item.GetItemLabelText()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            for item in menu.GetMenuItems()  # pyright: ignore[reportUnknownVariableType]
        ]

        assert labels == ["Restore", "Exit"]
    finally:
        frame.Destroy()
