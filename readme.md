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



### this script takes only the unsaved number without name type 

```bash
(() => {
    // 1. Grab the "Group Info" sidebar container
    // We use a broader selector since the specific IDs aren't hitting
    const sidebar = document.querySelector('div[tabindex="-1"]') || document.body;

    // 2. Find all text that looks like a phone number
    // This regex looks for: + followed by digits, spaces, or dashes
    const phoneRegex = /\+?\d[\d\s-]{8,20}/g;
    
    // 3. Extract all matches from the sidebar's HTML
    const matches = sidebar.innerText.match(phoneRegex) || [];
    
    // 4. Clean up: remove spaces/dashes and filter duplicates
    const cleanNumbers = [...new Set(
        matches.map(num => num.replace(/[\s-]/g, ''))
               .filter(num => num.length >= 10) // Ensure it's a full number
    )];

    if (cleanNumbers.length > 0) {
        console.log(`✅ Success! Found ${cleanNumbers.length} unique numbers:`);
        console.log(cleanNumbers.join('\n'));
        
        // Copy to clipboard
        copy(cleanNumbers.join('\n'));
        console.log("📋 Copied to clipboard!");
    } else {
        console.error("❌ Still no luck. Try this: Hover your mouse over one of the numbers in the list, then run the script again.");
    }
})();
```




### this keys take only the unsaved numbers (original numbers no invalid 16 digit numbers)
```bash
(() => {
    // 1. Target the sidebar container specifically
    const container = document.querySelector('div[tabindex="-1"]') || document.body;
    
    // 2. Find all elements that likely contain names or numbers
    // This looks for common classes/roles in web chat apps
    const elements = container.querySelectorAll('span[title], div[dir="auto"]');
    
    const results = new Set();

    elements.forEach(el => {
        const text = el.innerText.trim();
        const title = el.getAttribute('title');

        // Check the visible text and the "title" attribute (where numbers often hide)
        [text, title].forEach(val => {
            if (!val) return;
            
            // Clean the string to see if it's a number
            const clean = val.replace(/[\s-]/g, '');
            
            // Logic: If it starts with + and is a reasonable length, or is 10-12 digits
            if (/^\+?\d{10,15}$/.test(clean)) {
                results.add(clean);
            }
        });
    });

    const finalNumbers = Array.from(results);

    if (finalNumbers.length > 0) {
        console.log(`✅ Found ${finalNumbers.length} numbers:`);
        console.log(finalNumbers.join('\n'));
        copy(finalNumbers.join('\n'));
        console.log("📋 Copied to clipboard!");
    } else {
        console.error("❌ No numbers found. Ensure the 'Group Info' or 'Contact List' sidebar is fully open.");
    }
})();
```


### fetching only the 528 out of 1029 contact

```bash
(async () => {
    console.log("🚀 Starting Full Group Export (1024 members)...");
    const allNumbers = new Set();
    const sidebar = document.querySelector('div[tabindex="-1"]') || document.body;
    const scrollContainer = document.querySelector('div[data-testid="item-list-container"]')?.parentElement || sidebar;

    let lastCount = 0;
    let retries = 0;

    while (retries < 5) {
        // 1. Grab visible numbers & saved IDs
        const elements = document.querySelectorAll('span[title], div[aria-label], span[dir="auto"]');
        elements.forEach(el => {
            const val = el.getAttribute('title') || el.getAttribute('aria-label') || el.innerText;
            if (val) {
                const match = val.match(/\+?\d[\d\s-]{9,15}/g);
                if (match) {
                    match.forEach(num => {
                        const clean = num.replace(/[\s-]/g, '');
                        if (clean.length >= 10 && clean.length <= 13) {
                            allNumbers.add(clean);
                        }
                    });
                }
            }
        });

        console.log(`Caught ${allNumbers.size} numbers so far...`);

        // 2. Scroll down
        scrollContainer.scrollTop += 500;
        
        // 3. Wait for "Lazy Load" to trigger
        await new Promise(resolve => setTimeout(resolve, 800));

        // 4. Check if we found new numbers. If not, retry a few times before stopping.
        if (allNumbers.size === lastCount) {
            retries++;
        } else {
            retries = 0;
            lastCount = allNumbers.size;
        }
    }

    const finalResult = Array.from(allNumbers);
    console.log(`✅ Success! Total unique numbers found: ${finalResult.length}`);
    console.log(finalResult.join('\n'));
    copy(finalResult.join('\n'));
    console.log("📋 All numbers copied to clipboard!");
})();
```

