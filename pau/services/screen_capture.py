# pau/services/screen_capture.py

import os
import time
from datetime import datetime
import mss
import mss.tools

def take_screenshots(save_folder="data/screen_snapshot", prefix="DigitalVision", interval=10, iterations=0):
    """
    Periodically captures screenshots for all available physical monitors.

    Parameters:
        save_folder (str): Sub-folder under data/ where images will be saved.
        prefix (str): Filename prefix for screenshots.
        interval (int): Time (in seconds) between screenshots.
        iterations (int): Number of iterations to run; if 0, runs indefinitely.

    Each monitor's screenshot is saved with a filename formatted as:
        <prefix>_monitor<monitor_index>_YYYYMMDD_HHMMSS.png
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    with mss.mss() as sct:
        iteration = 0
        while iterations == 0 or iteration < iterations:
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            # sct.monitors[0] is the virtual monitor covering all screens;
            # Physical monitors are in sct.monitors[1:].
            for i, monitor in enumerate(sct.monitors[1:], start=1):
                filename = f"{prefix}_monitor{i}_{timestamp}.png"
                filepath = os.path.join(save_folder, filename)
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=filepath)
                print(f"[{timestamp}] Screenshot saved: {filepath}")
            time.sleep(interval)
            iteration += 1

if __name__ == "__main__":
    # For testing purposes: capture all screens every 10 seconds indefinitely.
    take_screenshots(interval=10)
