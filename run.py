import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

import requests
import json
import time
import datetime
import sqlite3
import smtplib
import random
import string
import numpy as np
import cv2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from apscheduler.schedulers.background import BackgroundScheduler
from ultralytics import YOLO

# Access your variables using os.getenv()
CAMERA_IP = os.getenv("CAMERA_IP")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
RTSP_PORT = int(os.getenv("RTSP_PORT"))
HTTP_PORT = int(os.getenv("HTTP_PORT"))
BASE_URL = os.getenv("BASE_URL")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH")
# --- NEW: Define a map of class IDs to animal names ---
# NOTE: These IDs are based on the standard COCO dataset.
# You will NEED a custom-trained model to detect 'squirrel', 'raccoon', and 'fox'.
# When you have a custom model, you must update the class IDs below to match your model's classes.
ANIMAL_CLASS_MAP = {
    14: "bird",
    15: "cat",
    16: "dog", # Often mistaken for foxes or raccoons by general models
    # Example IDs for a custom model (update these with your actual IDs)
    # 23: "squirrel",
    # 24: "raccoon",
    # 25: "fox",
}

CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD"))
DETECTION_COOLDOWN_SECONDS = int(os.getenv("DETECTION_COOLDOWN_SECONDS"))

# --- RENAMED: Directory for all animal images ---
IMAGE_DIR = os.getenv("IMAGE_DIR", "animal_images")

# --- Global Variables for Token Management ---
current_token = None
token_expiry_time = 0

# --- RENAMED: Database to be more generic ---
DB_NAME = "animal_watcher.db"

# --- UPDATED: Database function for new schema ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create a table for 'animal_visits' instead of 'bird_visits'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animal_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            animal_type TEXT NOT NULL,
            image_path TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- RENAMED & UPDATED: Function to record any animal visit ---
def record_animal_visit(animal_type, frame):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_filename = f"{animal_type}_{timestamp_str}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_filename)

    # Save the image
    cv2.imwrite(image_path, frame)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Insert into the new 'animal_visits' table
    cursor.execute("INSERT INTO animal_visits (timestamp, animal_type, image_path) VALUES (?, ?, ?)",
                   (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), animal_type, image_path))
    conn.commit()
    conn.close()
    print(f"Recorded animal visit: {animal_type} at {timestamp_str}")
    return image_path

# --- Reolink API Interaction Functions (No changes needed here) ---

def get_token():
    global current_token, token_expiry_time
    if current_token and time.time() < token_expiry_time:
        return current_token

    print("Requesting new token...")
    login_cmd = {
        "cmd": "Login",
        "param": {
            "User": {
                "Version": "0",
                "userName": USERNAME,
                "password": PASSWORD
            }
        }
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(f"{BASE_URL}?cmd=Login", headers=headers, data=json.dumps([login_cmd]), timeout=10)
        response.raise_for_status()
        res_json = response.json()
        if res_json and res_json[0]['code'] == 0:
            token_info = res_json[0]['value']['Token']
            current_token = token_info['name']
            lease_time = token_info['leaseTime']
            token_expiry_time = time.time() + lease_time - 300
            print(f"Successfully obtained token: {current_token}. Expires in {lease_time} seconds.")
            return current_token
        else:
            print(f"Failed to get token: {res_json[0].get('error', {})}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error during login: {e}")
        return None

def call_reolink_api(command, params=None, action=0):
    token = get_token()
    if not token:
        print("Cannot proceed without a valid token.")
        return None

    cmd_payload = { "cmd": command, "action": action, "param": params if params is not None else {} }
    headers = {'Content-Type': 'application/json'}
    url = f"{BASE_URL}?cmd={command}&token={token}"

    try:
        response = requests.post(url, headers=headers, data=json.dumps([cmd_payload]), timeout=10)
        response.raise_for_status()
        res_json = response.json()
        if res_json and res_json[0]['code'] == 0:
            return res_json[0].get('value')
        else:
            error_details = res_json[0].get('error', {}).get('detail', 'Unknown API Error')
            print(f"API call for {command} failed with code {res_json[0]['code']}: {error_details}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error calling {command}: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON response for {command}: {response.text}")
        return None

def get_ai_capabilities():
    response_value = call_reolink_api("GetAbility", {"User": {"userName": USERNAME}}, action=0)
    if response_value:
        return response_value.get("Ability", {}).get("abilityChn", [{}])[0]
    return {}

def get_md_state(channel=0):
    token = get_token()
    if not token:
        print("Cannot get MD state without a token.")
        return None
    url = f"{BASE_URL}?cmd=GetMdState&channel={channel}&token={token}"
    try:
        response = requests.post(url, timeout=5)
        response.raise_for_status()
        res_json = response.json()
        if res_json and res_json[0]['code'] == 0:
            return res_json[0]['value']['state']
        else:
            error_details = res_json[0].get('error', {}).get('detail', 'Unknown MD State Error')
            print(f"Failed to get MD state: {error_details}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error getting MD state: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON response for GetMdState: {response.text}")
        return None

def get_ai_state(channel=0):
    params = {"channel": channel}
    response_value = call_reolink_api("GetAiState", params, action=0)
    if response_value:
        return response_value
    return {}

def capture_snapshot(channel=0):
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    token = get_token()
    if not token:
        print("Cannot capture snapshot without a token.")
        return None
    url = f"{BASE_URL}?cmd=Snap&channel={channel}&rs={random_str}&token={token}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if 'image/jpeg' in response.headers.get('Content-Type', ''):
            print(f"Snapshot captured successfully (channel {channel}).")
            return response.content
        else:
            print(f"Snap command did not return JPEG. Content-Type: {response.headers.get('Content-Type')}")
            print(f"Response text: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error capturing snapshot: {e}")
        return None

def create_daily_collage(image_paths, max_images=70, thumb_width=320, thumb_height=240, cols=7):
    """
    Creates a single collage image from a list of image paths.

    Args:
        image_paths (list): A list of paths to the images for the collage.
        max_images (int): The maximum number of images to include in the collage.
        thumb_width (int): The width of each thumbnail in the collage.
        thumb_height (int): The height of each thumbnail in the collage.
        cols (int): The number of columns in the collage grid.

    Returns:
        str: The file path to the saved collage image, or None if no images were processed.
    """
    if not image_paths:
        print("No images to create a collage from.")
        return None

    # Limit the number of images to keep the collage from getting excessively large
    image_paths = image_paths[:max_images]
    
    # Calculate grid size
    num_images = len(image_paths)
    rows = (num_images + cols - 1) // cols

    # Create a blank canvas for the collage
    collage_height = rows * thumb_height
    collage_width = cols * thumb_width
    collage = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)

    print(f"Creating a {cols}x{rows} collage for {num_images} images...")

    for i, img_path in enumerate(image_paths):
        if not os.path.exists(img_path):
            continue

        try:
            # Read and resize the image
            img = cv2.imread(img_path)
            img = cv2.resize(img, (thumb_width, thumb_height))

            # --- Add text overlay (animal type and time) ---
            try:
                # Extract info from filename like 'bird_2025-06-25_21-15-30.jpg'
                filename = os.path.basename(img_path)
                parts = filename.replace('.jpg', '').split('_')
                animal_type = parts[0].capitalize()
                time_str = parts[2].replace('-', ':')
                label = f"{animal_type} @ {time_str}"
                
                # Add a semi-transparent background for the text
                cv2.rectangle(img, (0, thumb_height - 22), (thumb_width, thumb_height), (0, 0, 0), -1)
                # Add the text
                cv2.putText(img, label, (5, thumb_height - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            except Exception as e:
                print(f"Could not parse filename '{img_path}': {e}")


            # Calculate position in the grid
            row = i // cols
            col = i % cols
            y_offset = row * thumb_height
            x_offset = col * thumb_width

            # Paste the thumbnail onto the canvas
            collage[y_offset:y_offset + thumb_height, x_offset:x_offset + thumb_width] = img

        except Exception as e:
            print(f"Could not process image {img_path}: {e}")
            continue # Skip corrupted or unreadable images

    # Save the final collage image
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d")
    collage_filename = f"collage_{timestamp_str}.jpg"
    collage_path = os.path.join(IMAGE_DIR, collage_filename)
    cv2.imwrite(collage_path, collage)
    print(f"Collage saved to {collage_path}")

    return collage_path

# --- UPDATED: Daily summary function to be more generic ---
def generate_daily_summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=1)

    summary_data = {
        "total_visits": 0,
        "animal_counts": {},
        "all_images": [] # We will now fetch all image paths
    }

    # Query the 'animal_visits' table for all visits in the last 24 hours
    cursor.execute("""
        SELECT animal_type, image_path
        FROM animal_visits
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC 
    """, (start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S")))

    visits = cursor.fetchall()
    conn.close()

    summary_data["total_visits"] = len(visits)

    for visit in visits:
        animal_type, image_path = visit
        summary_data["animal_counts"][animal_type] = summary_data["animal_counts"].get(animal_type, 0) + 1
        if image_path and os.path.exists(image_path):
             summary_data["all_images"].append(image_path)


    # --- Integration of the collage ---
    # Create the collage from all the images gathered
    collage_path = create_daily_collage(summary_data["all_images"])
    
    # The list of attachments for the email will now be just the collage
    attachments = [collage_path] if collage_path else []

    # --- Generate the text summary ---
    summary_message = f"Daily Animal Activity Summary for {end_time.strftime('%Y-%m-%d')}:\n\n"
    summary_message += f"Total animal visits: {summary_data['total_visits']}\n"
    if summary_data["total_visits"] > 0:
        summary_message += f"A collage of today's visitors is attached.\n\n"
    
    summary_message += "Visit Counts:\n"
    if summary_data["animal_counts"]:
        for animal_type, count in summary_data["animal_counts"].items():
            summary_message += f"- {animal_type.capitalize()}: {count}\n"
    else:
        summary_message += "No animals were identified today.\n"

    # Return the text and the path to the collage
    return summary_message, attachments

# --- UPDATED: Email function for new subject line ---
def send_email_summary(summary_text, image_paths, recipient_email, sender_email, sender_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Daily Fountain Animal Activity Summary" # Updated subject

    msg.attach(MIMEText(summary_text, 'plain'))

    for img_path in image_paths:
        try:
            with open(img_path, 'rb') as fp:
                img = MIMEImage(fp.read(), name=os.path.basename(img_path))
            msg.attach(img)
        except Exception as e:
            print(f"Could not attach image {img_path}: {e}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Email summary sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# --- Main Application Logic ---
# Load the YOLOv8 model once
try:
    yolo_model = YOLO(YOLO_MODEL_PATH)
    print(f"YOLOv8 model loaded from {YOLO_MODEL_PATH}")
except Exception as e:
    print(f"Error loading YOLOv8 model: {e}. Please ensure the model file exists and is correct.")
    yolo_model = None

# --- UPDATED: Use a single global cooldown timer ---
last_detection_time = 0

# --- UPDATED: Main loop for multi-animal detection ---
def main_loop():
    global last_detection_time
    
    ai_capabilities = get_ai_capabilities()
    supports_dog_cat_ai = ai_capabilities.get("supportAiDogCat", {}).get("permit", 0) > 0
    print(f"Camera supports Dog/Cat AI detection: {supports_dog_cat_ai}")

    while True:
        motion_detected = False
        if supports_dog_cat_ai:
            ai_state = get_ai_state()
            if ai_state and ai_state.get("dog_cat", {}).get("alarm_state") == 1:
                print("AI Dog/Cat alarm detected!")
                motion_detected = True
        else:
            md_state = get_md_state()
            if md_state == 1:
                print("General Motion Detected!")
                motion_detected = True

        if motion_detected:
            current_time = time.time()
            if (current_time - last_detection_time) > DETECTION_COOLDOWN_SECONDS:
                print("Motion event triggering snapshot and analysis...")
                snapshot_data = capture_snapshot()
                
                if snapshot_data:
                    np_array = np.frombuffer(snapshot_data, np.uint8)
                    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

                    if frame is not None and yolo_model:
                        results = yolo_model(frame, verbose=False)
                        
                        detections = []
                        for r in results:
                            for box in r.boxes:
                                conf = box.conf[0].item()
                                cls = int(box.cls[0].item())
                                
                                # Check if the detected class is in our animal map
                                if conf > CONFIDENCE_THRESHOLD and cls in ANIMAL_CLASS_MAP:
                                    animal_name = ANIMAL_CLASS_MAP[cls]
                                    detections.append({
                                        "name": animal_name,
                                        "confidence": conf,
                                        "box": box.xyxy[0].tolist()
                                    })
                                    print(f"YOLO found: {animal_name} with confidence {conf:.2f}")

                        if detections:
                            # Prioritize birds. First, check if any birds were detected.
                            bird_detections = [d for d in detections if d['name'] == 'bird']
                            
                            if bird_detections:
                                # If birds are present, record the one with the highest confidence
                                best_detection = max(bird_detections, key=lambda x: x['confidence'])
                                print(f"Bird detected! Recording visit for 'bird'.")
                            else:
                                # If no birds, record the highest confidence non-bird animal
                                best_detection = max(detections, key=lambda x: x['confidence'])
                                print(f"Non-bird animal detected: {best_detection['name']}. Recording visit.")

                            animal_to_record = best_detection['name']
                            
                            # Draw box for the recorded detection on the saved frame
                            x1, y1, x2, y2 = map(int, best_detection['box'])
                            label = f"{animal_to_record} {best_detection['confidence']:.2f}"
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                            record_animal_visit(animal_to_record, frame)
                            last_detection_time = current_time # Reset cooldown
                        else:
                            print("Motion detected, but no target animals identified by YOLO.")
                    else:
                        print("Could not decode snapshot or YOLO model not loaded.")
                else:
                    print("Failed to get snapshot from camera.")
            else:
                print(f"Motion detected, but within cooldown period ({DETECTION_COOLDOWN_SECONDS}s). Skipping detection.")
        
        time.sleep(1)

if __name__ == "__main__":
    init_db()

    scheduler = BackgroundScheduler()
    # Schedule the daily summary at 11:00 PM
    scheduler.add_job(lambda: send_email_summary(*generate_daily_summary(), RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD),
                      'cron', hour=23, minute=0)
    scheduler.start()

    print("Multi-animal monitoring application started. Press Ctrl+C to exit.")
    try:
        main_loop()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Application stopped.")