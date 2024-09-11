import requests  # Library used to send HTTP requests
import os  # For loading environment variables from .env
from dotenv import load_dotenv  # To load the .env file

# Load environment variables from .env file
load_dotenv()

# Define your GroqCloud API Key and Endpoint
GROQCLOUD_API_KEY = os.getenv('GROQCLOUD_API_KEY')  # Retrieve API key from .env file
GROQCLOUD_API_URL = 'https://console.groq.com/api/v1/completions'  # Confirm the correct endpoint from GroqCloud documentation

# Set up the headers for the API request, including the authorization token
headers = {
    'Authorization': f'Bearer {GROQCLOUD_API_KEY}',  # Use Bearer token for authentication
    'Content-Type': 'application/json'  # Specify the request content type as JSON
}

# Define the data payload for the request, including model, prompt, and other parameters
data = {
    "model": "llama3-8b-8192",  # Specify the model you want to use (check GroqCloud docs for available models)
    "prompt": "Explain how to use GroqCloud API in Python.",  # The prompt or question you want the model to answer
    "max_tokens": 100,  # Maximum number of tokens in the response
    "temperature": 0.7  # Controls randomness in output; higher values make responses more creative
}

# Send a POST request to the GroqCloud API endpoint with headers and JSON data
response = requests.post(GROQCLOUD_API_URL, headers=headers, json=data)

# Check if the request was successful (status code 200 means success)
if response.status_code == 200:
    result = response.json()  # Parse the response as JSON
    # Print the generated text from the response
    print('Generated Text:', result['choices'][0]['text'].strip())  
else:
    # If the request failed, print the error status and message
    print('Error:', response.status_code, response.text)
