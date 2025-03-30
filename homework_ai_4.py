import os
from  dotenv import load_dotenv
from google import genai
from google.genai import types
import time
from requests import ReadTimeout
from tenacity import retry, stop_after_attempt, wait_exponential


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

timeout = 15
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=timeout * 1000)
)

@retry(stop=stop_after_attempt(4),
       wait=wait_exponential(
           multiplier=2,
           min=3,
           max=15
       ))
def get_response(prompt):
    time.sleep(0.4)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt]
        )
        return response.text
    except ReadTimeout:
        return f"Request exceeded timeout {timeout} second."
    except Exception as e:
        return f"There was an error: {e}"



if __name__ == "__main__":
    response = get_response("What is API?")
    if response:
        print(response)
    else:
        print("Failed to get a response.")