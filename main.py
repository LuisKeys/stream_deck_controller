import time
import signal
import sys
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import os
import subprocess
import yaml


def load_config():
    CONFIG_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config.yaml"
    )
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)


def render_key(deck, key_config):
    size = deck.key_image_format()["size"]
    image = Image.new("RGB", size, "black")
    draw = ImageDraw.Draw(image)

    if "icon" in key_config:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = key_config.get("base_icon_dir", "icons")
        icon_path = os.path.join(script_dir, base_dir, key_config["icon"])
        print(f"Looking for icon at: {os.path.abspath(icon_path)}")  # Debug output

        if not os.path.exists(icon_path):
            print(f"File not found: {icon_path}")
            if os.path.exists(os.path.join(script_dir, base_dir)):
                print(
                    f"Files in {os.path.join(script_dir, base_dir)}: {os.listdir(os.path.join(script_dir, base_dir))}"
                )
            return image

        try:
            icon = Image.open(icon_path).convert("RGBA").resize(size)
            image.paste(icon, (0, 0), icon)
        except Exception as e:
            print(f"Error loading icon {icon_path}: {e}")
            # Optionally, render text fallback if icon fails
            if "text" in key_config:
                font = ImageFont.load_default()
                w, h = draw.textsize(key_config["text"], font=font)
                draw.text(
                    ((image.width - w) / 2, (image.height - h) / 2),
                    key_config["text"],
                    fill="white",
                    font=font,
                )
            return image
    elif "text" in key_config:
        font = ImageFont.load_default()
        w, h = draw.textsize(key_config["text"], font=font)
        draw.text(
            ((image.width - w) / 2, (image.height - h) / 2),
            key_config["text"],
            fill="white",
            font=font,
        )

    return image


def run_command(command):
    subprocess.Popen(command, shell=True)


def reset_deck(deck):
    """Reset the Stream Deck to its default state"""
    # Turn off all key images
    deck.reset()
    # Set brightness to default (30%)
    deck.set_brightness(30)


def main():
    deck = DeviceManager().enumerate()[0]
    deck.open()
    reset_deck(deck)

    def cleanup_and_exit(signum=None, frame=None):
        reset_deck(deck)
        deck.close()
        sys.exit(0)

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, cleanup_and_exit)  # Ctrl+C
    signal.signal(signal.SIGTERM, cleanup_and_exit)  # kill or logout

    try:
        config = load_config()

        # draw keys
        for key, cfg in config["keys"].items():
            img = render_key(deck, cfg)
            # Convert PIL image to native format for StreamDeck
            native_img = PILHelper.to_native_format(deck, img)
            deck.set_key_image(int(key), native_img)

        # handle presses
        def key_change(deck, key, state):
            if state and key in config["keys"]:
                command = config["keys"][key]["command"]
                run_command(command)

        deck.set_key_callback(key_change)

        while True:
            time.sleep(0.1)

    finally:
        # Always reset the deck when exiting
        reset_deck(deck)
        deck.close()


if __name__ == "__main__":
    main()
