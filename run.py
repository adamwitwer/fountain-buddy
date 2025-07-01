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
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from PIL import Image

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

# Discord webhook URLs for bird identification
DISCORD_WEBHOOK_TEST = os.getenv("DISCORD_WEBHOOK_TEST")
DISCORD_WEBHOOK_PROD = os.getenv("DISCORD_WEBHOOK_PROD")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")  # Channel ID for production
USE_DISCORD = os.getenv("USE_DISCORD", "false").lower() == "true"

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
            species TEXT,
            confidence REAL,
            image_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def record_bird_visit(bird_type, frame, species=None, species_confidence=None):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Include species in filename if available
    if species and species != "Unknown Bird Species":
        species_clean = species.replace(" ", "_").replace("(", "").replace(")", "")
        image_filename = f"bird_{species_clean}_{timestamp_str}.jpg"
    else:
        image_filename = f"bird_{timestamp_str}.jpg"
    
    image_path = os.path.join(IMAGE_DIR, image_filename)

    # Save the image
    cv2.imwrite(image_path, frame)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bird_visits (timestamp, bird_type, species, confidence, image_path) VALUES (?, ?, ?, ?, ?)",
                   (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bird_type, species, species_confidence, image_path))
    conn.commit()
    conn.close()
    
    species_info = f" ({species}, {species_confidence:.2f})" if species else ""
    print(f"Recorded bird visit: {bird_type}{species_info} at {timestamp_str}")
    return image_path

# --- Discord Bird Identification Functions ---

# Common bird species in order of frequency (based on your local area)
COMMON_BIRDS = {
    1: "Northern Cardinal",
    2: "American Robin", 
    3: "Common Grackle",
    4: "Blue Jay",
    5: "Mourning Dove",
    6: "House Sparrow",
    7: "American Goldfinch",
    8: "Red-winged Blackbird",
    9: "House Finch",
    10: "Gray Catbird"
}

def send_bird_to_discord(image_path, yolo_confidence, ai_species=None, ai_confidence=None):
    """Send bird image to Discord for human identification."""
    
    if not USE_DISCORD:
        return
    
    webhook_url = DISCORD_WEBHOOK_PROD  # Use production webhook
    if not webhook_url:
        print("❌ Discord webhook not configured")
        return
    
    try:
        # Create the message with numbered options
        message_lines = [
            f"🐦 **New bird detected!** YOLO confidence: {yolo_confidence:.2f}",
        ]
        
        if ai_species and ai_confidence:
            message_lines.append(f"🤖 AI thinks: {ai_species} ({ai_confidence:.2f})")
        
        message_lines.extend([
            "",
            "**What species is this? Reply with number:**",
        ])
        
        # Add numbered common birds
        for num, species in COMMON_BIRDS.items():
            message_lines.append(f"{num}. {species}")
        
        message_lines.extend([
            "",
            "**Or reply with the species name for others**",
            f"📁 File: `{os.path.basename(image_path)}`"
        ])
        
        message_content = "\n".join(message_lines)
        
        # Send the image with message
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            data = {'content': message_content}
            
            response = requests.post(webhook_url, data=data, files=files, timeout=10)
            response.raise_for_status()
            
        print(f"✅ Bird image sent to Discord: {os.path.basename(image_path)}")
        
    except Exception as e:
        print(f"❌ Failed to send to Discord: {e}")

def update_bird_species_from_human(filename, human_species, human_confidence=1.0):
    """Update bird species in database based on human identification."""
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Find the record by image filename
        cursor.execute("""
            SELECT id, image_path, species FROM bird_visits 
            WHERE image_path LIKE ?
            ORDER BY timestamp DESC LIMIT 1
        """, (f"%{filename}%",))
        
        result = cursor.fetchone()
        if not result:
            print(f"❌ No database record found for {filename}")
            return False
        
        record_id, old_image_path, old_species = result
        
        # Update the species and confidence in database
        cursor.execute("""
            UPDATE bird_visits 
            SET species = ?, confidence = ? 
            WHERE id = ?
        """, (human_species, human_confidence, record_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Updated database: {filename} → {human_species}")
        
        # Rename the image file to include correct species
        if old_image_path and os.path.exists(old_image_path):
            new_filename = rename_image_with_species(old_image_path, human_species)
            if new_filename:
                # Update database with new filename
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("UPDATE bird_visits SET image_path = ? WHERE id = ?", 
                             (new_filename, record_id))
                conn.commit()
                conn.close()
                print(f"✅ Renamed image: {os.path.basename(old_image_path)} → {os.path.basename(new_filename)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating species: {e}")
        return False

def rename_image_with_species(old_path, species_name):
    """Rename image file to include the correct species name."""
    
    try:
        # Extract timestamp from old filename
        old_filename = os.path.basename(old_path)
        
        # Look for timestamp pattern (YYYY-MM-DD_HH-MM-SS)
        import re
        timestamp_match = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', old_filename)
        
        if timestamp_match:
            timestamp = timestamp_match.group(0)
            
            # Create new filename with species
            species_clean = species_name.replace(" ", "_").replace("(", "").replace(")", "")
            new_filename = f"bird_{species_clean}_{timestamp}.jpg"
            new_path = os.path.join(os.path.dirname(old_path), new_filename)
            
            # Rename the file
            os.rename(old_path, new_path)
            return new_path
        else:
            print(f"⚠️ Could not extract timestamp from {old_filename}")
            return old_path
            
    except Exception as e:
        print(f"❌ Error renaming image: {e}")
        return old_path

def parse_human_response(message_content):
    """Parse human response to extract species identification."""
    
    content = message_content.strip()
    
    # Check if it's a numbered response
    if content.isdigit():
        number = int(content)
        if number in COMMON_BIRDS:
            return COMMON_BIRDS[number]
        else:
            return None  # Invalid number
    
    # Check if it's a direct species name
    # Clean up the input and capitalize properly
    if len(content) > 1:
        return content.title()
    
    return None

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
        SELECT timestamp, bird_type, species, confidence, image_path
        FROM bird_visits
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp DESC
    """, (start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S")))

    visits = cursor.fetchall()
    conn.close()

    summary_data["total_visits"] = len(visits)

    for visit in visits:
        timestamp, bird_type, species, confidence, image_path = visit
        # Use species if available, otherwise fall back to bird_type
        display_name = species if species else bird_type
        summary_data["bird_counts"][display_name] = summary_data["bird_counts"].get(display_name, 0) + 1

        if len(summary_data["sample_images"]) < 3 and image_path and os.path.exists(image_path):
            if image_path not in summary_data["sample_images"]:
                summary_data["sample_images"].append(image_path)

    summary_message = f"Daily Bird Fountain Summary for {end_time.strftime('%Y-%m-%d')}:\n\n"
    summary_message += f"Total bird visits: {summary_data['total_visits']}\n\n"
    summary_message += "Bird Species Counts:\n"
    if summary_data["bird_counts"]:
        for species_name, count in summary_data["bird_counts"].items():
            summary_message += f"- {species_name}: {count}\n"
    else:
        summary_message += "No specific bird species identified today.\n"

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

# Load bird species classification model
bird_classifier = None
try:
    # Using ResNet50 pre-trained on ImageNet (includes many bird species)
    print("Loading bird species classifier...")
    bird_classifier = ResNet50(weights='imagenet')
    print("Bird species classifier loaded successfully")
except Exception as e:
    print(f"Error loading bird species classifier: {e}. Species identification will be disabled.")
    bird_classifier = None

# Keep track of last detection times for cooldown
last_detection_time_bird = 0

def classify_bird_species(image_crop):
    """
    Classify bird species from a cropped image containing a bird.
    Returns (species_name, confidence) or (None, 0) if classification fails.
    """
    if bird_classifier is None:
        return None, 0
    
    try:
        # Resize image to 224x224 as expected by ResNet50
        pil_image = Image.fromarray(cv2.cvtColor(image_crop, cv2.COLOR_BGR2RGB))
        pil_image = pil_image.resize((224, 224))
        
        # Convert to numpy array and preprocess for ResNet50
        img_array = np.array(pil_image)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Run inference
        predictions = bird_classifier.predict(img_array, verbose=0)
        
        # Decode predictions to get readable labels
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        
        # Look for bird-related classifications
        for i, (imagenet_id, label, confidence) in enumerate(decoded_predictions):
            # Check if this is a bird species (ImageNet has many bird classes)
            if is_bird_species(label):
                species_name = format_species_name(label)
                return species_name, float(confidence)
        
        # If no bird species found in top 3, return the top prediction anyway
        _, label, confidence = decoded_predictions[0]
        species_name = format_species_name(label)
        return species_name, float(confidence)
        
    except Exception as e:
        print(f"Error in bird species classification: {e}")
        return None, 0

def is_bird_species(label):
    """
    Check if the ImageNet label represents a bird species.
    """
    bird_keywords = [
        'robin', 'jay', 'cardinal', 'sparrow', 'finch', 'dove', 'pigeon',
        'crow', 'raven', 'hawk', 'eagle', 'owl', 'woodpecker', 'wren',
        'chickadee', 'nuthatch', 'warbler', 'thrush', 'flycatcher',
        'vireo', 'tanager', 'bunting', 'oriole', 'blackbird', 'grackle',
        'starling', 'swallow', 'martin', 'swift', 'hummingbird', 'kingfisher',
        'flicker', 'sapsucker', 'kingbird', 'phoebe', 'pewee', 'martin',
        'goldfinch', 'siskin', 'canary', 'redstart', 'chat', 'mockingbird',
        'catbird', 'thrasher', 'shrike', 'magpie', 'tit', 'chickadee'
    ]
    
    label_lower = label.lower()
    return any(keyword in label_lower for keyword in bird_keywords)

def format_species_name(label):
    """
    Format the ImageNet label into a readable species name.
    """
    # Remove underscores and capitalize words
    formatted = label.replace('_', ' ').title()
    
    # Remove common ImageNet artifacts
    formatted = formatted.replace(',', ' -')
    
    return formatted

def main_loop():
    global last_detection_time_bird
    
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
            if (current_time - last_detection_time_bird) > DETECTION_COOLDOWN_SECONDS:
                print("Motion event triggering snapshot and bird detection...")
                snapshot_data = capture_snapshot()
                
                if snapshot_data:
                    # Convert snapshot data to OpenCV image format
                    np_array = np.frombuffer(snapshot_data, np.uint8)
                    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

                    if frame is not None and yolo_model:
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        results = yolo_model(frame_rgb, verbose=False)
                        birds_found = []
                        bird_crops = []
                        for r in results:
                            for box in r.boxes:
                                conf = box.conf[0].item()
                                cls = int(box.cls[0].item())
                                # Assuming COCO dataset where 'bird' is class 14
                                if conf > CONFIDENCE_THRESHOLD and cls == BIRD_CLASS_ID:
                                    # Get bounding box coordinates
                                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                                    
                                    # Extract bird crop for species classification
                                    bird_crop = frame[y1:y2, x1:x2]
                                    bird_crops.append(bird_crop)
                                    
                                    # Optional: Draw bounding box for debugging if displaying frame
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                    cv2.putText(frame, f"Bird {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                    birds_found.append({"label": "bird", "confidence": conf})

                        if birds_found:
                            print(f"Actual bird detected by YOLO! Found {len(birds_found)} instances.")
                            
                            # Classify species for the first (largest) bird detection
                            species_name = None
                            species_confidence = None
                            if bird_crops and bird_classifier:
                                try:
                                    # Use the largest bird crop for species classification
                                    largest_crop = max(bird_crops, key=lambda crop: crop.shape[0] * crop.shape[1])
                                    species_name, species_confidence = classify_bird_species(largest_crop)
                                    if species_name:
                                        print(f"Species identified: {species_name} (confidence: {species_confidence:.2f})")
                                except Exception as e:
                                    print(f"Error during species classification: {e}")
                            
                            image_path = record_bird_visit("bird", frame, species_name, species_confidence)
                            
                            # Send to Discord for human identification
                            if USE_DISCORD:
                                # Get the highest YOLO confidence from detections
                                max_yolo_confidence = max(bird['confidence'] for bird in birds_found)
                                send_bird_to_discord(image_path, max_yolo_confidence, species_name, species_confidence)
                            
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