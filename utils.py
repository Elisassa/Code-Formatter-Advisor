import time
import logging
from groq import Groq
import os

# Load environment variables from a .env file
from dotenv import load_dotenv

load_dotenv()
my_api_key = os.environ.get("GROQCLOUD_API_KEY")

client = Groq(api_key=my_api_key)


# Measure execution time
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Execution time: {end_time - start_time:.2f} seconds.")
        return result

    return wrapper


# Function to read the code file
def read_code_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code


# Function to send a chat completion request
def send_chat_completion_request(code):
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Analyze the following code and provide detailed formatting and improvement suggestions. Focus on the following aspects:
                1. Standardize indentation and spacing for better readability.
                2. Suggest descriptive and meaningful function and variable names.
                3. Add appropriate docstrings to functions to explain their purpose, inputs, and outputs.
                4. Include type hints for function arguments and return values to enhance code clarity.
                5. Highlight any unused imports or redundant code that can be removed.
                6. Suggest improvements to make the code adhere to best practices and improve its overall structure.

                Here is the code:{code}
                """,
            }
        ],
        model="mixtral-8x7b-32768",
    )
