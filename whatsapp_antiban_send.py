import re
import csv
import urllib.parse
import subprocess
import time
import sys
import os
import random

# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------
INPUT_FILE         = "input.txt"
MESSAGE_FILE       = "message.md"
SENT_REGISTRY_FILE = "sent_numbers.txt"

# Anti-Ban Constants (High Safety)
BATCH_SIZE         = 10            # Messages per batch
LONG_BREAK_MIN     = 60            # Minutes to wait after a batch
SHORT_DELAY_RANGE  = (280, 320)    # ~5 minute delay between messages

GREETINGS = ["Hi", "Hello", "Hey there", "Greetings", "Hey", "Hi there"]

# --------------------------------------------------------------------------
# DATA PERSISTENCE FUNCTIONS
# --------------------------------------------------------------------------

def get_already_sent():
    """Load history of sent numbers to avoid duplicates."""
    if not os.path.exists(SENT_REGISTRY_FILE):
        return set()
    with open(SENT_REGISTRY_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def mark_as_sent(number):
    """Log a number to the registry immediately after triggering."""
    with open(SENT_REGISTRY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{number}\n")

def get_random_message_variant(filepath):
    """Reads all lines from message.md and returns one random variant."""
    if not os.path.exists(filepath):
        return "Hi, this is Nikhil from Bootcoding."
    with open(filepath, "r", encoding="utf-8") as f:
        # Filter out empty lines and strip whitespace
        variants = [line.strip() for line in f if line.strip()]
    
    if not variants:
        return "Hi, this is Nikhil from Bootcoding."
    
    return random.choice(variants)

# --------------------------------------------------------------------------
# PROCESSING FUNCTIONS
# --------------------------------------------------------------------------

def extract_numbers(filepath):
    """Extract and clean international format numbers."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    raw = re.findall(r'\+[\d\s\-]{7,20}', content)
    cleaned = []
    for num in raw:
        n = re.sub(r'[\s\-]', '', num)
        if re.match(r'^\+\d{10,15}$', n):
            cleaned.append(n)
    return cleaned

def open_whatsapp_desktop(number, custom_message):
    """Trigger the system to open WhatsApp Desktop with the message."""
    encoded = urllib.parse.quote(custom_message)
    whatsapp_url = f"whatsapp://send?phone={number.lstrip('+')}&text={encoded}"
    try:
        if sys.platform == "win32":
            os.startfile(whatsapp_url)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", whatsapp_url])
        else:
            subprocess.Popen(["xdg-open", whatsapp_url])
        return True
    except Exception as e:
        print(f"System Error: {e}")
        return False

def run_sender():
    # 1. Load Data
    raw_list = extract_numbers(INPUT_FILE)
    history = get_already_sent()
    
    # 2. Filter out duplicates and previously sent numbers
    unique_to_send = []
    seen_in_run = set()
    for n in raw_list:
        if n not in history and n not in seen_in_run:
            unique_to_send.append(n)
            seen_in_run.add(n)

    total = len(unique_to_send)
    if total == 0:
        print("No new numbers to process. Session aborted.")
        return

    print("-" * 40)
    print(f"Total new numbers: {total}")
    print(f"Batch Size: {BATCH_SIZE} | Wait: 5m | Break: 60m")
    print("-" * 40)
    input("Press Enter to begin sending...")

    for i, num in enumerate(unique_to_send, 1):
        # Pick a fresh variant and a random greeting for every single person
        base_body = get_random_message_variant(MESSAGE_FILE)
        full_msg = f"{random.choice(GREETINGS)}! {base_body}"
        
        print(f"[{i}/{total}] Opening chat for {num}...")
        success = open_whatsapp_desktop(num, full_msg)
        
        if success:
            mark_as_sent(num)
            
            # Handle Delays
            if i < total:
                if i % BATCH_SIZE == 0:
                    print(f"Batch {i//BATCH_SIZE} done. Waiting {LONG_BREAK_MIN} minutes...")
                    for m in range(LONG_BREAK_MIN, 0, -1):
                        print(f"Resuming in {m}m...  ", end="\r")
                        time.sleep(60)
                else:
                    delay = random.uniform(*SHORT_DELAY_RANGE)
                    print(f"Waiting {delay/60:.2f} minutes before next...")
                    time.sleep(delay)

    print("\nAll tasks finished. Logged to sent_numbers.txt.")

if __name__ == "__main__":
    run_sender()