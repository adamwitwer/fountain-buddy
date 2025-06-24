import os
import requests
import json
import time
import datetime
import sqlite3
import smtplib
import random
import string
import numpy as np # Often used with cv2 for image manipulation
import cv2
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from apscheduler.schedulers.background import BackgroundScheduler
from ultralytics import YOLO # Assuming YOLO is used as discussed

# Load environment variables from .env file
load_dotenv()

# Now access your variables using os.getenv()
CAMERA_IP = os.getenv("CAMERA_IP")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
RTSP_PORT = int(os.getenv("RTSP_PORT")) # Convert to int if it's a number
HTTP_PORT = int(os.getenv("HTTP_PORT"))
BASE_URL = os.getenv("BASE_URL")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH")
BIRD_CLASS_ID = int(os.getenv("BIRD_CLASS_ID"))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD"))
DETECTION_COOLDOWN_SECONDS = int(os.getenv("DETECTION_COOLDOWN_SECONDS"))

IMAGE_DIR = os.getenv("IMAGE_DIR", "bird_images")

# --- Global Variables for Token Management ---
current_token = None
token_expiry_time = 0

# --- Database Functions ---
DB_NAME = "fountain_buddy.db"
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bird_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            bird_type TEXT NOT NULL,
            image_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def record_bird_visit(bird_type, frame):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_filename = f"bird_{timestamp_str}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_filename)

    # Save the image
    cv2.imwrite(image_path, frame)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bird_visits (timestamp, bird_type, image_path) VALUES (?, ?, ?)",
                   (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bird_type, image_path))
    conn.commit()
    conn.close()
    print(f"Recorded bird visit: {bird_type} at {timestamp_str}")
    return image_path

# --- Reolink API Interaction Functions ---

def get_token():
    global current_token, token_expiry_time
    if current_token and time.time() < token_expiry_time:
        return current_token # Token is still valid

    print("Requesting new token...")
    login_cmd = {
        "cmd": "Login",
        "param": {
            "User": {
                "Version": "0", # Use version 0 as private encryption not public 
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
            lease_time = token_info['leaseTime'] # Lease time in seconds 
            token_expiry_time = time.time() + lease_time - 300 # Refresh 5 minutes before expiry
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

    cmd_payload = {
        "cmd": command,
        "action": action, # 0 for get value, 1 for get initial, range, value 
        "param": params if params is not None else {}
    }
    
    headers = {'Content-Type': 'application/json'}
    url = f"{BASE_URL}?cmd={command}&token={token}"

    try:
        response = requests.post(url, headers=headers, data=json.dumps([cmd_payload]), timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
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
    response_value = call_reolink_api("GetAbility", {"User": {"userName": USERNAME}}, action=0) # Get user-specific abilities 
    if response_value:
        return response_value.get("Ability", {}).get("abilityChn", [{}])[0] # Assuming channel 0 abilities 
    return {}

def get_md_state(channel=0):
    # Short session style URL is supported for GetMdState for convenience 
    # "https://IPC_IP/api.cgi?cmd=GetMdState&channel=0&token=TOKEN"
    token = get_token()
    if not token:
        print("Cannot get MD state without a token.")
        return None

    url = f"{BASE_URL}?cmd=GetMdState&channel={channel}&token={token}"
    try:
        response = requests.post(url, timeout=5) # No JSON body needed for this specific cmd 
        response.raise_for_status()
        res_json = response.json()
        if res_json and res_json[0]['code'] == 0:
            return res_json[0]['value']['state'] # 1 for detected, 0 for no motion 
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
        return response_value # Contains 'dog_cat', 'people', 'vehicle' states 
    return {}

def capture_snapshot(channel=0):
    # The 'rs' parameter is a random string to prevent browser caching 
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    token = get_token()
    if not token:
        print("Cannot capture snapshot without a token.")
        return None

    url = f"{BASE_URL}?cmd=Snap&channel={channel}&rs={random_str}&token={token}"
    try:
        # Snap command returns image/jpeg content directly 
        response = requests.get(url, timeout=10) # Use GET for Snap
        response.raise_for_status()
        
        if 'image/jpeg' in response.headers.get('Content-Type', ''):
            print(f"Snapshot captured successfully (channel {channel}).")
            return response.content # Raw image bytes
        else:
            print(f"Snap command did not return JPEG. Content-Type: {response.headers.get('Content-Type')}")
            print(f"Response text: {response.text}") # May contain API error JSON if not successful
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error capturing snapshot: {e}")
        return None

# --- Daily Summary Functions (as previously defined) ---
def generate_daily_summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=1)

    summary_data = {
        "total_visits": 0,
        "bird_counts": {},
        "sample_images": []
    }

    cursor.execute("""
        SELECT timestamp, bird_type, image_path
        FROM bird_visits
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp DESC
    """, (start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S")))

    visits = cursor.fetchall()
    conn.close()

    summary_data["total_visits"] = len(visits)

    for visit in visits:
        timestamp, bird_type, image_path = visit
        summary_data["bird_counts"][bird_type] = summary_data["bird_counts"].get(bird_type, 0) + 1

        if len(summary_data["sample_images"]) < 3 and image_path and os.path.exists(image_path):
            if image_path not in summary_data["sample_images"]:
                summary_data["sample_images"].append(image_path)

    summary_message = f"Daily Bird Fountain Summary for {end_time.strftime('%Y-%m-%d')}:\n\n"
    summary_message += f"Total bird visits: {summary_data['total_visits']}\n\n"
    summary_message += "Bird Type Counts:\n"
    if summary_data["bird_counts"]:
        for bird_type, count in summary_data["bird_counts"].items():
            summary_message += f"- {bird_type}: {count}\n"
    else:
        summary_message += "No specific bird types identified today.\n"

    return summary_message, summary_data["sample_images"]

def send_email_summary(summary_text, image_paths, recipient_email, sender_email, sender_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Daily Bird Fountain Activity Summary"

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
import random
import string
from ultralytics import YOLO

# Load the YOLOv8 model once
try:
    yolo_model = YOLO(YOLO_MODEL_PATH)
    print(f"YOLOv8 model loaded from {YOLO_MODEL_PATH}")
except Exception as e:
    print(f"Error loading YOLOv8 model: {e}. Please ensure the model file exists and is correct.")
    yolo_model = None # Set to None if loading fails

# Keep track of last detection times for cooldown
last_detection_time_bird = 0

def main_loop():
    global last_detection_time_bird
    
    ai_capabilities = get_ai_capabilities()
    supports_dog_cat_ai = ai_capabilities.get("supportAiAnimal", 0) == 1
    print(f"Camera supports Dog/Cat AI detection: {supports_dog_cat_ai}")

    while True:
        motion_detected = False
        if supports_dog_cat_ai:
            ai_state = get_ai_state()
            if ai_state and ai_state.get("dog_cat", {}).get("alarm_state") == 1:
                print("AI Dog/Cat alarm detected!")
                motion_detected = True
        
        if not motion_detected: # If AI didn't detect, check general MD
            md_state = get_md_state()
            if md_state == 1:
                print("General Motion Detected!")
                motion_detected = True

        if motion_detected:
            current_time = time.time()
            if (current_time - last_detection_time_bird) > DETECTION_COOLDOWN_SECONDS:
                print("Motion event triggering snapshot and bird detection...")
                snapshot_data = capture_snapshot()
                
                if snapshot_data:
                    # Convert snapshot data to OpenCV image format
                    np_array = np.frombuffer(snapshot_data, np.uint8)
                    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

                    if frame is not None and yolo_model:
                        results = yolo_model(frame, verbose=False)
                        birds_found = []
                        for r in results:
                            for box in r.boxes:
                                conf = box.conf[0].item()
                                cls = int(box.cls[0].item())
                                # Assuming COCO dataset where 'bird' is class 14
                                if conf > CONFIDENCE_THRESHOLD and cls == BIRD_CLASS_ID:
                                    # Optional: Draw bounding box for debugging if displaying frame
                                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                    cv2.putText(frame, f"Bird {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                    birds_found.append({"label": "bird", "confidence": conf}) # We can generalize this to "bird"

                        if birds_found:
                            print(f"Actual bird detected by YOLO! Found {len(birds_found)} instances.")
                            record_bird_visit("bird", frame) # Record with generic "bird" type
                            last_detection_time_bird = current_time
                        else:
                            print("No birds identified by YOLO, but motion/AI detected.")
                    else:
                        print("Could not decode snapshot or YOLO model not loaded.")
                else:
                    print("Failed to get snapshot from camera.")
            else:
                print(f"Motion detected, but within cooldown period ({DETECTION_COOLDOWN_SECONDS}s). Skipping detection.")
        
        time.sleep(1) # Poll every second for motion/AI events

if __name__ == "__main__":
    init_db()

    # Schedule the daily summary email
    scheduler = BackgroundScheduler()
    # Runs at 11:00 PM every day
    scheduler.add_job(lambda: send_email_summary(*generate_daily_summary(), RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD),
                      'cron', hour=23, minute=0)
    scheduler.start()

    print("Bird monitoring application started. Press Ctrl+C to exit.")
    try:
        main_loop()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown() # Shut down the scheduler cleanly
        print("Application stopped.")
