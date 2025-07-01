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
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID")) if os.getenv("DISCORD_CHANNEL_ID") else None

# Setup Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'🤖 Discord bot logged in as {client.user}')
    if DISCORD_CHANNEL_ID:
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            print(f'👁️ Monitoring channel: #{channel.name}')
        else:
            print(f'❌ Could not find channel with ID: {DISCORD_CHANNEL_ID}')
    else:
        print('⚠️ No DISCORD_CHANNEL_ID configured')

@client.event
async def on_message(message):
    # Don't respond to the bot's own messages or webhook messages
    if message.author == client.user or message.webhook_id:
        return
    
    # Only process messages in the bird identification channel
    if DISCORD_CHANNEL_ID and message.channel.id != DISCORD_CHANNEL_ID:
        return
    
    # Parse the human response
    species_name = parse_human_response(message.content)
    
    if not species_name:
        # Not a valid bird identification response
        return
    
    print(f"📝 Human identification received: '{message.content}' → {species_name}")
    
    # Find the most recent bird detection that needs identification
    # Look for recent messages from webhook (bot messages) containing file names
    recent_filename = await find_recent_bird_filename(message.channel)
    
    if recent_filename:
        success = update_bird_species_from_human(recent_filename, species_name)
        
        if success:
            # Send confirmation in Discord
            if message.content.isdigit():
                response = f"✅ Thanks! Identified as **{species_name}** (#{message.content})"
            else:
                response = f"✅ Thanks! Identified as **{species_name}**"
            
            await message.add_reaction("✅")
            await message.reply(response, mention_author=False)
            print(f"✅ Successfully processed identification: {species_name}")
        else:
            await message.add_reaction("❌")
            await message.reply("❌ Sorry, couldn't update the database. Please try again.", mention_author=False)
            print(f"❌ Failed to update database for: {species_name}")
    else:
        await message.add_reaction("❓")
        await message.reply("❓ Couldn't find a recent bird image to identify. Please make sure you're responding to a recent detection.", mention_author=False)
        print("❓ No recent bird filename found for identification")

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
    
    if not DISCORD_CHANNEL_ID:
        print("❌ DISCORD_CHANNEL_ID not configured. Discord bot disabled.")
        return
    
    print("🚀 Starting Discord bot for bird identification...")
    
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