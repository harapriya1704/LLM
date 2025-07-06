from openai import OpenAI
import httpx
import os
import certifi
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env', override=True)

# Setup HTTP client with Dell certs (if needed)
http_client = httpx.Client(verify=certifi.where())

# Initialize OpenAI-compatible client
client = OpenAI(
    base_url='https://genai-api-dev.dell.com/v1',
    http_client=http_client,
    api_key=os.environ["DEV_GENAI_API_KEY"]
)

# Configuration
streaming = True
max_output_tokens = 200
model_selected = "mixtral-8x7b-instruct-v01"

# Prompt
prompt = f"Can you explain who the Los Angeles Dodgers are and what they are known for in less than {max_output_tokens} tokens?"

print(f"\n\nModel: {model_selected}")
try:
    completion = client.chat.completions.create(
        model=model_selected,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        max_tokens=max_output_tokens,
        stream=streaming
    )

    if streaming:
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end='', flush=True)
    else:
        print(completion.choices[0].message.content)

except Exception as e:
    print(f"\n❌ Error with model {model_selected}: {e}")
