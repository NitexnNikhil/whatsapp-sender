# 🛡️ WhatsApp Smart-Manual Sender (2026 Edition)

A Python-based semi-automated messaging utility designed to minimize account risk by mimicking human behavior and respecting WhatsApp’s 2026 behavioral detection logic.

---

## 📖 How It Works (Anti-Ban Strategy)

Unlike standard "loops" that trigger a ban within minutes, this script operates on a **Human Mimicry Framework**. It uses four specific layers of protection:

1.  **Randomized Jitter (8–18s):** Bots are perfectly consistent; humans are messy. The script varies the wait time between each chat to break "mechanical" signatures.
2.  **Batch Cooling (The 15/5 Rule):** High-velocity bursts are a major red flag. Every 15 messages, the script pauses for 5 minutes to reset the "Activity Velocity" counter.
3.  **Greeting Randomization (Hash Breaking):** Sending identical text to 100+ people triggers "Pattern Tracking." By rotating greetings (*Hi, Hey, Hello*), we change the message's digital fingerprint.
4.  **OS-Native Hook:** It does not use "headless" browsers (like Selenium). It uses the official `whatsapp://` URI, which is the safest way to interact with the Desktop app.

---

## ⚙️ Configuration

| Variable | Recommended Value | Purpose |
| :--- | :--- | :--- |
| `BATCH_SIZE` | `15` | How many messages to send before a long break. |
| `LONG_BREAK_MIN`| `5` | Minutes to "cool down" the account reputation. |
| `SHORT_DELAY` | `8-18s` | Time to simulate "reading and clicking." |

---

## 🚦 Usage Instructions

1.  **Preparation:** Ensure your `input.txt` contains numbers in the format `+1234567890`.
2.  **App Setup:** Open the **WhatsApp Desktop App** and ensure you are logged in.
3.  **Run:** Execute the script. It will open the chat and pre-fill the message.
4.  **Action:** You must **manually click "Send"** or press Enter in the WhatsApp window. 
    > *Note: This manual step is intentional. It ensures the interaction is registered as "User Initiated" by the OS.*

---

## ⚠️ The "Red Line" (Survival Tips)

Even with this script, you are subject to the **3-Report Rule**. 

* **Priority 1:** Only message people who have a reason to hear from you.
* **The Reply Ratio:** If your "Sent-to-Reply" ratio drops below 10%, stop immediately. High un-replied volume is the #1 indicator of spam to the AI.
* **The Address Book:** If a user saves your number, you become "immune" to most automated filters. Your first message should encourage them to save your contact.

---

## 📄 Disclaimer
This tool is for responsible communication. Excessive messaging to strangers *will* eventually lead to account restriction or a permanent ban. Use at your own risk.