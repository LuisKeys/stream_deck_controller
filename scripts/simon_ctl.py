#!/usr/bin/env python3
"""Press a button of the running Simon control window from the outside.

Usage: simon_ctl.py mute|lang

Finds the "Simon" GTK window through the AT-SPI accessibility bus, locates the
button by its label and invokes its "click" action. No mouse movement, no focus
change, no coordinates. Bound to Stream Deck keys 8 and 9 in config.yaml.
Needs the system python3 (python3-gi with Atspi). Linux only.
"""
import sys

import gi

gi.require_version("Atspi", "2.0")
from gi.repository import Atspi  # noqa: E402

WINDOW_NAME = "Simon"
# Labels each button can show (see gui_linux.c in simon_dictate).
# "Exit" is never listed, so it can never be pressed by mistake.
BUTTONS = {
    "mute": {"Mute", "Muted"},
    "lang": {"EN", "ES"},
}


def find_window():
    desktop = Atspi.get_desktop(0)
    for i in range(desktop.get_child_count()):
        app = desktop.get_child_at_index(i)
        if app is None:
            continue
        for j in range(app.get_child_count()):
            win = app.get_child_at_index(j)
            if win is not None and win.get_name() == WINDOW_NAME:
                return win
    return None


def find_button(node, labels):
    if node.get_role() == Atspi.Role.PUSH_BUTTON and node.get_name() in labels:
        return node
    for i in range(node.get_child_count()):
        child = node.get_child_at_index(i)
        if child is None:
            continue
        found = find_button(child, labels)
        if found is not None:
            return found
    return None


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in BUTTONS:
        print("usage: simon_ctl.py mute|lang", file=sys.stderr)
        return 2

    win = find_window()
    if win is None:
        print(f'simon_ctl: window "{WINDOW_NAME}" not found (is simon_dictate running? '
              "is accessibility enabled?)", file=sys.stderr)
        return 1

    btn = find_button(win, BUTTONS[sys.argv[1]])
    if btn is None:
        print(f"simon_ctl: {sys.argv[1]} button not found", file=sys.stderr)
        return 1

    btn.get_action_iface().do_action(0)  # action 0 = "click"
    return 0


if __name__ == "__main__":
    sys.exit(main())
