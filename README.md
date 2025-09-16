# Stream Deck Control

A customizable Python application to control your Elgato Stream Deck on Linux. Assign icons and commands to each key for quick access to your favorite apps, websites, and scripts.

---

## Features
- Assign custom icons and commands to each Stream Deck key
- Supports PNG, JPG, and ICO icons (with automatic resizing)
- Graceful shutdown and device reset on exit
- Autostart at login (KDE Plasma and other desktops)
- Simple YAML configuration

---

## Requirements
- Python 3.7+
- [Pillow](https://python-pillow.org/) (PIL)
- [StreamDeck Python Library](https://github.com/abcminiuser/python-elgato-streamdeck)
- PyYAML

Install dependencies:
```sh
pip install -r requirements.txt
```

---

## Usage

1. **Connect your Stream Deck.**
2. **Edit `config.yaml`** to assign icons and commands to each key:

```yaml
keys:
  0:
    icon: "microsoft-edge.png"
    command: "microsoft-edge"
  1:
    icon: "tabby.png"
    command: "tabby"
  # ...
```

- Place your icon images in the `icons/` folder.
- Supported image formats: PNG, JPG, ICO (best results with PNG).

3. **Run the program:**
```sh
python main.py
```

---

## Autostart at Login (KDE Plasma)

1. Create a file at `~/.config/autostart/stream_deck_control.desktop`:

```
[Desktop Entry]
Type=Application
Exec=/path/to/python /path/to/main.py
WorkingDirectory=/path/to/project
Name=Stream Deck Control
Comment=Start Stream Deck Control at login
X-KDE-autostart-after=panel
```

2. Replace `/path/to/python` and `/path/to/main.py` with your actual paths.
3. Log out and log back in, or use KDE System Settings → Startup and Shutdown → Autostart.

---

## Graceful Shutdown
- The Stream Deck is reset and all keys are cleared when the program exits or is killed.

---

## Troubleshooting
- If icons do not appear, check the `icons/` folder and file names.
- For `.ico` files, convert to `.png` if you see errors.
- If the program does not autostart, check the `.desktop` file paths and permissions.

---

## License
MIT License

---

## Credits
- [python-elgato-streamdeck](https://github.com/abcminiuser/python-elgato-streamdeck)
- [Pillow](https://python-pillow.org/)
- [PyYAML](https://pyyaml.org/)
