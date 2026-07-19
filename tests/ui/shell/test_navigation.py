import pytest
import wx

from ui.shell.navigation import Navigation

pytestmark = pytest.mark.widget


def test_navigation_shows_empty_state_and_add_account_button(wx_app: wx.App) -> None:
    frame = wx.Frame(None)
    try:
        nav = Navigation(frame)

        assert nav.add_account_button.GetLabel() == "Add Account"
        assert nav.add_account_button.CanAcceptFocus()
    finally:
        frame.Destroy()
