#!/usr/bin/env python3
"""Show a short on-screen notification in the middle of the screen.

Usage: osd.py TEXT [SECONDS]

Borderless, always-on-top GTK window that closes itself after
SECONDS (default 1). Own window, independent of Simon. Needs the system
python3 (python3-gi with Gtk 3). X11.
"""
import sys

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk  # noqa: E402

CSS = b"""
window { background-color: rgba(20, 20, 20, 0.88); border-radius: 18px; }
label { color: white; font-size: 44px; font-weight: bold; padding: 28px 56px; }
"""


def main():
    if len(sys.argv) < 2:
        print("usage: osd.py TEXT [SECONDS]", file=sys.stderr)
        return 2
    text = sys.argv[1]
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

    win = Gtk.Window(type=Gtk.WindowType.POPUP)
    win.set_decorated(False)
    win.set_keep_above(True)
    win.set_accept_focus(False)
    win.set_skip_taskbar_hint(True)
    win.set_position(Gtk.WindowPosition.CENTER)
    win.set_app_paintable(True)
    screen = win.get_screen()
    visual = screen.get_rgba_visual()
    if visual is not None:
        win.set_visual(visual)

    provider = Gtk.CssProvider()
    provider.load_from_data(CSS)
    Gtk.StyleContext.add_provider_for_screen(
        screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    win.add(Gtk.Label(label=text))
    win.show_all()

    GLib.timeout_add(int(seconds * 1000), Gtk.main_quit)
    Gtk.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
