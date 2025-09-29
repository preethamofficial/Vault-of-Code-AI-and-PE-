import os
from openai import OpenAI

# Make sure your API key is set in the environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, can you hear me?"}]
    )
    print("✅ API is working!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("❌ Something went wrong:", e)
