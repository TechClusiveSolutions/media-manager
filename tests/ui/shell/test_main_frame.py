from pathlib import Path

import wx

from services.config.config_store import ConfigStore
from ui.shell.main_frame import MainFrame
from ui.shell.single_instance_guard import SingleInstanceGuard


def _store(tmp_path: Path) -> ConfigStore:
    return ConfigStore(tmp_path / "config.json")


def test_menu_bar_has_required_top_level_menus(tmp_path: Path, wx_app: wx.App) -> None:
    frame = MainFrame(_store(tmp_path))
    try:
        menu_bar = frame.GetMenuBar()
        labels = [menu_bar.GetMenuLabelText(i) for i in range(menu_bar.GetMenuCount())]

        assert labels == ["File", "Compose", "View", "Account", "Tools", "Help"]
    finally:
        frame.Destroy()


def test_empty_state_navigation_panel_present(tmp_path: Path, wx_app: wx.App) -> None:
    frame = MainFrame(_store(tmp_path))
    try:
        assert frame.navigation.add_account_button.GetLabel() == "Add Account"
    finally:
        frame.Destroy()


def test_close_with_minimize_to_tray_disabled_calls_shutdown(
    tmp_path: Path, wx_app: wx.App
) -> None:
    store = _store(tmp_path)
    shutdown_calls: list[None] = []
    frame = MainFrame(store, on_shutdown=lambda: shutdown_calls.append(None))
    try:
        frame.Close(force=True)
        assert shutdown_calls == [None]
    finally:
        if frame:
            frame.Destroy()


def test_close_with_minimize_to_tray_enabled_hides_instead_of_shutting_down(
    tmp_path: Path, wx_app: wx.App
) -> None:
    store = _store(tmp_path)
    store.set("minimize_to_tray", True)
    shutdown_calls: list[None] = []
    frame = MainFrame(store, on_shutdown=lambda: shutdown_calls.append(None))
    try:
        close_event = wx.CloseEvent(wx.EVT_CLOSE.typeId)
        close_event.SetCanVeto(True)
        frame.GetEventHandler().ProcessEvent(close_event)

        assert shutdown_calls == []
        assert frame.IsShown() is False
    finally:
        frame._shutdown()  # pyright: ignore[reportPrivateUsage]
        frame.Destroy()


def test_settings_menu_item_opens_and_closes_settings_dialog(
    tmp_path: Path, wx_app: wx.App
) -> None:
    frame = MainFrame(_store(tmp_path))
    try:
        wx.CallLater(10, _dismiss_topmost_dialog)
        frame._on_settings(wx.CommandEvent())  # pyright: ignore[reportPrivateUsage]

        assert frame.HasFocus() or frame.FindFocus() is not None
    finally:
        frame.Destroy()


def _dismiss_topmost_dialog() -> None:
    for window in wx.GetTopLevelWindows():  # pyright: ignore[reportUnknownVariableType, reportCallIssue]
        if isinstance(window, wx.Dialog) and window.IsModal():
            window.EndModal(wx.ID_CANCEL)
            return


def test_focus_poll_timer_raises_frame_on_focus_request(tmp_path: Path, wx_app: wx.App) -> None:
    guard = SingleInstanceGuard(tmp_path / "mediman.lock")
    guard.acquire()
    frame = MainFrame(_store(tmp_path), single_instance_guard=guard)
    try:
        frame.Iconize(True)
        guard.request_focus_on_existing()

        frame._on_focus_poll_timer(None)  # pyright: ignore[reportPrivateUsage, reportArgumentType]

        assert frame.IsIconized() is False
    finally:
        guard.release()
        frame.Destroy()


def test_exit_menu_item_forces_close(tmp_path: Path, wx_app: wx.App) -> None:
    shutdown_calls: list[None] = []
    frame = MainFrame(_store(tmp_path), on_shutdown=lambda: shutdown_calls.append(None))
    try:
        frame._on_exit(wx.CommandEvent())  # pyright: ignore[reportPrivateUsage]

        assert shutdown_calls == [None]
    finally:
        frame.Destroy()


def test_tray_exit_removes_icon_and_shuts_down(tmp_path: Path, wx_app: wx.App) -> None:
    store = _store(tmp_path)
    store.set("minimize_to_tray", True)
    shutdown_calls: list[None] = []
    frame = MainFrame(store, on_shutdown=lambda: shutdown_calls.append(None))
    frame._minimize_to_tray()  # pyright: ignore[reportPrivateUsage]

    frame._on_tray_exit()  # pyright: ignore[reportPrivateUsage]

    assert shutdown_calls == [None]
