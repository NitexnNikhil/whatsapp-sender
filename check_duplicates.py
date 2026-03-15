import re

# ─────────────────────────────────────────────
INPUT_FILE = "input.txt"
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

def check_duplicates(numbers):
    seen = {}
    for num in numbers:
        seen[num] = seen.get(num, 0) + 1

    duplicates = {num: count for num, count in seen.items() if count > 1}
    unique     = [num for num, count in seen.items() if count == 1]

    return unique, duplicates

# ── Main ──────────────────────────────────────
numbers = extract_numbers(INPUT_FILE)

if not numbers:
    print("❌ No valid phone numbers found in input.txt")
else:
    unique, duplicates = check_duplicates(numbers)

    print("=" * 45)
    print("       Duplicate Number Checker")
    print("=" * 45)
    print(f"  📋 Total numbers found  : {len(numbers)}")
    print(f"  ✅ Unique numbers        : {len(unique)}")
    print(f"  🔁 Duplicate numbers     : {len(duplicates)}")
    print("=" * 45)

    if duplicates:
        print("\n🔁 Duplicate Numbers (with occurrence count):\n")
        for num, count in duplicates.items():
            print(f"   {num}  →  appeared {count} times")
    else:
        print("\n✅ No duplicates found!")

    print("\n✅ Unique Numbers:\n")
    for num in unique:
        print(f"   {num}")