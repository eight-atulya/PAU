import os
import time
import cv2
import numpy as np
import mss
import mss.tools
from skimage.metrics import structural_similarity as ssim

def is_similar(image1_path, image2_path, threshold=0.88):
    """
    Compare two images using Structural Similarity Index (SSIM).
    Returns True if similarity is above the threshold.
    """
    if not os.path.exists(image1_path) or not os.path.exists(image2_path):
        return False  # No comparison if any image is missing

    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    if img1.shape != img2.shape:
        return False  # Different resolutions, assume different images

    # Compute SSIM (Structural Similarity Index)
    similarity_index, _ = ssim(img1, img2, full=True)
    
    return similarity_index >= threshold

def take_screenshots(save_folder="data/screen_snapshot", prefix="DigitalVision", interval=10, iterations=0):
    """
    Captures screenshots periodically but avoids duplicates using SSIM.
    Ensures that each monitor is compared only to its own last captured image.
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    last_saved_images = {}  # Dictionary to track last saved image per monitor

    with mss.mss() as sct:
        iteration = 0
        while iterations == 0 or iteration < iterations:
            timestamp = time.strftime("%Y%m%d_%H%M%S")

            for i, monitor in enumerate(sct.monitors[1:], start=1):
                filename = f"{prefix}_monitor{i}_{timestamp}.png"
                filepath = os.path.join(save_folder, filename)

                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=filepath)

                if i in last_saved_images:
                    # Check similarity for the same monitor
                    if is_similar(last_saved_images[i], filepath):
                        os.remove(filepath)  # Delete duplicate
                        print(f"Deleted duplicate for monitor {i}: {filepath}")
                    else:
                        last_saved_images[i] = filepath  # Update last saved image for this monitor
                else:
                    last_saved_images[i] = filepath  # First image for this monitor

            time.sleep(interval)
            iteration += 1

if __name__ == "__main__":
    take_screenshots(interval=10)
