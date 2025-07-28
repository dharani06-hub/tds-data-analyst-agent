import os
import openai

# Use environment variable to keep your API key secure
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can switch to "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error from LLM: {str(e)}"
