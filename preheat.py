# preheat.py

import threading
from pau.services.screen_capture import take_screenshots

def start_screen_capture():
    # Start the screenshot service in a background thread.
    thread = threading.Thread(
        target=take_screenshots,
        kwargs={
            "save_folder": "data/screen_snapshot",
            "prefix": "DigitalVision",
            "interval": 10,   # adjust the interval as desired
            "iterations": 0   # 0 means run indefinitely
        },
        daemon=True
    )
    thread.start()
    print("DigitalVision screen capture started in background thread.")

if __name__ == "__main__":
    start_screen_capture()
    # Keep the script running (or integrate into your main app startup)
    while True:
        pass
