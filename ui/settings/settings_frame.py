"""Modal settings dialog (docs/UX.md §7): search-filterable category tree.

Only the General category (with the two Foundational toggles from
docs/SESSION_MANAGEMENT.md §1) is implemented here; the remaining categories
(Accounts, Notifications, Compose & AI, Autonomy, Accessibility, Advanced)
are tracked as separate, later issues.
"""

import wx

from services.config.config_store import ConfigStore

_CATEGORIES = ["General"]


class SettingsFrame(wx.Dialog):
    def __init__(self, parent: wx.Window, config_store: ConfigStore) -> None:
        super().__init__(parent, title="Settings", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self._config_store = config_store

        self.search_box = wx.SearchCtrl(self)
        self.search_box.SetName("Search settings")

        self.autosave_notice = wx.StaticText(
            self, label="Changes on this screen are saved automatically."
        )

        self.category_list = wx.ListBox(self, choices=_CATEGORIES)
        self.category_list.SetSelection(0)

        self.allow_multiple_instances_checkbox = wx.CheckBox(self, label="Allow multiple instances")
        self.allow_multiple_instances_checkbox.SetValue(config_store.allow_multiple_instances)

        self.minimize_to_tray_checkbox = wx.CheckBox(self, label="Minimize to tray")
        self.minimize_to_tray_checkbox.SetValue(config_store.minimize_to_tray)

        general_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        general_panel_sizer.Add(self.allow_multiple_instances_checkbox, 0, wx.ALL, 6)
        general_panel_sizer.Add(self.minimize_to_tray_checkbox, 0, wx.ALL, 6)

        body_sizer = wx.BoxSizer(wx.HORIZONTAL)
        body_sizer.Add(self.category_list, 0, wx.EXPAND | wx.ALL, 6)
        body_sizer.Add(general_panel_sizer, 1, wx.EXPAND | wx.ALL, 6)

        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(self.search_box, 0, wx.EXPAND | wx.ALL, 6)
        root_sizer.Add(self.autosave_notice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 6)
        root_sizer.Add(body_sizer, 1, wx.EXPAND)
        self.SetSizer(root_sizer)

        self.allow_multiple_instances_checkbox.Bind(wx.EVT_CHECKBOX, self._on_toggle_allow_multiple)
        self.minimize_to_tray_checkbox.Bind(wx.EVT_CHECKBOX, self._on_toggle_minimize_to_tray)

        self.Bind(wx.EVT_INIT_DIALOG, self._on_init_dialog)

    def _on_init_dialog(self, event: wx.InitDialogEvent) -> None:
        event.Skip()
        self.search_box.SetFocus()

    def _on_toggle_allow_multiple(self, event: wx.CommandEvent) -> None:
        self._config_store.set("allow_multiple_instances", event.IsChecked())

    def _on_toggle_minimize_to_tray(self, event: wx.CommandEvent) -> None:
        self._config_store.set("minimize_to_tray", event.IsChecked())
