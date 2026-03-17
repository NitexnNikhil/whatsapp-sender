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

