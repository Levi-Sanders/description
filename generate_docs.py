import os
import json
import time
from groq import Groq

# Retrieve the Groq API key from environment variables
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Path for saving the memory state
MEMORY_FILE = "memory_state.json"
DOCS_OUTPUT_PATH = "docs/"

# Load the prompt from the prompt.txt file
def load_prompt():
    with open("prompt.txt", "r") as file:
        return file.read()

# Load memory state (if exists)
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {
        "step": 1,  # Starting step
        "completed_steps": []  # Track completed sections
    }

# Save memory state (for resuming work later)
def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)

# Define the function to generate content based on the prompt
def generate_content(prompt, step, completed_steps):
    # Call the Groq API to generate the documentation
    completion = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_completion_tokens=2048,
        top_p=0.95,
        stream=False
    )

    # Extract the generated content
    content = completion.choices[0].message.content

    # Construct the MDX content with imports and the predefined components
    mdx_content = f"""
    import {{ LinearProcessFlow }} from './components/LinearProcessFlow'
    import {{ Quiz }} from './components/Quiz'
    import {{ Math }} from './components/Math'

    # Flash USDT Documentation

    <LinearProcessFlow />
    <Quiz />
    <Math />

    {content}
    """

    # Create Extended Code Blocks with meta-information
    extended_code_blocks = f"""
    ```tsx project="Flash USDT" file="components/FlashUSDT.tsx" type="react"
    // Example React Component Code
    export default function FlashUSDT() {{
        return <div>Flash USDT Component</div>;
    }}
    ```

    ```js project="Flash USDT" file="server/index.js" type="nodejs"
    // Example Node.js Code
    const express = require('express');
    const app = express();
    app.listen(3000, () => {{
        console.log('Server running on port 3000');
    }});
    ```

    ```html project="Flash USDT" file="public/index.html" type="html"
    <!-- Example HTML Code -->
    <html>
        <head><title>Flash USDT</title></head>
        <body><h1>Welcome to Flash USDT</h1></body>
    </html>
    ```

    ```md project="Flash USDT" file="docs/readme.md" type="markdown"
    # Flash USDT Documentation
    This document covers how to use Flash USDT, how to make transactions, and other important details.
    ```

    ```mermaid title="Example Flowchart" type="diagram"
    graph TD;
        A[Start] --> B[Process];
        B --> C[End];
    ```

    ```python project="Flash USDT" file="scripts/process.py" type="code"
    # Example Python Code
    def process_data(data):
        return data.upper()
    ```

    """

    # Add Chain of Thought (CoT) integration
    thinking_process = """
    <Thinking>
        The task requires detailed documentation with multiple components. The user needs interactive features like quizzes and linear process flows.
        I will structure the content properly, ensuring clarity and SEO optimization. The code blocks will be properly formatted, and I will ensure all necessary information is included.
        The content should also follow best practices for technical documentation, making sure it is easy to understand and visually appealing.
    </Thinking>
    """

    mdx_content = thinking_process + mdx_content + extended_code_blocks

    # Save the MDX content to the output folder
    mdx_filename = f"{DOCS_OUTPUT_PATH}flash-usdt-step{step}.mdx"
    with open(mdx_filename, "w") as f:
        f.write(mdx_content)

    # Also generate an HTML version of the same content
    html_content = f"""
    <html>
        <head><title>Flash USDT Documentation</title></head>
        <body>
            <h1>Flash USDT Documentation</h1>
            <div><LinearProcessFlow /></div>
            <div><Quiz /></div>
            <div><Math /></div>
            <div>{content}</div>
        </body>
    </html>
    """
    html_filename = f"{DOCS_OUTPUT_PATH}flash-usdt-step{step}.html"
    with open(html_filename, "w") as f:
        f.write(html_content)

    # Print the step completed
    print(f"Step {step} completed successfully!")

# Main function that controls the workflow and memory
def run():
    # Load previous memory (if any)
    memory = load_memory()
    current_step = memory["step"]
    completed_steps = memory["completed_steps"]

    # Check which steps are completed and continue with the next step
    for step in range(current_step, 6):  # Assuming 5 total steps to complete
        if step not in completed_steps:
            print(f"Generating content for step {step}...")
            prompt = load_prompt()
            generate_content(prompt, step, completed_steps)

            # Update memory to reflect the completed step
            completed_steps.append(step)
            memory["step"] = step + 1  # Update the next step to process
            save_memory(memory)  # Save the memory after each step

        # Wait between steps (optional)
        time.sleep(10)  # Sleep for 10 seconds before generating the next step

if __name__ == "__main__":
    run()
