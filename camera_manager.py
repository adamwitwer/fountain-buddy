#!/usr/bin/env python3
"""
Camera management class for multi-camera support.
Handles individual camera configurations, API calls, and location-specific settings.
"""

import os
import requests
import json
import time
import random
import string
from typing import Dict, Optional, Any

class CameraManager:
    """Manages a single camera's configuration and API interactions."""
    
    def __init__(self, camera_id: str, location: str, config: Dict[str, Any]):
        """
        Initialize camera manager.
        
        Args:
            camera_id: Unique identifier for this camera (e.g., 'fountain', 'peanut')
            location: Human-readable location name (e.g., 'fountain', 'peanut')
            config: Dictionary containing camera configuration
        """
        self.camera_id = camera_id
        self.location = location
        
        # Camera network configuration
        self.ip = config['ip']
        self.username = config['username']
        self.password = config['password']
        self.rtsp_port = config.get('rtsp_port', 554)
        self.http_port = config.get('http_port', 80)
        self.base_url = f"http://{self.ip}:{self.http_port}/cgi-bin/api.cgi"
        
        # Discord configuration
        self.webhook_url = config['webhook_url']
        self.channel_id = config['channel_id']
        
        # Location-specific bird species
        self.common_birds = config['common_birds']
        
        # Token management
        self.current_token = None
        self.token_expiry_time = 0
        
        # Image directory
        self.image_dir = os.path.join("bird_images", self.location)
        os.makedirs(self.image_dir, exist_ok=True)
        
        print(f"🎥 Initialized camera: {self.camera_id} at {self.ip} for {self.location}")
    
    def get_token(self) -> Optional[str]:
        """Get or refresh authentication token for camera API."""
        
        # Check if current token is still valid
        if self.current_token and time.time() < self.token_expiry_time:
            return self.current_token
        
        print(f"🔑 Requesting new token for {self.camera_id}...")
        
        login_cmd = {
            "cmd": "Login",
            "param": {
                "User": {
                    "Version": "0",
                    "userName": self.username,
                    "password": self.password
                }
            }
        }
        
        headers = {'Content-Type': 'application/json'}
        
        for i in range(2): # Try up to 2 times
            try:
                response = requests.post(
                    f"{self.base_url}?cmd=Login", 
                    headers=headers, 
                    data=json.dumps([login_cmd]), 
                    timeout=10
                )
                response.raise_for_status()
                
                res_json = response.json()
                if res_json and res_json[0]['code'] == 0:
                    token_info = res_json[0]['value']['Token']
                    self.current_token = token_info['name']
                    lease_time = token_info['leaseTime']
                    self.token_expiry_time = time.time() + lease_time - 300  # Refresh 5 minutes before expiry
                    
                    print(f"✅ Token obtained for {self.camera_id}: {self.current_token[:8]}... (expires in {lease_time}s)")
                    return self.current_token
                else:
                    print(f"❌ Failed to get token for {self.camera_id}: {res_json[0].get('error', {})}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Network error getting token for {self.camera_id}: {e}")
                if i == 0:
                    print(f"🔄 Retrying token request for {self.camera_id} in 1 second...")
                    time.sleep(1)
                    continue
                return None
    
    def call_api(self, command: str, params: Optional[Dict] = None, action: int = 0) -> Optional[Dict]:
        """Make an API call to the camera."""
        
        token = self.get_token()
        if not token:
            print(f"❌ Cannot proceed without token for {self.camera_id}")
            return None
        
        cmd_payload = {
            "cmd": command,
            "action": action,
            "param": params if params is not None else {}
        }
        
        headers = {'Content-Type': 'application/json'}
        url = f"{self.base_url}?cmd={command}&token={token}"
        
        for i in range(2): # Try up to 2 times
            try:
                response = requests.post(url, headers=headers, data=json.dumps([cmd_payload]), timeout=10)
                response.raise_for_status()
                
                res_json = response.json()
                if res_json and res_json[0]['code'] == 0:
                    return res_json[0].get('value')
                else:
                    # Check for login error (-6) and retry once.
                    if res_json and res_json[0].get('error', {}).get('rspCode') == -6:
                        print(f"🔑 Token expired for {self.camera_id} on API call '{command}'. Re-logging in.")
                        self.current_token = None  # Invalidate token
                        token = self.get_token()   # Get new token
                        if not token:
                            print(f"❌ Failed to get new token for {self.camera_id}. Aborting retry.")
                            return None
                        
                        # Retry the request with the new token
                        print(f"🔄 Retrying API call '{command}' for {self.camera_id} with new token.")
                        url = f"{self.base_url}?cmd={command}&token={token}"
                        try:
                            retry_response = requests.post(url, headers=headers, data=json.dumps([cmd_payload]), timeout=10)
                            retry_response.raise_for_status()
                            retry_res_json = retry_response.json()

                            if retry_res_json and retry_res_json[0]['code'] == 0:
                                print(f"✅ Retry successful for API call '{command}' on {self.camera_id}.")
                                return retry_res_json[0].get('value')
                            else:
                                # Even retry failed, so log and exit
                                error_details = retry_res_json[0].get('error', {}).get('detail', 'Unknown API Error on retry')
                                print(f"❌ Retry failed for API call '{command}' on {self.camera_id}: {error_details}")
                                return None
                        except requests.exceptions.RequestException as e:
                            print(f"❌ Network error on retry for {command} for {self.camera_id}: {e}")
                            return None
                        except json.JSONDecodeError:
                            print(f"❌ Failed to decode JSON response on retry for {command} on {self.camera_id}")
                            return None

                    error_details = res_json[0].get('error', {}).get('detail', 'Unknown API Error')
                    print(f"❌ API call {command} failed for {self.camera_id}: {error_details}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Network error calling {command} for {self.camera_id}: {e}")
                if i == 0:
                    print(f"🔄 Retrying API call '{command}' for {self.camera_id} in 1 second...")
                    time.sleep(1)
                    continue
                return None
            except json.JSONDecodeError:
                print(f"❌ Failed to decode JSON response for {command} on {self.camera_id}")
                return None
    
    def get_ai_capabilities(self) -> Dict:
        """Get AI detection capabilities for this camera."""
        
        response_value = self.call_api("GetAbility", {"User": {"userName": self.username}}, action=0)
        if response_value:
            return response_value.get("Ability", {}).get("abilityChn", [{}])[0]
        return {}
    
    def get_motion_state(self, channel: int = 0) -> Optional[int]:
        """Get motion detection state for this camera."""
        
        token = self.get_token()
        if not token:
            return None
        
        url = f"{self.base_url}?cmd=GetMdState&channel={channel}&token={token}"
        
        for i in range(2): # Try up to 2 times
            try:
                response = requests.post(url, timeout=5)
                response.raise_for_status()
                
                res_json = response.json()
                if res_json and res_json[0]['code'] == 0:
                    return res_json[0]['value']['state']  # 1 for detected, 0 for no motion
                else:
                    # Check for login error (-6) and retry once.
                    if res_json and res_json[0].get('error', {}).get('rspCode') == -6:
                        print(f"🔑 Token expired for {self.camera_id} during GetMdState. Re-logging in.")
                        self.current_token = None  # Invalidate token
                        token = self.get_token()   # Get new token
                        if not token:
                            print(f"❌ Failed to get new token for {self.camera_id}. Aborting GetMdState retry.")
                            return None
                        
                        # Retry the request with the new token
                        print(f"🔄 Retrying GetMdState for {self.camera_id} with new token.")
                        url = f"{self.base_url}?cmd=GetMdState&channel={channel}&token={token}"
                        try:
                            retry_response = requests.post(url, timeout=5)
                            retry_response.raise_for_status()
                            retry_res_json = retry_response.json()

                            if retry_res_json and retry_res_json[0]['code'] == 0:
                                print(f"✅ Retry successful for GetMdState on {self.camera_id}.")
                                return retry_res_json[0]['value']['state']
                            else:
                                error_details = retry_res_json[0].get('error', {}).get('detail', 'Unknown MD State Error on retry')
                                print(f"❌ Retry failed for GetMdState on {self.camera_id}: {error_details}")
                                return None
                        except requests.exceptions.RequestException as e:
                            print(f"❌ Network error on retry for GetMdState for {self.camera_id}: {e}")
                            return None
                        except json.JSONDecodeError:
                            print(f"❌ Failed to decode motion state response on retry for {self.camera_id}")
                            return None

                    error_details = res_json[0].get('error', {}).get('detail', 'Unknown MD State Error')
                    print(f"❌ Failed to get motion state for {self.camera_id}: {error_details}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Network error getting motion state for {self.camera_id}: {e}")
                if i == 0:
                    print(f"🔄 Retrying GetMdState for {self.camera_id} in 1 second...")
                    time.sleep(1)
                    continue
                return None
            except json.JSONDecodeError:
                print(f"❌ Failed to decode motion state response for {self.camera_id}")
                return None
    
    def get_ai_state(self, channel: int = 0) -> Dict:
        """Get AI detection state for this camera."""
        
        params = {"channel": channel}
        response_value = self.call_api("GetAiState", params, action=0)
        if response_value:
            return response_value
        return {}
    
    def capture_snapshot(self, channel: int = 0) -> Optional[bytes]:
        """Capture a snapshot from this camera."""
        
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        token = self.get_token()
        
        if not token:
            print(f"❌ Cannot capture snapshot from {self.camera_id} without token")
            return None
        
        url = f"{self.base_url}?cmd=Snap&channel={channel}&rs={random_str}&token={token}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            if 'image/jpeg' in response.headers.get('Content-Type', ''):
                print(f"📸 Snapshot captured from {self.camera_id}")
                return response.content
            else:
                print(f"❌ Snap command for {self.camera_id} did not return JPEG: {response.headers.get('Content-Type')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error capturing snapshot from {self.camera_id}: {e}")
            return None
    
    def motion_detected(self) -> bool:
        """Check if motion or AI detection is triggered for this camera."""
        
        # Check AI capabilities first
        ai_capabilities = self.get_ai_capabilities()
        supports_dog_cat_ai = ai_capabilities.get("supportAiDogCat", {}).get("permit", 0) > 0
        
        if supports_dog_cat_ai:
            # Use AI detection
            ai_state = self.get_ai_state()
            if ai_state and ai_state.get("dog_cat", {}).get("alarm_state") == 1:
                print(f"🤖 AI detection triggered on {self.camera_id}")
                return True
        else:
            # Fall back to motion detection
            motion_state = self.get_motion_state()
            if motion_state == 1:
                print(f"🏃 Motion detected on {self.camera_id}")
                return True
        
        return False
    
    def get_image_path(self, filename: str) -> str:
        """Get the full path for saving an image from this camera."""
        return os.path.join(self.image_dir, filename)
    
    def get_location_emoji(self) -> str:
        """Get emoji for this camera's location."""
        location_emojis = {
            'fountain': '🏛️',
            'peanut': '🥜'
        }
        return location_emojis.get(self.location, '📷')
    
    def __str__(self) -> str:
        """String representation of camera."""
        return f"Camera({self.camera_id}@{self.ip}:{self.location})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"CameraManager(id='{self.camera_id}', location='{self.location}', ip='{self.ip}')"


def create_camera_managers() -> Dict[str, CameraManager]:
    """Create camera managers from environment configuration."""
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Location-specific bird species lists
    FOUNTAIN_BIRDS = {
        1: "Northern Cardinal",
        2: "American Robin", 
        3: "Common Grackle",
        4: "Blue Jay",
        5: "Mourning Dove",
        6: "House Sparrow",
        7: "Gray Catbird",
        8: "House Finch",
        9: "Song Sparrow",
        10: "European Starling",
        11: "Carolina Wren"
    }
    
    PEANUT_BIRDS = {
        1: "Red-bellied Woodpecker",
        2: "Black-capped Chickadee",
        3: "Northern Flicker",
        4: "White-breasted Nuthatch",
        5: "Tufted Titmouse",
        6: "Carolina Wren",
        7: "European Starling",
        8: "Downy Woodpecker",
        9: "Hairy Woodpecker",
        10: "House Sparrow",
        11: "Gray Catbird"
    }
    
    cameras = {}
    
    # Fountain Camera
    fountain_config = {
        'ip': os.getenv('FOUNTAIN_CAMERA_IP'),
        'username': os.getenv('FOUNTAIN_USERNAME'),
        'password': os.getenv('FOUNTAIN_PASSWORD'),
        'rtsp_port': int(os.getenv('FOUNTAIN_RTSP_PORT', 554)),
        'http_port': int(os.getenv('FOUNTAIN_HTTP_PORT', 80)),
        'webhook_url': os.getenv('DISCORD_WEBHOOK_FOUNTAIN'),
        'channel_id': os.getenv('DISCORD_CHANNEL_FOUNTAIN_ID'),
        'common_birds': FOUNTAIN_BIRDS
    }
    
    if all([fountain_config['ip'], fountain_config['username'], fountain_config['password']]):
        cameras['fountain'] = CameraManager('fountain', 'fountain', fountain_config)
    else:
        print("⚠️ Fountain camera configuration incomplete")
    
    # Peanut Camera
    peanut_config = {
        'ip': os.getenv('PEANUT_CAMERA_IP'),
        'username': os.getenv('PEANUT_USERNAME'),
        'password': os.getenv('PEANUT_PASSWORD'),
        'rtsp_port': int(os.getenv('PEANUT_RTSP_PORT', 554)),
        'http_port': int(os.getenv('PEANUT_HTTP_PORT', 80)),
        'webhook_url': os.getenv('DISCORD_WEBHOOK_PEANUT'),
        'channel_id': os.getenv('DISCORD_CHANNEL_PEANUT_ID'),
        'common_birds': PEANUT_BIRDS
    }
    
    if all([peanut_config['ip'], peanut_config['username'], peanut_config['password']]):
        cameras['peanut'] = CameraManager('peanut', 'peanut', peanut_config)
    else:
        print("⚠️ Peanut camera configuration incomplete")
    
    print(f"🎥 Initialized {len(cameras)} cameras: {list(cameras.keys())}")
    return cameras


if __name__ == "__main__":
    # Test camera managers
    cameras = create_camera_managers()
    
    for camera_id, camera in cameras.items():
        print(f"\nTesting {camera_id} camera:")
        print(f"  Location: {camera.location}")
        print(f"  IP: {camera.ip}")
        print(f"  Species count: {len(camera.common_birds)}")
        print(f"  Image directory: {camera.image_dir}")
        
        # Test token acquisition
        token = camera.get_token()
        if token:
            print(f"  ✅ Token acquired: {token[:8]}...")
        else:
            print(f"  ❌ Failed to get token")
