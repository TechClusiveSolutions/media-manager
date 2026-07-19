"""The persistent main application window (docs/UX.md §1/§8).

Scoped to the Application Shell issue: menu bar chrome, the empty-state
navigation panel, Settings access, single-instance focus handling, and
minimize-to-tray/bounded-drain shutdown. Feed/compose/DM content areas are
tracked as separate, later issues.
"""

from collections.abc import Callable

import wx

from services.config.config_store import ConfigStore
from ui.settings.settings_frame import SettingsFrame
from ui.shell.navigation import Navigation
from ui.shell.single_instance_guard import SingleInstanceGuard
from ui.shell.tray_icon import TrayIcon

_FOCUS_POLL_INTERVAL_MS = 500


class MainFrame(wx.Frame):
    def __init__(
        self,
        config_store: ConfigStore,
        single_instance_guard: SingleInstanceGuard | None = None,
        on_shutdown: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(None, title="Mediman")
        self._config_store = config_store
        self._single_instance_guard = single_instance_guard
        self._on_shutdown = on_shutdown
        self._tray_icon: TrayIcon | None = None
        self._settings_menu_item: wx.MenuItem | None = None

        self._build_menu_bar()

        self.navigation = Navigation(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.navigation, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self._on_close)

        if self._single_instance_guard is not None:
            self._focus_poll_timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self._on_focus_poll_timer, self._focus_poll_timer)
            self._focus_poll_timer.Start(_FOCUS_POLL_INTERVAL_MS)

    def _build_menu_bar(self) -> None:
        menu_bar = wx.MenuBar()

        file_menu = wx.Menu()
        self._settings_menu_item = file_menu.Append(wx.ID_ANY, "Settings...\tCtrl+,")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self._on_settings, self._settings_menu_item)
        self.Bind(wx.EVT_MENU, self._on_exit, exit_item)
        menu_bar.Append(file_menu, "&File")

        compose_menu = wx.Menu()
        compose_menu.Append(wx.ID_ANY, "New Post")
        compose_menu.Append(wx.ID_ANY, "Draft with AI")
        compose_menu.Append(wx.ID_ANY, "Open Drafts")
        menu_bar.Append(compose_menu, "&Compose")

        view_menu = wx.Menu()
        view_menu.Append(wx.ID_ANY, "Feed Navigation Layout")
        view_menu.Append(wx.ID_ANY, "Show/Hide Notification Panel")
        menu_bar.Append(view_menu, "&View")

        account_menu = wx.Menu()
        account_menu.Append(wx.ID_ANY, "Add Account")
        account_menu.Append(wx.ID_ANY, "Manage Accounts")
        account_menu.Append(wx.ID_ANY, "Reconnect")
        menu_bar.Append(account_menu, "&Account")

        tools_menu = wx.Menu()
        tools_menu.Append(wx.ID_ANY, "Autonomous Post Record Review")
        menu_bar.Append(tools_menu, "&Tools")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ANY, "User Guide")
        help_menu.Append(wx.ID_ABOUT, "About")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

    def _on_settings(self, _event: wx.CommandEvent) -> None:
        dialog = SettingsFrame(self, self._config_store)
        dialog.ShowModal()
        dialog.Destroy()
        self.SetFocus()

    def _on_focus_poll_timer(self, _event: wx.TimerEvent) -> None:
        assert self._single_instance_guard is not None
        if self._single_instance_guard.poll_focus_requested():
            self.Show()
            self.Raise()
            self.Iconize(False)

    def _on_exit(self, _event: wx.CommandEvent) -> None:
        self.Close(force=True)

    def _on_close(self, event: wx.CloseEvent) -> None:
        if self._config_store.minimize_to_tray and event.CanVeto():
            event.Veto()
            self._minimize_to_tray()
            return
        self._shutdown()
        event.Skip()

    def _minimize_to_tray(self) -> None:
        self.Hide()
        if self._tray_icon is None:
            self._tray_icon = TrayIcon(self, on_exit=self._on_tray_exit)

    def _on_tray_exit(self) -> None:
        if self._tray_icon is not None:
            self._tray_icon.RemoveIcon()
            self._tray_icon.Destroy()
            self._tray_icon = None
        self._shutdown()
        self.Destroy()

    def _shutdown(self) -> None:
        if self._single_instance_guard is not None:
            self._single_instance_guard.release()
        if self._on_shutdown is not None:
            self._on_shutdown()
