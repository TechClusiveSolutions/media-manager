from collections.abc import Iterator

import pytest
import wx


@pytest.fixture(scope="session")
def wx_app() -> Iterator[wx.App]:
    """A single wx.App for the whole test session (widget tests need one)."""
    app = wx.App()
    yield app
