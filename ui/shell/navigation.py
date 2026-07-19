"""Empty-state navigation panel shown in ``MainFrame`` when no accounts exist.

Full account/feed-tree navigation (docs/UX.md §4) is out of scope for this
issue; this is the empty-state described in the Application Shell
acceptance criteria only.
"""

import wx


class Navigation(wx.Panel):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent)

        message = wx.StaticText(
            self,
            label="No accounts are configured yet.",
        )
        self.add_account_button = wx.Button(self, label="Add Account")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(message, 0, wx.ALL, 12)
        sizer.Add(self.add_account_button, 0, wx.ALL, 12)
        self.SetSizer(sizer)

        # Named so assistive technology announces this region as
        # "no accounts configured yet" rather than an unlabeled panel.
        self.SetName("Account navigation")
