# Python 3.12 compatibility fix - must be imported before TensorFlow
try:
    import distutils
except ImportError:
    import sys
    import importlib.util
    from unittest.mock import MagicMock
    
    # Create minimal distutils replacement for TensorFlow
    distutils_spec = importlib.util.spec_from_loader("distutils", loader=None)
    distutils_module = importlib.util.module_from_spec(distutils_spec)
    distutils_module.version = MagicMock()
    distutils_module.spawn = MagicMock()
    distutils_module.util = MagicMock()
    
    sys.modules["distutils"] = distutils_module
    sys.modules["distutils.version"] = distutils_module.version
    sys.modules["distutils.spawn"] = distutils_module.spawn
    sys.modules["distutils.util"] = distutils_module.util

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
from custom_bird_classifier import CustomBirdClassifier
from auto_retrain import AutoRetrainer
from camera_manager import CameraManager, create_camera_managers

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
ACTIVE_IMAGE_DIR = os.path.join(IMAGE_DIR, "active")

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

def record_bird_visit(bird_type, frame, camera_manager, species=None, species_confidence=None):
    """Record a bird visit with location awareness."""
    
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Include species in filename if available
    if species and species != "Unknown Bird Species":
        species_clean = species.replace(" ", "_").replace("(", "").replace(")", "")
        image_filename = f"bird_{species_clean}_{timestamp_str}.jpg"
    else:
        image_filename = f"bird_{timestamp_str}.jpg"
    
    image_path = camera_manager.get_image_path(image_filename)

    # Save the image
    cv2.imwrite(image_path, frame)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bird_visits (timestamp, bird_type, species, confidence, image_path, location, camera_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        bird_type, species, species_confidence, image_path,
        camera_manager.location, camera_manager.camera_id
    ))
    conn.commit()
    conn.close()
    
    species_info = f" ({species}, {species_confidence:.2f})" if species else ""
    location_emoji = camera_manager.get_location_emoji()
    print(f"{location_emoji} Recorded bird visit: {bird_type}{species_info} at {camera_manager.location} - {timestamp_str}")
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
    8: "European Starling",
    9: "House Finch",
    10: "Gray Catbird"
}

def send_bird_to_discord(image_path, camera_manager, yolo_confidence, ai_species=None, ai_confidence=None):
    """Send bird image to Discord for human identification."""
    
    if not USE_DISCORD:
        return
    
    webhook_url = camera_manager.webhook_url
    if not webhook_url:
        print(f"❌ Discord webhook not configured for {camera_manager.location}")
        return
    
    try:
        location_emoji = camera_manager.get_location_emoji()
        location_name = camera_manager.location.title()
        
        # Create the message with numbered options
        message_lines = [
            f"{location_emoji} **New bird at {location_name}!** YOLO confidence: {yolo_confidence:.2f}",
        ]
        
        if ai_species and ai_confidence:
            message_lines.append(f"🤖 AI thinks: {ai_species} ({ai_confidence:.2f})")
        
        message_lines.extend([
            "",
            "**What species is this? Reply with number:**",
        ])
        
        # Add numbered common birds for this location
        for num, species in camera_manager.common_birds.items():
            message_lines.append(f"{num}. {species}")
        
        message_lines.extend([
            "",
            "**Or reply with the species name for others**",
            f"📁 File: `{os.path.basename(image_path)}`",
            f"📍 Location: {location_name}"
        ])
        
        message_content = "\n".join(message_lines)
        
        # Send the image with message
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            data = {'content': message_content}
            
            response = requests.post(webhook_url, data=data, files=files, timeout=10)
            response.raise_for_status()
            
        print(f"✅ Bird image sent to Discord ({location_name}): {os.path.basename(image_path)}")
        
    except Exception as e:
        print(f"❌ Failed to send to Discord ({camera_manager.location}): {e}")

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
        
        # Check if this is a correction (species was already identified by human)
        # Allow unlimited corrections - any change from previous species is a correction
        is_correction = old_species and old_species != "Unknown Bird" and old_species != human_species
        
        # Track if this was already human-verified (confidence = 1.0 means human identification)
        cursor.execute("SELECT confidence FROM bird_visits WHERE id = ?", (record_id,))
        confidence_result = cursor.fetchone()
        was_human_verified = confidence_result and confidence_result[0] == 1.0
        
        # This is a re-correction if it was already human-verified
        is_recorrection = is_correction and was_human_verified
        
        # Update the species and confidence in database
        cursor.execute("""
            UPDATE bird_visits 
            SET species = ?, confidence = ? 
            WHERE id = ?
        """, (human_species, human_confidence, record_id))
        
        conn.commit()
        conn.close()
        
        if is_recorrection:
            print(f"🔁 Re-corrected identification: {old_species} → {human_species}")
        elif is_correction:
            print(f"🔄 Corrected identification: {old_species} → {human_species}")
        else:
            print(f"✅ Updated database: {filename} → {human_species}")
        
        # Handle image file renaming
        if old_image_path and os.path.exists(old_image_path):
            new_filename = rename_image_with_species(old_image_path, human_species)
            if new_filename and new_filename != old_image_path:
                # Update database with new filename
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("UPDATE bird_visits SET image_path = ? WHERE id = ?", 
                             (new_filename, record_id))
                conn.commit()
                conn.close()
                
                if is_recorrection:
                    print(f"🔁 Renamed re-corrected image: {os.path.basename(old_image_path)} → {os.path.basename(new_filename)}")
                elif is_correction:
                    print(f"🔄 Renamed corrected image: {os.path.basename(old_image_path)} → {os.path.basename(new_filename)}")
                else:
                    print(f"✅ Renamed image: {os.path.basename(old_image_path)} → {os.path.basename(new_filename)}")
        
        return {"success": True, "is_correction": is_correction, "is_recorrection": is_recorrection, "old_species": old_species}
        
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
            
            # Check if new filename is different from current
            if new_path == old_path:
                # No change needed
                return old_path
            
            # Check if target file already exists (shouldn't happen, but safety check)
            if os.path.exists(new_path):
                print(f"⚠️ Target file {new_filename} already exists, skipping rename")
                return old_path
            
            # Rename the file
            os.rename(old_path, new_path)
            return new_path
        else:
            print(f"⚠️ Could not extract timestamp from {old_filename}")
            return old_path
            
    except FileNotFoundError:
        print(f"⚠️ Original file {old_path} not found (may have been renamed already)")
        # Try to find the file with the new species name
        directory = os.path.dirname(old_path)
        old_filename = os.path.basename(old_path)
        timestamp_match = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', old_filename)
        
        if timestamp_match:
            timestamp = timestamp_match.group(0)
            species_clean = species_name.replace(" ", "_").replace("(", "").replace(")", "")
            new_filename = f"bird_{species_clean}_{timestamp}.jpg"
            new_path = os.path.join(directory, new_filename)
            return new_path
        
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

def check_for_model_updates():
    """Check if model needs retraining"""
    try:
        retrainer = AutoRetrainer(min_new_samples=15)
        if retrainer.check_and_retrain():
            # Reload the custom classifier with new model
            print("Model retrained successfully, reloading custom classifier...")
            custom_classifier.load_model()
            print("Custom classifier reloaded with updated model")
            return True
        return False
    except Exception as e:
        print(f"Error checking for model updates: {e}")
        return False

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

# Initialize custom bird classifier
custom_classifier = CustomBirdClassifier()
custom_classifier.load_model()

# Keep track of last detection times for cooldown
last_detection_time_bird = 0

def original_classify_bird_species(image_crop):
    """
    Original ImageNet-based bird species classification (fallback).
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

def classify_bird_species(image_crop):
    """Classify bird species using custom model (ImageNet disabled)"""
    try:
        if custom_classifier.is_loaded:
            result = custom_classifier.predict(image_crop)
            print(f"Custom classifier: {result['species']} ({result['confidence']:.2f})")
            if result['confidence'] > 0.15:  # Lower threshold for custom model
                return result['species'], result['confidence']
            else:
                print(f"Low confidence ({result['confidence']:.2f}), marking as Unknown Bird")
                return "Unknown Bird", result['confidence']
    except Exception as e:
        print(f"Custom classifier error: {e}")
    
    # No ImageNet fallback - return Unknown Bird
    return "Unknown Bird", 0.0

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

def process_bird_detection(camera_manager):
    """Process bird detection for a specific camera."""
    
    print(f"{camera_manager.get_location_emoji()} Motion/AI triggered on {camera_manager.location} camera")
    snapshot_data = camera_manager.capture_snapshot()
    
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
                        
                        # Optional: Draw bounding box for debugging
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"Bird {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        birds_found.append({"label": "bird", "confidence": conf})

            if birds_found:
                print(f"🐦 Bird detected by YOLO at {camera_manager.location}! Found {len(birds_found)} instances.")
                
                # Classify species for the first (largest) bird detection
                species_name = None
                species_confidence = None
                if bird_crops:
                    try:
                        # Use the largest bird crop for species classification
                        largest_crop = max(bird_crops, key=lambda crop: crop.shape[0] * crop.shape[1])
                        species_name, species_confidence = classify_bird_species(largest_crop)
                        if species_name:
                            print(f"🤖 Species identified: {species_name} (confidence: {species_confidence:.2f})")
                    except Exception as e:
                        print(f"❌ Error during species classification: {e}")
                
                # Record the bird visit
                image_path = record_bird_visit("bird", frame, camera_manager, species_name, species_confidence)
                
                # Send to Discord for human identification
                if USE_DISCORD:
                    # Get the highest YOLO confidence from detections
                    max_yolo_confidence = max(bird['confidence'] for bird in birds_found)
                    send_bird_to_discord(image_path, camera_manager, max_yolo_confidence, species_name, species_confidence)
                
                return True
            else:
                print(f"🔍 No birds identified by YOLO at {camera_manager.location}, but motion/AI detected.")
        else:
            print(f"❌ Could not decode snapshot from {camera_manager.location} or YOLO model not loaded.")
    else:
        print(f"❌ Failed to get snapshot from {camera_manager.location} camera.")
    
    return False

def main_loop():
    """Main detection loop for multiple cameras."""
    
    # Initialize camera managers
    cameras = create_camera_managers()
    
    if not cameras:
        print("❌ No cameras configured. Please check your .env file.")
        return
    
    print(f"🚀 Starting multi-camera bird detection with {len(cameras)} cameras:")
    for camera_id, camera in cameras.items():
        print(f"   📷 {camera_id}: {camera.location} at {camera.ip}")
    
    # Track last detection time per camera to implement cooldown
    last_detection_times = {camera_id: 0 for camera_id in cameras.keys()}
    
    print(f"🔄 Monitoring {len(cameras)} cameras for bird activity...")
    
    while True:
        for camera_id, camera_manager in cameras.items():
            try:
                # Check if motion/AI is detected for this camera
                if camera_manager.motion_detected():
                    current_time = time.time()
                    
                    # Check cooldown period for this specific camera
                    if (current_time - last_detection_times[camera_id]) > DETECTION_COOLDOWN_SECONDS:
                        # Process bird detection for this camera
                        if process_bird_detection(camera_manager):
                            last_detection_times[camera_id] = current_time
                    else:
                        remaining_cooldown = DETECTION_COOLDOWN_SECONDS - (current_time - last_detection_times[camera_id])
                        print(f"⏳ {camera_manager.location} camera in cooldown ({remaining_cooldown:.1f}s remaining)")
                        
            except Exception as e:
                print(f"❌ Error processing {camera_id} camera: {e}")
                time.sleep(5)  # Brief pause before retrying this camera
        
        time.sleep(1)  # Poll every second for motion/AI events

if __name__ == "__main__":
    init_db()

    # Schedule the daily summary email and model update check
    scheduler = BackgroundScheduler()
    
    # Runs at 11:00 PM every day
    def daily_tasks():
        # Check for model updates first
        check_for_model_updates()
        # Then send daily summary
        send_email_summary(*generate_daily_summary(), RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD)
    
    scheduler.add_job(daily_tasks, 'cron', hour=23, minute=0)
    scheduler.start()

    print("Bird monitoring application started. Press Ctrl+C to exit.")
    try:
        main_loop()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown() # Shut down the scheduler cleanly
        print("Application stopped.")