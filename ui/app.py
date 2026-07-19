"""Application entry point: wires ConfigStore, single-instance enforcement,
and MainFrame together per docs/SESSION_MANAGEMENT.md §1.
"""

import sys
from pathlib import Path

import wx

from services.config.config_store import ConfigStore
from ui.shell.main_frame import MainFrame
from ui.shell.single_instance_guard import SingleInstanceGuard

_APP_DATA_DIR = Path.home() / ".mediman"
_CONFIG_PATH = _APP_DATA_DIR / "config.json"
_LOCK_PATH = _APP_DATA_DIR / "mediman.lock"


class MedimanApp(wx.App):
    def OnInit(self) -> bool:  # noqa: N802 (wx API override)
        config_store = ConfigStore(_CONFIG_PATH)

        guard: SingleInstanceGuard | None = None
        if not config_store.allow_multiple_instances:
            guard = SingleInstanceGuard(_LOCK_PATH)
            if not guard.acquire():
                guard.request_focus_on_existing()
                return False

        frame = MainFrame(config_store, single_instance_guard=guard)
        frame.Show()
        self.SetTopWindow(frame)
        return True


def main() -> int:
    app = MedimanApp()
    app.MainLoop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
