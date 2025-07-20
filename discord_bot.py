#!/usr/bin/env python3
"""
Discord bot for processing human bird identification responses.
This bot listens for messages in the bird identification channel and updates the database.
"""

import os
import discord
import asyncio
import sqlite3
import re
from dotenv import load_dotenv
from run import update_bird_species_from_human, parse_human_response, COMMON_BIRDS

# Load environment variables
load_dotenv()

# Discord configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Multi-channel support
FOUNTAIN_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_FOUNTAIN_ID")) if os.getenv("DISCORD_CHANNEL_FOUNTAIN_ID") else None
PEANUT_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_PEANUT_ID")) if os.getenv("DISCORD_CHANNEL_PEANUT_ID") else None

# Backwards compatibility
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID")) if os.getenv("DISCORD_CHANNEL_ID") else FOUNTAIN_CHANNEL_ID

# Channel to location mapping
CHANNEL_LOCATIONS = {}
if FOUNTAIN_CHANNEL_ID:
    CHANNEL_LOCATIONS[FOUNTAIN_CHANNEL_ID] = 'fountain'
if PEANUT_CHANNEL_ID:
    CHANNEL_LOCATIONS[PEANUT_CHANNEL_ID] = 'peanut'

# Location-specific bird species (imported from camera_manager)
from camera_manager import create_camera_managers

# Get camera managers to access species lists
try:
    cameras = create_camera_managers()
    LOCATION_BIRDS = {
        'fountain': cameras.get('fountain', {}).common_birds if 'fountain' in cameras else COMMON_BIRDS,
        'peanut': cameras.get('peanut', {}).common_birds if 'peanut' in cameras else {}
    }
except:
    # Fallback if camera_manager fails
    LOCATION_BIRDS = {
        'fountain': COMMON_BIRDS,
        'peanut': {}
    }

# Setup Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'🤖 Discord bot logged in as {client.user}')
    
    # Monitor multiple channels
    monitored_channels = []
    
    for channel_id, location in CHANNEL_LOCATIONS.items():
        channel = client.get_channel(channel_id)
        if channel:
            monitored_channels.append(f'#{channel.name} ({location})')
            print(f'👁️ Monitoring {location} channel: #{channel.name}')
        else:
            print(f'❌ Could not find {location} channel with ID: {channel_id}')
    
    if not monitored_channels:
        print('⚠️ No Discord channels configured for monitoring')
    else:
        print(f'🔄 Monitoring {len(monitored_channels)} channels: {", ".join(monitored_channels)}')

@client.event
async def on_message(message):
    # Don't respond to the bot's own messages or webhook messages
    if message.author == client.user or message.webhook_id:
        return
    
    # Check if message is in a monitored channel
    if message.channel.id not in CHANNEL_LOCATIONS:
        return
    
    # Get the location for this channel
    location = CHANNEL_LOCATIONS[message.channel.id]
    
    # Parse the human response using location-specific species list
    species_name = parse_human_response_for_location(message.content, location)
    
    if not species_name:
        # Not a valid bird identification response
        return
    
    print(f"📝 Human identification received from {location}: '{message.content}' → {species_name}")
    
    # Find the bird filename associated with this conversation
    # If replying to a message, get filename from that specific message
    # Otherwise, find the most recent bird detection
    target_filename = None
    
    referenced_msg = None
    if message.reference and message.reference.message_id:
        # User is replying to a specific message - find filename from that message
        try:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_filename = extract_filename_from_message(referenced_msg)
            print(f"🎯 Reply detected - using filename from referenced message: {target_filename}")
        except:
            print("⚠️ Could not fetch referenced message")
    
    if not target_filename:
        # Fallback: find most recent bird detection
        target_filename = await find_recent_bird_filename(message.channel)
        print(f"🔍 Using most recent bird filename: {target_filename}")
    
    if target_filename:
        result = update_bird_species_from_human(target_filename, species_name)
        
        # Handle both old boolean return and new dict return for backwards compatibility
        if isinstance(result, dict) and result.get("success"):
            is_correction = result.get("is_correction", False)
            old_species = result.get("old_species")
            
            # Send confirmation in Discord
            if is_correction:
                if message.content.isdigit():
                    response = f"🔄 **Correction accepted!** Changed from **{old_species}** → **{species_name}** (#{message.content})"
                else:
                    response = f"🔄 **Correction accepted!** Changed from **{old_species}** → **{species_name}**"
                await message.add_reaction("🔄")
            else:
                if message.content.isdigit():
                    response = f"✅ Thanks! Identified as **{species_name}** (#{message.content})"
                else:
                    response = f"✅ Thanks! Identified as **{species_name}**"
                await message.add_reaction("✅")
            
            await message.reply(response, mention_author=False)
            
            # Add appropriate reaction to the original bird detection message if this was a reply
            if referenced_msg:
                try:
                    if is_correction:
                        await referenced_msg.add_reaction("🔄")
                    else:
                        await referenced_msg.add_reaction("✅")
                    print(f"{'🔄' if is_correction else '✅'} Added reaction to original message")
                except Exception as e:
                    print(f"⚠️ Could not add reaction to referenced message: {e}")
            
            action = "corrected" if is_correction else "identified"
            print(f"✅ Successfully {action}: {species_name}")
            
        elif result:  # Old boolean return format
            # Send confirmation in Discord
            if message.content.isdigit():
                response = f"✅ Thanks! Identified as **{species_name}** (#{message.content})"
            else:
                response = f"✅ Thanks! Identified as **{species_name}**"
            
            await message.add_reaction("✅")
            await message.reply(response, mention_author=False)
            
            # Add green checkmark to the original bird detection message if this was a reply
            if referenced_msg:
                try:
                    await referenced_msg.add_reaction("✅")
                    print(f"✅ Added checkmark to original message")
                except Exception as e:
                    print(f"⚠️ Could not add reaction to referenced message: {e}")
            
            print(f"✅ Successfully processed identification: {species_name}")
        else:
            await message.add_reaction("❌")
            await message.reply("❌ Sorry, couldn't update the database. Please try again.", mention_author=False)
            print(f"❌ Failed to update database for: {species_name}")
    else:
        await message.add_reaction("❓")
        await message.reply("❓ Couldn't find a recent bird image to identify. Please make sure you're responding to a recent detection.", mention_author=False)
        print("❓ No recent bird filename found for identification")

def parse_human_response_for_location(message_content, location):
    """Parse human response using location-specific species list."""
    
    content = message_content.strip()
    
    # Get species list for this location
    location_birds = LOCATION_BIRDS.get(location, {})
    
    # Check if it's a numbered response
    if content.isdigit():
        number = int(content)
        if number in location_birds:
            return location_birds[number]
        else:
            return None  # Invalid number for this location
    
    # Check if it's a direct species name
    # Clean up the input and capitalize properly
    if len(content) > 1:
        return content.title()
    
    return None

def extract_filename_from_message(message):
    """Extract filename from a Discord message."""
    
    try:
        # Look for filename in message content
        if "📁 File:" in message.content:
            filename_match = re.search(r'📁 File: `([^`]+)`', message.content)
            if filename_match:
                return filename_match.group(1)
        
        # Also check attachments as backup
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.startswith('bird_') and attachment.filename.endswith('.jpg'):
                    return attachment.filename
        
        return None
        
    except Exception as e:
        print(f"❌ Error extracting filename from message: {e}")
        return None

async def find_recent_bird_filename(channel):
    """Find the filename from the most recent bird detection message."""
    
    try:
        # Look at the last 10 messages in the channel
        async for msg in channel.history(limit=10):
            # Skip user messages, only look at webhook/bot messages
            if not msg.webhook_id and msg.author != client.user:
                continue
                
            # Look for filename in message content
            if "📁 File:" in msg.content:
                # Extract filename using regex
                filename_match = re.search(r'📁 File: `([^`]+)`', msg.content)
                if filename_match:
                    return filename_match.group(1)
            
            # Also check if message has attachments (backup method)
            if msg.attachments:
                for attachment in msg.attachments:
                    if attachment.filename.startswith('bird_') and attachment.filename.endswith('.jpg'):
                        return attachment.filename
        
        return None
        
    except Exception as e:
        print(f"❌ Error finding recent filename: {e}")
        return None

def run_discord_bot():
    """Run the Discord bot."""
    
    if not DISCORD_BOT_TOKEN:
        print("❌ DISCORD_BOT_TOKEN not configured. Discord bot disabled.")
        return
    
    if not CHANNEL_LOCATIONS:
        print("❌ No Discord channels configured. Discord bot disabled.")
        print("   Please set DISCORD_CHANNEL_FOUNTAIN_ID and/or DISCORD_CHANNEL_PEANUT_ID")
        return
    
    print(f"🚀 Starting Discord bot for multi-channel bird identification...")
    print(f"   Monitoring {len(CHANNEL_LOCATIONS)} channels: {list(CHANNEL_LOCATIONS.values())}")
    
    try:
        client.run(DISCORD_BOT_TOKEN)
    except discord.LoginFailure:
        print("❌ Discord bot login failed. Check DISCORD_BOT_TOKEN.")
    except Exception as e:
        print(f"❌ Discord bot error: {e}")

async def test_bot_functionality():
    """Test the bot's core functions without running the full bot."""
    
    print("🧪 Testing Discord bot functionality...")
    
    # Test parsing
    test_responses = ["1", "3", "Northern Cardinal", "gray catbird", "Blue Jay"]
    
    for response in test_responses:
        species = parse_human_response(response)
        print(f"   '{response}' → {species}")
    
    print("✅ Bot functionality tests complete")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        asyncio.run(test_bot_functionality())
    else:
        # Run the bot
        run_discord_bot()