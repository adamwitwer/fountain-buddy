#!/usr/bin/env python3
"""
Test script for Discord webhook integration.
This will test sending a bird image to Discord using the test webhook.
"""

import os
import requests
import glob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord webhooks
DISCORD_WEBHOOK_TEST = "https://discord.com/api/webhooks/1389645282916171816/LwXQ-jI-mOkpeQ8v3TToN94kmwuW1TG22evVG2X00lCB5pDfTJJL85S2BtlIQS75bUKY"
DISCORD_WEBHOOK_PROD = "https://discord.com/api/webhooks/1389645614777761832/czp2n9HedKhUex37Bs4xgpNJvVyeP9hs8q6kCOXJgXvIA6jKmWFDmJIc1fKurB7Obubb"

# Common bird species for testing
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

def test_discord_webhook(use_test_webhook=True):
    """Test the Discord webhook with a sample bird image."""
    
    webhook_url = DISCORD_WEBHOOK_TEST if use_test_webhook else DISCORD_WEBHOOK_PROD
    channel_name = "#bird-id-test" if use_test_webhook else "#bird-id"
    
    print(f"🧪 Testing Discord webhook for {channel_name}")
    print(f"🔗 Webhook URL: {webhook_url[:50]}...")
    
    # Find a test image (use existing bird crop if available, or any bird image)
    test_image_path = None
    
    # First try to find the bird crop from previous testing
    if os.path.exists("bird_crop_1.jpg"):
        test_image_path = "bird_crop_1.jpg"
        print(f"📷 Using test crop: {test_image_path}")
    else:
        # Look for any bird image in the Desktop folder
        bird_images = glob.glob("/Users/adam/Desktop/bird_images/*.jpg")
        if bird_images:
            test_image_path = bird_images[0]
            print(f"📷 Using bird image: {os.path.basename(test_image_path)}")
        else:
            print("❌ No test images found")
            return False
    
    if not test_image_path or not os.path.exists(test_image_path):
        print("❌ Test image not found")
        return False
    
    try:
        # Create test message with numbered options
        message_lines = [
            f"🧪 **TEST: Bird identification system**",
            f"🐦 **New bird detected!** YOLO confidence: 0.85",
            f"🤖 AI thinks: Common Grackle (0.73)",
            "",
            "**What species is this? Reply with number:**",
        ]
        
        # Add numbered common birds
        for num, species in COMMON_BIRDS.items():
            message_lines.append(f"{num}. {species}")
        
        message_lines.extend([
            "",
            "**Or reply with the species name for others**",
            f"📁 File: `{os.path.basename(test_image_path)}`",
            "",
            "*This is a test message - the system is working!*"
        ])
        
        message_content = "\n".join(message_lines)
        
        # Send the image with message
        with open(test_image_path, 'rb') as f:
            files = {'file': (os.path.basename(test_image_path), f, 'image/jpeg')}
            data = {'content': message_content}
            
            print("📤 Sending test message to Discord...")
            response = requests.post(webhook_url, data=data, files=files, timeout=15)
            response.raise_for_status()
            
        print(f"✅ Test message sent successfully to {channel_name}!")
        print(f"🔍 Check Discord to see the message with numbered bird options")
        print(f"💬 Try replying with a number (1-10) or bird species name")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_both_webhooks():
    """Test both test and production webhooks."""
    print("🚀 Testing Discord Webhook Integration")
    print("=" * 40)
    
    print("\n1️⃣ Testing #bird-id-test channel...")
    test_success = test_discord_webhook(use_test_webhook=True)
    
    if test_success:
        print("\n2️⃣ Testing #bird-id production channel...")
        prod_success = test_discord_webhook(use_test_webhook=False)
        
        if prod_success:
            print("\n🎉 Both webhooks working perfectly!")
            print("📝 Ready to add to .env file:")
            print(f"DISCORD_WEBHOOK_TEST={DISCORD_WEBHOOK_TEST}")
            print(f"DISCORD_WEBHOOK_PROD={DISCORD_WEBHOOK_PROD}")
            print("USE_DISCORD=true")
        else:
            print("\n⚠️ Test webhook works, but production webhook failed")
    else:
        print("\n❌ Test webhook failed - check the URL and permissions")

if __name__ == "__main__":
    test_both_webhooks()