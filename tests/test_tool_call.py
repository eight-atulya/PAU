import openai
import os

# Connect to local LM Studio API
client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


# Create the file if it does not exist
if not os.path.exists('core_instruction.md'):
    with open('core_instruction.md', 'w', encoding='utf-8') as file:
        file.write('')

# Open the .md file in read mode
with open('core_instruction.md', 'r', encoding='utf-8') as file:
    # Read the content of the file
    core_instruction = file.read()




def generate_response(prompt, model="model-identifier"):
    """Sends a prompt to the AI model and returns the response."""
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": core_instruction},
            {"role": "user", "content": prompt}
            ],
        temperature=0,
    )
    return completion.choices[0].message.content

# Taking user input
user_prompt = input("Enter your prompt: ")

# Calling the function and passing user input
response = generate_response(user_prompt)

# Printing the AI-generated response
print("\nSystem Response:\n", response)