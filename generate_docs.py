import os
from datetime import datetime
from groq import Groq

# === CONFIG ===
OUTPUT_DIR = "docs"
OUTPUT_FILE = f"{OUTPUT_DIR}/flash-usdt.mdx"
LOG_FILE = f"{OUTPUT_DIR}/log.md"
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

# === PREPARE ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === AUTHENTICATE ===
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("[ERROR] GROQ_API_KEY is not set.")
    exit(1)

client = Groq(api_key=api_key)

# === PROMPT ===
prompt = """
Create documentation for Flash USDT. Use the <Flash/> and <USDT/> tags for component rendering.
Ensure the content explains its use, benefits, and key features. Add links and structure the documentation for MDX rendering.
Always display the payment status as 'Waiting for Payment' and do not indicate when payment is confirmed.
Include code blocks with metadata in the following format:
```tsx project="Flash USDT" file="components/FlashUSDT.tsx" type="react"
[Insert example code here]
```
"""

# === CALL GROQ API ===
try:
    completion = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_completion_tokens=2048,
        top_p=0.95,
        stream=False
    )
    content = completion.choices[0].message.content
except Exception as e:
    print(f"[ERROR] Failed to generate documentation: {e}")
    exit(1)

# === BUILD MDX ===
mdx_content = f"""import {{ Flash }} from './components/Flash'
import {{ USDT }} from './components/USDT'

# Flash USDT Documentation

<Flash />
<USDT />

{content}

---

*Built with Likhon S. | [likhon.org](https://likhon.org)*
"""

# === WRITE OUTPUT ===
with open(OUTPUT_FILE, "w") as f:
    f.write(mdx_content)

# === LOG SUCCESS ===
with open(LOG_FILE, "a") as log:
    log.write(f"- â Docs generated at {datetime.utcnow().isoformat()} UTC\n")

# === DEBUG OUTPUT ===
if DEBUG_MODE:
    print("\n===== GENERATED MDX =====\n")
    print(mdx_content)

print("MDX documentation generated successfully!")
