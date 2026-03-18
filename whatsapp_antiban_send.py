import re
import csv
import urllib.parse
import subprocess
import time
import sys
import os
import random

# ──────────────────────────────────────────────────────────────────────────
# CONFIGURATION & ANTI-BAN SETTINGS
# ──────────────────────────────────────────────────────────────────────────
INPUT_FILE        = "input.txt"
OUTPUT_FILE       = "output_log.csv"

# Anti-Abuse Parameters (2026 Standards)
BATCH_SIZE        = 15           # Pause after every 15 messages
LONG_BREAK_MIN    = 5            # Length of the batch pause (minutes)
SHORT_DELAY_RANGE = (8, 18)      # Human-mimicry delay between messages (seconds)

GREETINGS = ["Hi", "Hello", "Hey there", "Greetings", "Hey", "Hi there"]

# ──────────────────────────────────────────────────────────────────────────
# CORE FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────

def extract_numbers(filepath):
    """Finds phone numbers with international format in the input file."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Matches + followed by 10-15 digits, allowing for spaces/dashes
    raw = re.findall(r'\+[\d\s\-]{7,20}', content)
    cleaned = []
    for num in raw:
        n = re.sub(r'[\s\-]', '', num)
        if re.match(r'^\+\d{10,15}$', n):
            cleaned.append(n)
    return cleaned

def remove_duplicates(numbers):
    """Filters out duplicate numbers while preserving order."""
    seen = set()
    unique = []
    duplicates = []
    for num in numbers:
        if num in seen:
            duplicates.append(num)
        else:
            seen.add(num)
            unique.append(num)
    return unique, duplicates

def get_random_message(base_message):
    """Prefixes message with a random greeting to bypass simple pattern hashing."""
    return f"{random.choice(GREETINGS)}! {base_message}"

def smart_delay():
    """Simulates the time a human takes to read, paste, and click."""
    delay = random.uniform(*SHORT_DELAY_RANGE)
    print(f"   ⏳ Human-mimicry delay: {delay:.2f}s...")
    time.sleep(delay)

def save_log(numbers, message, filepath):
    """Saves a record of the numbers and the generated URLs."""
    encoded_base = urllib.parse.quote(message)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Phone Number", "Original Message", "WhatsApp URL"])
        for num in numbers:
            url = f"https://wa.me/{num.lstrip('+')}?text={encoded_base}"
            writer.writerow([num, message, url])
    print(f"\n Log saved: {filepath}\n")

def open_whatsapp_desktop(number, custom_message):
    """Triggers the OS to open the WhatsApp Desktop application."""
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
        print(f"Error triggering WhatsApp app: {e}")
        return False

def send_messages_smart(numbers, message):
    """Main loop with batching and randomized delays."""
    total = len(numbers)
    print(f"\n🚀 Starting Smart Sender | Total: {total} numbers")
    print("Ensure WhatsApp Desktop is OPEN and LOGGED IN.")
    input("Press ENTER to begin...")

    for i, num in enumerate(numbers, 1):
        # 1. Randomize content slightly per recipient
        custom_msg = get_random_message(message)
        
        # 2. Open the chat
        print(f"\n [{i}/{total}] Opening chat for {num}...")
        success = open_whatsapp_desktop(num, custom_msg)
        
        if success:
            # 3. Apply randomized delay before moving to next
            smart_delay()
            print(f"UI Triggered for {num} — Click 'Send' in the app!")
        
        # 4. Batch Cooling Logic
        if i % BATCH_SIZE == 0 and i < total:
            print(f"\n BATCH LIMIT ({BATCH_SIZE}) REACHED.")
            print(f"   Cooling down for {LONG_BREAK_MIN} minutes to protect account trust score...")
            for minute in range(LONG_BREAK_MIN, 0, -1):
                print(f" Resuming in {minute}m...", end="\r")
                time.sleep(60)
            print("\nCool-down complete. Resuming next batch...")

    print("\n\n ALL CHATS OPENED!")
    print("Note: If you receive 0 replies, STOP all activity for 24-48 hours.")

# ──────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ──────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    raw_numbers = extract_numbers(INPUT_FILE)

    if not raw_numbers:
        print(f" Error: No valid numbers found in {INPUT_FILE}")
        print("Ensure numbers are in international format (e.g., +1234567890)")
    else:
        unique_numbers, duplicates = remove_duplicates(raw_numbers)

        print("=" * 55)
        print("  WhatsApp Smart-Manual Desktop Tool")
        print("=" * 55)
        print(f"Unique numbers  : {len(unique_numbers)}")
        if duplicates:
            print(f"Duplicates skipped: {len(duplicates)}")
        print("=" * 55)

        MESSAGE = input("\nType your message body and press ENTER:\n> ").strip()

        if not MESSAGE:
            print("No message entered. Exiting.")
        else:
            save_log(unique_numbers, MESSAGE, OUTPUT_FILE)
            send_messages_smart(unique_numbers, MESSAGE)