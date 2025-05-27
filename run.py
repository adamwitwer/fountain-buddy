# Fountain Buddy Starter Script
# Captures stills from an RTSP stream (e.g., Lumus Pro) every N seconds
# Stores them in ~/FountainBuddy/YYYY-MM-DD/ directories

import os
import cv2
import time
from datetime import datetime

# === CONFIGURATION ===
RTSP_URL = "rtsp://your-camera-url-here"
CAPTURE_INTERVAL_SEC = 5  # Seconds between frames
SAVE_DIR = os.path.expanduser("~/FountainBuddy")

# === INITIALIZATION ===
os.makedirs(SAVE_DIR, exist_ok=True)
print(f"[INFO] Saving captures to: {SAVE_DIR}")

# Start RTSP stream
cap = cv2.VideoCapture(RTSP_URL)
if not cap.isOpened():
    print("[ERROR] Failed to connect to RTSP stream.")
    exit(1)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARNING] Failed to read frame. Retrying...")
            time.sleep(1)
            continue

        # Determine today's folder
        today = datetime.now().strftime("%Y-%m-%d")
        day_folder = os.path.join(SAVE_DIR, today)
        os.makedirs(day_folder, exist_ok=True)

        # Save frame
        timestamp = datetime.now().strftime("%H-%M-%S")
        filename = f"fountain_{timestamp}.jpg"
        path = os.path.join(day_folder, filename)
        cv2.imwrite(path, frame)
        print(f"[INFO] Saved: {path}")

        time.sleep(CAPTURE_INTERVAL_SEC)

except KeyboardInterrupt:
    print("[INFO] Stopped by user.")

cap.release()