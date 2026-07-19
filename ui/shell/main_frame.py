"""The persistent main application window (docs/UX.md §1/§8).

Scoped to the Application Shell issue: menu bar chrome, the empty-state
navigation panel, Settings access, single-instance focus handling, and
minimize-to-tray/bounded-drain shutdown. Feed/compose/DM content areas are
tracked as separate, later issues.
"""

from collections.abc import Callable
from typing import cast

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
        super().__init__(None, title="MediMan")
        self._config_store = config_store
        self._single_instance_guard = single_instance_guard
        self._on_shutdown = on_shutdown
        self._tray_icon: TrayIcon | None = None
        self._settings_menu_item: wx.MenuItem | None = None
        self._focus_before_settings: wx.Window | None = None
        # No core.accounts.AccountManager exists yet (tracked separately,
        # Milestone 2) — every launch is currently the "no accounts
        # configured" state, so account-dependent menu items start disabled.
        # set_has_active_accounts() is the seam that milestone will wire up.
        self._has_active_accounts = False

        self._build_menu_bar()
        self._update_account_dependent_menu_items()

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
        exit_item = file_menu.Append(wx.ID_EXIT, "Exit\tCtrl+Q")
        self.Bind(wx.EVT_MENU, self._on_settings, self._settings_menu_item)
        self.Bind(wx.EVT_MENU, self._on_exit, exit_item)
        menu_bar.Append(file_menu, "&File")

        self._compose_menu = wx.Menu()
        self._compose_menu.Append(wx.ID_ANY, "New Post")
        self._compose_menu.Append(wx.ID_ANY, "Draft with AI")
        self._compose_menu.Append(wx.ID_ANY, "Open Drafts")
        menu_bar.Append(self._compose_menu, "&Compose")

        self._view_menu = wx.Menu()
        self._view_menu.Append(wx.ID_ANY, "Feed Navigation Layout")
        self._view_menu.Append(wx.ID_ANY, "Show/Hide Notification Panel")
        menu_bar.Append(self._view_menu, "&View")

        account_menu = wx.Menu()
        account_menu.Append(wx.ID_ANY, "Add Account")
        account_menu.Append(wx.ID_ANY, "Manage Accounts")
        self._reconnect_item = account_menu.Append(wx.ID_ANY, "Reconnect")
        menu_bar.Append(account_menu, "&Account")

        tools_menu = wx.Menu()
        tools_menu.Append(wx.ID_ANY, "Autonomous Post Record Review")
        menu_bar.Append(tools_menu, "&Tools")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ANY, "User Guide")
        help_menu.Append(wx.ID_ABOUT, "About")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

    def set_has_active_accounts(self, has_accounts: bool) -> None:
        """Enable/disable menu items that assume at least one active account.

        The seam `core.accounts.AccountManager` (Milestone 2) will call into
        once it exists; every launch is the no-accounts state until then.
        """
        self._has_active_accounts = has_accounts
        self._update_account_dependent_menu_items()

    def _update_account_dependent_menu_items(self) -> None:
        for item in cast("list[wx.MenuItem]", self._compose_menu.GetMenuItems()):
            item.Enable(self._has_active_accounts)
        for item in cast("list[wx.MenuItem]", self._view_menu.GetMenuItems()):
            item.Enable(self._has_active_accounts)
        self._reconnect_item.Enable(self._has_active_accounts)

    def _on_settings(self, _event: wx.CommandEvent) -> None:
        # wx's stubs declare FindFocus() -> Window (non-optional), but it
        # returns None at runtime when nothing currently holds focus.
        self._focus_before_settings = cast("wx.Window | None", wx.Window.FindFocus())
        dialog = SettingsFrame(self, self._config_store)
        dialog.ShowModal()
        dialog.Destroy()
        if self._focus_before_settings is not None:
            self._focus_before_settings.SetFocus()
        else:
            self.navigation.add_account_button.SetFocus()

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
