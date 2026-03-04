import sys
from PIL import Image, ImageDraw
import pystray
# from sympy import root
from startup import toggle_startup, is_in_startup

def create_image():
    # Simple black/white square icon
    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill='white')
    return image

def quit_app(icon, item):
    icon.stop()
    sys.exit(0)

def run_tray():
    icon = pystray.Icon(
        "VoiceMute",
        create_image(),
        "Voice Mute Controller",
        menu=pystray.Menu(
            pystray.MenuItem(
                "Run on Startup", toggle_startup,
                checked=lambda item: is_in_startup(),
            ),
            pystray.MenuItem("Quit", quit_app)
        )
    )
    icon.run()

# def minimise_to_tray():
#     root.withdraw()