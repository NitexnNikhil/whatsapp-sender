import re
import csv
import urllib.parse
import subprocess
import time
import sys
import os

# ─────────────────────────────────────────────
INPUT_FILE  = "input.txt"
OUTPUT_FILE = "output.csv"
# ─────────────────────────────────────────────

def extract_numbers(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    raw = re.findall(r'\+[\d\s\-]{7,20}', content)
    cleaned = []
    for num in raw:
        n = re.sub(r'[\s\-]', '', num)
        if re.match(r'^\+\d{10,15}$', n):
            cleaned.append(n)
    return cleaned

def save_csv(numbers, message, filepath):
    encoded = urllib.parse.quote(message)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Phone Number", "Message", "WhatsApp URL"])
        for num in numbers:
            url = f"https://wa.me/{num.lstrip('+')}?text={encoded}"
            writer.writerow([num, message, url])
    print(f"\n✅ CSV saved: {filepath}\n")

def open_whatsapp_desktop(number, message):
    encoded = urllib.parse.quote(message)
    whatsapp_url = f"whatsapp://send?phone={number.lstrip('+')}&text={encoded}"
    platform = sys.platform
    try:
        if platform == "win32":
            os.startfile(whatsapp_url)
        elif platform == "darwin":
            subprocess.Popen(["open", whatsapp_url])
        else:
            subprocess.Popen(["xdg-open", whatsapp_url])
        return True
    except Exception as e:
        print(f"   ❌ Error opening WhatsApp: {e}")
        return False

def send_messages(numbers, message):
    total = len(numbers)
    print(f"\n  Message : {message}")
    print("=" * 55)
    print("\n⚠️  Make sure WhatsApp Desktop app is INSTALLED & LOGGED IN!")
    print("   Download: https://www.whatsapp.com/download\n")
    input("   Press ENTER when ready to start sending...")

    for i, num in enumerate(numbers, 1):
        print(f"\n📤 [{i}/{total}] Opening WhatsApp Desktop for {num} ...")
        success = open_whatsapp_desktop(num, message)
        if success:
            print(f"   ⏳ Waiting 6 seconds for WhatsApp Desktop to load...")
            time.sleep(6)
            print(f"   ✅ Chat opened for {num} — click SEND in the app!")
        if i < total:
            input("\n   Press ENTER to open next number (or Ctrl+C to stop)...")

    print("\n🎉 All chats opened in WhatsApp Desktop!")
    print(f"📄 Check '{OUTPUT_FILE}' for a full record.")

# ── Main ──────────────────────────────────────
numbers = extract_numbers(INPUT_FILE)

if not numbers:
    print("❌ No valid phone numbers found in input.txt")
else:
    print("=" * 55)
    print("  WhatsApp Desktop Auto-Sender")
    print("=" * 55)
    print(f"  ✅ Numbers found: {len(numbers)}")
    for n in numbers:
        print(f"     {n}")
    print("=" * 55)
    print()
    MESSAGE = input("✏️  Type your message and press ENTER:\n> ").strip()

    if not MESSAGE:
        print("❌ No message entered. Exiting.")
    else:
        save_csv(numbers, MESSAGE, OUTPUT_FILE)
        send_messages(numbers, MESSAGE)



