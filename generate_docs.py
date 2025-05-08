import os
from groq import Groq

# Fetch the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client
client = Groq(api_key=api_key)

# Create a prompt for generating Flash USDT-related documentation
prompt = """
Create documentation for Flash USDT. Use the <Flash/> and <USDT/> tags for component rendering.
Ensure the content explains its use, benefits, and key features. Add links and structure the documentation for MDX rendering.
"""

# Make the API call to generate content
completion = client.chat.completions.create(
    model="qwen-qwq-32b",  # Your preferred model
    messages=[{"role": "user", "content": prompt}],
    temperature=0.6,
    max_completion_tokens=2048,
    top_p=0.95,
    stream=False
)

# Extract content from the response
content = completion['choices'][0]['message']['content']

# Generate MDX file with custom tags
mdx_content = f"""
import {{ Flash }} from './components/Flash'
import {{ USDT }} from './components/USDT'

# Flash USDT Documentation

<Flash />
<USDT />

{content}
"""

# Save the generated MDX content to the file
with open("docs/flash-usdt.mdx", "w") as f:
    f.write(mdx_content)

print("MDX content generated successfully!")
