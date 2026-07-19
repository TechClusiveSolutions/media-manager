"""System tray icon shown when ``minimize_to_tray`` is enabled.

Per docs/SESSION_MANAGEMENT.md §1: closing the main window hides it to this
icon instead of exiting; the process keeps running. Selecting Exit from the
icon's context menu performs the full bounded-drain shutdown.
"""

from collections.abc import Callable

import wx
import wx.adv


class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame: wx.Frame, on_exit: Callable[[], None]) -> None:
        super().__init__()
        self._frame = frame
        self._on_exit_callback: Callable[[], None] = on_exit
        # wx's stubs declare SetIcon(BitmapBundle), but wx.Icon is accepted at
        # runtime; this is a stub inaccuracy, not a real type mismatch.
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION), "Mediman")  # pyright: ignore[reportArgumentType]
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self._on_restore)

    def CreatePopupMenu(self) -> wx.Menu:  # noqa: N802 (wx API override)
        menu = wx.Menu()
        restore_item = menu.Append(wx.ID_ANY, "Restore")
        exit_item = menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self._on_restore, restore_item)
        self.Bind(wx.EVT_MENU, self._on_exit, exit_item)
        return menu

    def _on_restore(self, _event: wx.Event) -> None:
        self._frame.Show()
        self._frame.Raise()
        self.RemoveIcon()

    def _on_exit(self, _event: wx.Event) -> None:
        self._on_exit_callback()
