### First oopen your whatsapp web

### Now go to the group where you want all members phone number


## Now click on inspect and in the console *** Follow this below command ***
```bash
// Extract phone numbers from WhatsApp Web group member list
let numbers = new Set();

// Find all span elements
document.querySelectorAll("span").forEach(span => {
    let text = span.innerText;
    if (text && text.match(/\+\d+/)) {
        numbers.add(text.trim());
    }
});

console.log("Extracted Numbers:");
console.log([...numbers].join("\n"));
```



### Fetch all number but just scroll at bottom first then slowly slowly get upwards

```bash
(async () => {
    console.log("🚀 Starting Aggressive Full Export...");
    const allNumbers = new Set();
    
    // 1. Find the actual scrollable div (WhatsApp's sidebar is nested)
    const findScrollable = () => {
        const divs = document.querySelectorAll('div');
        return Array.from(divs).find(el => el.scrollHeight > el.clientHeight && 
                                           window.getComputedStyle(el).overflowY !== 'hidden');
    };

    const scrollContainer = findScrollable() || document.querySelector('div[tabindex="-1"]');

    if (!scrollContainer) {
        console.error("❌ Couldn't find the scrollable list. Make sure the 'Group Info' sidebar is open!");
        return;
    }

    let lastCount = 0;
    let stopCount = 0;

    while (stopCount < 10) { // Increased retries to 10 for larger groups
        const elements = document.querySelectorAll('span[title], div[aria-label], span[dir="auto"]');
        
        elements.forEach(el => {
            const val = el.getAttribute('title') || el.getAttribute('aria-label') || el.innerText;
            if (val) {
                const match = val.match(/\+?\d[\d\s-]{9,15}/g);
                if (match) {
                    match.forEach(num => {
                        const clean = num.replace(/[\s-]/g, '');
                        // Filter out those 19-digit internal IDs
                        if (clean.length >= 10 && clean.length <= 13) {
                            allNumbers.add(clean);
                        }
                    });
                }
            }
        });

        console.log(`Current Count: ${allNumbers.size}`);

        // 2. Perform the scroll
        scrollContainer.scrollBy(0, 800);
        
        // 3. Wait for data to load
        await new Promise(r => setTimeout(r, 1000));

        if (allNumbers.size === lastCount) {
            stopCount++;
            // Try a small "jiggle" scroll to trigger lazy loading if stuck
            scrollContainer.scrollBy(0, -50); 
        } else {
            stopCount = 0;
            lastCount = allNumbers.size;
        }
    }

    const finalResult = Array.from(allNumbers);
    console.log(`✅ Finished! Total unique numbers found: ${finalResult.length}`);
    console.log(finalResult.join('\n'));
    copy(finalResult.join('\n'));
    console.log("📋 Copied to clipboard!");
})();
```
### With the copy command in the console
```bash
(async () => {
    console.log("🚀 Starting Aggressive Full Export...");
    const allNumbers = new Set();
    
    const findScrollable = () => {
        const divs = document.querySelectorAll('div');
        return Array.from(divs).find(el => el.scrollHeight > el.clientHeight && 
                                           window.getComputedStyle(el).overflowY !== 'hidden');
    };

    const scrollContainer = findScrollable() || document.querySelector('div[tabindex="-1"]');
    if (!scrollContainer) return console.error("❌ Sidebar not found!");

    let lastCount = 0;
    let stopCount = 0;

    while (stopCount < 10) { 
        document.querySelectorAll('span[title], div[aria-label], span[dir="auto"]').forEach(el => {
            const val = el.getAttribute('title') || el.getAttribute('aria-label') || el.innerText;
            if (val) {
                const matches = val.match(/\+?\d[\d\s-]{9,15}/g);
                if (matches) matches.forEach(num => {
                    const clean = num.replace(/[\s-]/g, '');
                    if (clean.length >= 10 && clean.length <= 13) allNumbers.add(clean);
                });
            }
        });

        console.log(`Current Count: ${allNumbers.size}`);
        scrollContainer.scrollBy(0, 800);
        await new Promise(r => setTimeout(r, 1000));

        if (allNumbers.size === lastCount) {
            stopCount++;
            scrollContainer.scrollBy(0, -50); 
        } else {
            stopCount = 0;
            lastCount = allNumbers.size;
        }
    }

    const finalResult = Array.from(allNumbers).join('\n');
    
    // --- UI BUTTON FALLBACK ---
    const btn = document.createElement('button');
    btn.innerText = `✅ Extraction Done! Click to Copy ${allNumbers.size} Numbers`;
    btn.style = "position:fixed;top:20px;left:50%;transform:translateX(-50%);z-index:9999;padding:20px;background:#25D366;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;box-shadow:0 4px 15px rgba(0,0,0,0.3);";
    
    btn.onclick = async () => {
        await navigator.clipboard.writeText(finalResult);
        btn.innerText = "📋 COPIED TO CLIPBOARD!";
        btn.style.background = "#075E54";
        setTimeout(() => btn.remove(), 3000);
    };
    
    document.body.appendChild(btn);
    console.log("👆 Click the green button at the top of your screen to copy!");
})();
```


# WhatsApp Anti-Abuse & Bulk Messaging Guide (Personal Accounts)

This document outlines the official policies and algorithmic behaviors governing personal (non-business) WhatsApp accounts regarding bulk messaging and automation.

---

## 📖 Official Policy Documentation

WhatsApp does not publish its internal detection algorithms, but the legal and technical basis for account bans is detailed in the following official sources:

### 1. Responsible Use Guide
The primary resource for individual users. It explicitly prohibits "Automated or bulk messages" to maintain platform integrity.
* **Official Link:** [How to use WhatsApp responsibly](https://faq.whatsapp.com/361005896189245)
* **Key Logic:** Utilizes Machine Learning (ML) paired with user-generated reports to identify non-human behavior.

### 2. Technical White Paper: "Stopping Abuse"
A technical overview of how WhatsApp fights spam without compromising end-to-end encryption by analyzing behavioral metadata.
* **Source:** [Stopping Abuse: How WhatsApp Fights Spam](https://www.whatsapp.com/facts/white-paper-stopping-abuse.pdf)
* **Key Logic:** Focuses on "Account Harvesting" (scraping) and registration patterns to block bulk senders at the point of entry.

### 3. Account Restriction Policy (2025/2026 Update)
A new enforcement tier that restricts an account's ability to start new conversations while still allowing replies to existing ones.
* **Official Link:** [About Restricted Accounts](https://faq.whatsapp.com/717472490411581)
* **Primary Trigger:** Repeatedly engaging in high-velocity messaging to unsaved contacts.

---

## 📊 Estimated Messaging Limits (Community Data 2026)

*Note: These are approximations based on platform behavior; actual limits are dynamic and depend on account reputation.*

| Account Type | Est. Daily Limit | Penalty for Violation |
| :--- | :--- | :--- |
| **New Account (<30 days)** | 200–300 messages | Instant Permanent Ban |
| **Established Account** | 500–800 messages | Restriction or Temporary Ban |
| **Broadcast List** | 256 contacts | Delivery failure (if not in contacts) |

---

## 🤖 The Detection Algorithm: Key Signals

The automated system monitors three primary "tripwires" for personal accounts:

### 1. The "Report-to-Message" Ratio
The most critical metric. If **~3%** of recipients click "Report" or "Block," the account is flagged for immediate review or suspension.

### 2. Contact Sync Ratio
The algorithm checks how many recipients have **your number** saved in their address book. 
* **High Risk:** Sending 100+ messages to "cold" numbers (numbers that don't have you saved).
* **Low Risk:** Sending to established contacts.

### 3. Velocity & Interaction Patterns
* **Speed:** Humans do not send 100 messages in 60 seconds. High velocity triggers a "Bot" signature.
* **Reciprocity:** If you send 100 messages and receive **0 replies**, the system concludes the messages are unwanted (spam).

---

## ⚠️ Summary of Risk
For personal accounts, there is no "safe" way to automate bulk messaging. Unlike the Business API, personal accounts lack a "Trust Tier" system. Detection is based on **behavioral metadata**—even if the content of your message is encrypted, the *way* you send it is visible to the anti-spam system.



# WhatsApp Manual Messaging & Risk Mitigation Guide (2026)

This guide details the algorithmic risks associated with manual high-volume messaging on personal WhatsApp accounts and provides a framework for staying under the detection threshold.

---

## ⚖️ Manual vs. Automated: The Technical Reality

While manual messaging avoids the "mechanical" signatures of a script, WhatsApp’s 2026 anti-spam AI focuses on **behavioral outcomes** rather than just the method of delivery.

### 1. The "Human vs. Bot" Signature
* **The Advantage:** Manual typing/pasting creates "irregular delays" (jitter), which bypasses the **Velocity Triggers** that instantly kill automated scripts.
* **The Risk:** Repeatedly pasting the exact same text string 100+ times triggers **Pattern Tracking**. To the AI, "Manual Spam" is indistinguishable from "Smart Botting" if the content is 100% identical.

### 2. The 2026 "Report" Threshold (The 3-Report Rule)
The most significant danger to manual messaging is the user-initiated report.
* **The Trigger:** If you message 100 strangers and just **3 to 5** click the "Report" button within a 1-hour window, your account faces **Automatic Suspension**.
* **The UI Factor:** WhatsApp prominently displays "Block or Report" for all messages from unsaved contacts. The barrier for a user to ban you is lower than ever.

---

## 📊 Risk Comparison Matrix

| Risk Factor | Manual Messaging | Automated Script |
| :--- | :--- | :--- |
| **Detection Speed** | Moderate (Minutes to Hours) | Fast (Seconds to Minutes) |
| **"Spam" Signature** | Lower (Human jitter) | High (Perfect timing) |
| **Primary Ban Reason** | **User Reports** | **Algorithmic Detection** |
| **Account Recovery** | Easier (Human appeal) | Near Impossible (Bot logs) |

---

## 🛡️ Survival Rules for High-Volume Manual Messaging

If you are scaling to 100+ (or even 999) messages manually, follow these protocols to minimize the "Ban Probability":

### A. Personalize the First Line
Avoid "static" templates. Use variables like Name, Company, or Group Name to break the pattern hash.
* ❌ **Bad:** *"Hi, check out our new service at..."*
* ✅ **Good:** *"Hey [Name], I noticed your profile in the [Group Name]..."*

### B. The "20/20" Velocity Rule
To avoid the "High-Volume Burst" trigger, stagger your activity:
* Send to **20 people**.
* Stop all activity for **20 minutes**.
* This mimics natural human usage patterns.

### C. Prioritize "2-Way" Conversations
The algorithm calculates a **Trust Score** based on reciprocity.
* If you send 100 messages and get **10 replies**, your account is considered "Social."
* If you send 100 messages and get **0 replies**, your account is considered "Abrasive."
* *Strategy:* Ask a question to encourage a reply.

### D. The Address Book Shield
Once a user saves your number in their phone, your messages are no longer subject to "Cold Message" filters. 
* Encourage users to save your contact early in the conversation to effectively become "immune" to automated spam filters.

---

## ⚠️ Final Verdict
Manual messaging is a "controlled gamble." While you are safer from the bot-detection algorithm, you are entirely at the mercy of **User Sentiment**. If your message is not valuable, the users will ban you faster than the script will.